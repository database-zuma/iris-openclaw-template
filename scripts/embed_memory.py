#!/usr/bin/env python3
"""
Iris Vector Memory — Embed & Index
===================================
Reads Iris memory/*.md files, chunks them into semantic units,
generates embeddings via Gemini API, and upserts to PostgreSQL pgvector.

Usage:
    python3 embed_memory.py                  # Embed new/changed memories only
    python3 embed_memory.py --full           # Re-embed everything
    python3 embed_memory.py --file 2026-02-27.md  # Embed specific file
    python3 embed_memory.py --stats          # Show embedding stats
    python3 embed_memory.py --no-classify    # Embed without signal classification

Requires: psycopg2, requests
ENV: GEMINI_API_KEY, DATABASE_URL (or PG* vars from .env)
"""

import os
import re
import sys
import json
import hashlib
import time
import subprocess
import argparse
import warnings
from pathlib import Path
from datetime import datetime

import psycopg2
import psycopg2.extras
import requests

warnings.filterwarnings("ignore")

# ── Config ──────────────────────────────────────────────────────────
MEMORY_DIR = Path.home() / ".openclaw" / "workspace" / "memory"
KNOWLEDGE_DIR = Path.home() / ".openclaw" / "workspace" / "knowledge"
ENV_FILE = Path.home() / ".openclaw" / "workspace" / ".env"

GEMINI_MODEL = "gemini-embedding-001"
GEMINI_API_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/{model}:embedContent"
)
EMBEDDING_DIM = 3072

# Chunk settings
MIN_CHUNK_LENGTH = 50  # Skip chunks shorter than this
MAX_CHUNK_LENGTH = 2000  # Split chunks longer than this
BATCH_DELAY = 0.1  # Seconds between API calls (rate limiting)


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


def get_gemini_embedding(
    text: str, api_key: str, task_type: str = "RETRIEVAL_DOCUMENT"
) -> list:
    """Generate embedding via Gemini REST API."""
    url = GEMINI_API_URL.format(model=GEMINI_MODEL) + f"?key={api_key}"
    payload = {
        "model": f"models/{GEMINI_MODEL}",
        "content": {"parts": [{"text": text[:8000]}]},  # Gemini limit
        "taskType": task_type,
    }
    resp = requests.post(url, json=payload, timeout=30)
    if resp.status_code == 200:
        return resp.json()["embedding"]["values"]
    else:
        raise Exception(f"Gemini API error {resp.status_code}: {resp.text[:200]}")


def content_hash(text: str) -> str:
    """SHA256 hash of content for dedup."""
    return hashlib.sha256(text.encode()).hexdigest()[:32]


def chunk_memory_file(filepath: Path) -> list[dict]:
    """
    Parse a memory markdown file into semantic chunks.

    Strategy:
    - Split by ## headers (each section = 1 chunk)
    - If no headers, split by double newlines (paragraphs)
    - If a section is too long, split by single newlines
    - Skip chunks that are too short (< MIN_CHUNK_LENGTH chars)
    """
    text = filepath.read_text(encoding="utf-8")
    filename = filepath.name

    # Extract date from filename (YYYY-MM-DD.md)
    date_match = re.match(r"(\d{4}-\d{2}-\d{2})", filename)
    file_date = (
        date_match.group(1) if date_match else datetime.now().strftime("%Y-%m-%d")
    )

    chunks = []

    # Split by ## headers first
    sections = re.split(r"(?m)^##\s+", text)

    if len(sections) <= 1:
        # No ## headers — split by paragraphs (double newline)
        sections = text.split("\n\n")

    for i, section in enumerate(sections):
        section = section.strip()
        if len(section) < MIN_CHUNK_LENGTH:
            continue

        # If section is too long, split further
        if len(section) > MAX_CHUNK_LENGTH:
            sub_parts = section.split("\n")
            current = ""
            for part in sub_parts:
                if (
                    len(current) + len(part) > MAX_CHUNK_LENGTH
                    and len(current) >= MIN_CHUNK_LENGTH
                ):
                    chunks.append(
                        {
                            "date": file_date,
                            "content": current.strip(),
                            "source_file": f"memory/{filename}",
                            "chunk_index": len(chunks),
                            "content_hash": content_hash(current.strip()),
                        }
                    )
                    current = part + "\n"
                else:
                    current += part + "\n"
            if current.strip() and len(current.strip()) >= MIN_CHUNK_LENGTH:
                chunks.append(
                    {
                        "date": file_date,
                        "content": current.strip(),
                        "source_file": f"memory/{filename}",
                        "chunk_index": len(chunks),
                        "content_hash": content_hash(current.strip()),
                    }
                )
        else:
            chunks.append(
                {
                    "date": file_date,
                    "content": section,
                    "source_file": f"memory/{filename}",
                    "chunk_index": i,
                    "content_hash": content_hash(section),
                }
            )

    return chunks


def chunk_knowledge_file(filepath: Path) -> list[dict]:
    """
    Parse a knowledge markdown file into semantic chunks.
    Same strategy as memory but different source_file prefix.
    """
    text = filepath.read_text(encoding="utf-8")
    rel_path = filepath.relative_to(KNOWLEDGE_DIR)

    # Use file modification date
    mtime = datetime.fromtimestamp(filepath.stat().st_mtime)
    file_date = mtime.strftime("%Y-%m-%d")

    chunks = []
    sections = re.split(r"(?m)^##\s+", text)

    if len(sections) <= 1:
        sections = text.split("\n\n")

    for i, section in enumerate(sections):
        section = section.strip()
        if len(section) < MIN_CHUNK_LENGTH:
            continue

        if len(section) > MAX_CHUNK_LENGTH:
            sub_parts = section.split("\n")
            current = ""
            for part in sub_parts:
                if (
                    len(current) + len(part) > MAX_CHUNK_LENGTH
                    and len(current) >= MIN_CHUNK_LENGTH
                ):
                    chunks.append(
                        {
                            "date": file_date,
                            "content": current.strip(),
                            "source_file": f"knowledge/{rel_path}",
                            "chunk_index": len(chunks),
                            "content_hash": content_hash(current.strip()),
                        }
                    )
                    current = part + "\n"
                else:
                    current += part + "\n"
            if current.strip() and len(current.strip()) >= MIN_CHUNK_LENGTH:
                chunks.append(
                    {
                        "date": file_date,
                        "content": current.strip(),
                        "source_file": f"knowledge/{rel_path}",
                        "chunk_index": len(chunks),
                        "content_hash": content_hash(current.strip()),
                    }
                )
        else:
            chunks.append(
                {
                    "date": file_date,
                    "content": section,
                    "source_file": f"knowledge/{rel_path}",
                    "chunk_index": i,
                    "content_hash": content_hash(section),
                }
            )

    return chunks


def get_existing_hashes(conn) -> set:
    """Get all existing content hashes from DB."""
    with conn.cursor() as cur:
        cur.execute("SELECT content_hash FROM iris.memory_vectors")
        return {row[0] for row in cur.fetchall()}


def upsert_chunk(conn, chunk: dict, embedding: list):
    """Insert or update a memory chunk with its embedding."""
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO iris.memory_vectors (date, content, embedding, source_file, chunk_index, content_hash)
            VALUES (%s, %s, %s::vector, %s, %s, %s)
            ON CONFLICT (content_hash) DO UPDATE SET
                embedding = EXCLUDED.embedding,
                content = EXCLUDED.content,
                date = EXCLUDED.date
        """,
            (
                chunk["date"],
                chunk["content"],
                str(embedding),
                chunk["source_file"],
                chunk["chunk_index"],
                chunk["content_hash"],
            ),
        )
    conn.commit()


def show_stats(conn):
    """Print embedding statistics."""
    with conn.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM iris.memory_vectors")
        total = cur.fetchone()[0]

        cur.execute("""
            SELECT source_file, COUNT(*), MIN(date), MAX(date) 
            FROM iris.memory_vectors 
            GROUP BY source_file 
            ORDER BY MAX(date) DESC
        """)
        files = cur.fetchall()

        cur.execute("SELECT MIN(date), MAX(date) FROM iris.memory_vectors")
        date_range = cur.fetchone()

    print(f"\n📊 Iris Vector Memory Stats")
    print(f"{'─' * 50}")
    print(f"Total chunks: {total}")
    if date_range[0]:
        print(f"Date range: {date_range[0]} → {date_range[1]}")
    print(f"\nBy source file:")
    for f, count, min_d, max_d in files:
        print(f"  {f}: {count} chunks ({min_d})")
    print()


def main():
    parser = argparse.ArgumentParser(description="Iris Vector Memory — Embed & Index")
    parser.add_argument("--full", action="store_true", help="Re-embed everything")
    parser.add_argument("--file", type=str, help="Embed specific memory file")
    parser.add_argument("--stats", action="store_true", help="Show stats only")
    parser.add_argument(
        "--include-knowledge", action="store_true", help="Also embed knowledge/ files"
    )
    parser.add_argument(
        "--no-classify", action="store_true",
        help="Skip auto signal classification after embedding"
    )
    args = parser.parse_args()

    env = load_env()
    api_key = env.get("GEMINI_API_KEY", os.environ.get("GEMINI_API_KEY", ""))
    if not api_key:
        print("❌ GEMINI_API_KEY not found in .env or environment")
        sys.exit(1)

    conn = get_db_connection(env)

    if args.stats:
        show_stats(conn)
        conn.close()
        return

    # Collect files to process
    memory_files = []
    if args.file:
        fp = MEMORY_DIR / args.file
        if not fp.exists():
            print(f"❌ File not found: {fp}")
            sys.exit(1)
        memory_files = [fp]
    else:
        memory_files = sorted(MEMORY_DIR.glob("*.md"))
        # Exclude special files
        memory_files = [f for f in memory_files if not f.name.startswith(".")]

    # Get existing hashes (skip if --full)
    existing_hashes = set() if args.full else get_existing_hashes(conn)

    # Chunk all files
    all_chunks = []
    for fp in memory_files:
        chunks = chunk_memory_file(fp)
        all_chunks.extend(chunks)

    # Optionally include knowledge files
    if args.include_knowledge:
        for fp in sorted(KNOWLEDGE_DIR.rglob("*.md")):
            if fp.name == "INDEX.md":
                continue
            chunks = chunk_knowledge_file(fp)
            all_chunks.extend(chunks)

    # Filter out already-embedded chunks
    new_chunks = [c for c in all_chunks if c["content_hash"] not in existing_hashes]

    if not new_chunks:
        print("✅ All memories already embedded. Nothing new to process.")
        show_stats(conn)
        conn.close()
        return

    print(f"📝 Found {len(all_chunks)} total chunks, {len(new_chunks)} new to embed")

    # Embed and upsert
    success = 0
    errors = 0
    for i, chunk in enumerate(new_chunks):
        try:
            embedding = get_gemini_embedding(chunk["content"], api_key)
            upsert_chunk(conn, chunk, embedding)
            success += 1
            # Progress
            if (i + 1) % 10 == 0 or i == len(new_chunks) - 1:
                print(
                    f"  ✅ {i + 1}/{len(new_chunks)} embedded ({chunk['source_file']})"
                )
            time.sleep(BATCH_DELAY)
        except Exception as e:
            errors += 1
            print(f"  ❌ Error embedding chunk {i} from {chunk['source_file']}: {e}")

    print(f"\n🎉 Done! Embedded: {success}, Errors: {errors}")

    # Note: pgvector 0.6.0 caps index dims at 2000, but Gemini embeddings are 3072.
    # Sequential scan is fast enough for <10K chunks. Skip index creation.
    # If pgvector is upgraded to 0.7+, uncomment below:
    # CREATE INDEX ... USING hnsw (embedding vector_cosine_ops)
    if success > 0:
        print(f"📐 Skipping vector index (3072 dims > pgvector 0.6.0 limit of 2000).")
        print(f"   Sequential scan is fast for {success + len(existing_hashes)} chunks.")

    show_stats(conn)
    conn.close()

    # ── Post-embed hook: auto-classify new chunks ──
    if success > 0 and not getattr(args, 'no_classify', False):
        print("\n🔍 Auto-classifying new chunks with signal extraction...")
        script_dir = Path(__file__).parent
        classify_script = script_dir / "extract_signals.py"
        if classify_script.exists():
            result = subprocess.run(
                [sys.executable, str(classify_script)],
                capture_output=False
            )
            if result.returncode != 0:
                print("⚠️  Signal classification had errors (see above). Run manually: python3 scripts/extract_signals.py")
        else:
            print(f"⚠️  extract_signals.py not found at {classify_script}")

if __name__ == "__main__":
    main()
