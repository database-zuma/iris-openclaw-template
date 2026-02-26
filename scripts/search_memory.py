#!/usr/bin/env python3
"""
Iris Vector Memory — Semantic Search
=====================================
Search Iris's memory using semantic similarity via pgvector.
Returns the most relevant memory chunks for a given query.

Usage:
    python3 search_memory.py "kapan terakhir bahas planogram?"
    python3 search_memory.py "shipping delay issue" --limit 10
    python3 search_memory.py "RO request Jatim" --since 2026-02-01
    python3 search_memory.py "database error" --source knowledge
    python3 search_memory.py --json "planogram toko baru"

Requires: psycopg2, requests
ENV: GEMINI_API_KEY, DATABASE_URL (or PG* vars from .env)
"""

import os
import sys
import json
import argparse
import warnings
from pathlib import Path
from datetime import datetime

import psycopg2
import psycopg2.extras
import requests

warnings.filterwarnings("ignore")

# ── Config ──────────────────────────────────────────────────────────
ENV_FILE = Path.home() / ".openclaw" / "workspace" / ".env"
GEMINI_MODEL = "gemini-embedding-001"
GEMINI_API_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/{model}:embedContent"
)
DEFAULT_LIMIT = 5


def load_env():
    """Load environment variables from .env file."""
    env = {}
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, _, val = line.partition("=")
                env[key.strip()] = val.strip()
    return env


def get_db_connection(env):
    """Connect to PostgreSQL."""
    db_url = env.get("DATABASE_URL", os.environ.get("DATABASE_URL", ""))
    if db_url:
        return psycopg2.connect(db_url)
    return psycopg2.connect(
        host=env.get("PGHOST", "76.13.194.120"),
        port=env.get("PGPORT", "5432"),
        dbname=env.get("PGDATABASE", "openclaw_ops"),
        user=env.get("PGUSER", "openclaw_app"),
        password=env.get("PGPASSWORD", ""),
    )


def get_query_embedding(text: str, api_key: str) -> list:
    """Generate query embedding via Gemini REST API."""
    url = GEMINI_API_URL.format(model=GEMINI_MODEL) + f"?key={api_key}"
    payload = {
        "model": f"models/{GEMINI_MODEL}",
        "content": {"parts": [{"text": text[:8000]}]},
        "taskType": "RETRIEVAL_QUERY",  # Query mode for search
    }
    resp = requests.post(url, json=payload, timeout=30)
    if resp.status_code == 200:
        return resp.json()["embedding"]["values"]
    else:
        raise Exception(f"Gemini API error {resp.status_code}: {resp.text[:200]}")


def search_memory(
    conn, query_embedding: list, limit: int = 5, since: str = None, source: str = None
) -> list:
    """
    Search memory vectors by cosine similarity.

    Args:
        conn: PostgreSQL connection
        query_embedding: Query vector
        limit: Max results
        since: Filter by date (YYYY-MM-DD)
        source: Filter by source type ('memory', 'knowledge', or None for all)

    Returns:
        List of dicts with content, similarity score, date, source
    """
    conditions = []
    params = [str(query_embedding), limit]

    if since:
        conditions.append("date >= %s")
        params.insert(-1, since)  # Before limit

    if source:
        if source == "memory":
            conditions.append("source_file LIKE 'memory/%%'")
        elif source == "knowledge":
            conditions.append("source_file LIKE 'knowledge/%%'")

    where_clause = ""
    if conditions:
        where_clause = "WHERE " + " AND ".join(conditions)

    # Build query — cosine distance (1 - similarity), lower = more similar
    sql = f"""
        SELECT 
            content,
            date,
            source_file,
            1 - (embedding <=> %s::vector) AS similarity
        FROM iris.memory_vectors
        {where_clause}
        ORDER BY embedding <=> %s::vector
        LIMIT %s
    """

    # We need embedding param twice (for SELECT and ORDER BY)
    query_params = [str(query_embedding)]
    if since:
        query_params.append(since)
    query_params.append(str(query_embedding))
    query_params.append(limit)

    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute(sql, query_params)
        results = cur.fetchall()

    return [dict(r) for r in results]


def format_results(results: list, query: str) -> str:
    """Format search results for display."""
    if not results:
        return f"No memories found matching: '{query}'"

    output = []
    output.append(f'🔍 Semantic search: "{query}"')
    output.append(f"{'─' * 60}")

    for i, r in enumerate(results, 1):
        sim_pct = r["similarity"] * 100
        # Truncate content for display
        content = r["content"][:300]
        if len(r["content"]) > 300:
            content += "..."

        output.append(
            f"\n[{i}] 📅 {r['date']} | 📁 {r['source_file']} | 🎯 {sim_pct:.1f}% match"
        )
        output.append(content)

    output.append(f"\n{'─' * 60}")
    output.append(f"Found {len(results)} relevant memories")
    return "\n".join(output)


def format_json(results: list, query: str) -> str:
    """Format search results as JSON (for programmatic use by Iris)."""
    return json.dumps(
        {
            "query": query,
            "results": [
                {
                    "content": r["content"],
                    "date": str(r["date"]),
                    "source_file": r["source_file"],
                    "similarity": round(float(r["similarity"]), 4),
                }
                for r in results
            ],
            "count": len(results),
        },
        indent=2,
        ensure_ascii=False,
    )


def main():
    parser = argparse.ArgumentParser(description="Iris Vector Memory — Semantic Search")
    parser.add_argument("query", type=str, help="Search query")
    parser.add_argument(
        "--limit", type=int, default=DEFAULT_LIMIT, help="Max results (default: 5)"
    )
    parser.add_argument("--since", type=str, help="Filter by date (YYYY-MM-DD)")
    parser.add_argument(
        "--source",
        type=str,
        choices=["memory", "knowledge"],
        help="Filter by source type",
    )
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    env = load_env()
    api_key = env.get("GEMINI_API_KEY", os.environ.get("GEMINI_API_KEY", ""))
    if not api_key:
        print("❌ GEMINI_API_KEY not found")
        sys.exit(1)

    conn = get_db_connection(env)

    # Generate query embedding
    query_embedding = get_query_embedding(args.query, api_key)

    # Search
    results = search_memory(
        conn,
        query_embedding,
        limit=args.limit,
        since=args.since,
        source=args.source,
    )

    # Output
    if args.json:
        print(format_json(results, args.query))
    else:
        print(format_results(results, args.query))

    conn.close()


if __name__ == "__main__":
    main()
