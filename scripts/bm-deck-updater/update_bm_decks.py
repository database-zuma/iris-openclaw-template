#!/usr/bin/env python3
"""
BM Deck Updater — Weekly Monday 07:00 WIB
Queries live DB data, updates HTML markers, deploys to Vercel.

Usage:
  python3 update_bm_decks.py                  # Update all branches
  python3 update_bm_decks.py --branch jatim   # Update specific branch
  python3 update_bm_decks.py --dry-run        # Preview without deploying
"""

import re
import sys
import subprocess
import argparse
from datetime import date, datetime
from pathlib import Path

# Add script dir to path
sys.path.insert(0, str(Path(__file__).parent))
from config import DB_URL, VERCEL_TOKEN, VERCEL_BIN, VERCEL_CLI, BRANCHES
from queries import (
    get_connection, get_current_period,
    get_store_revenue, get_store_targets,
    get_ff_fa_fs, get_bcg_series, get_top_products,
)


# ─── Helpers ────────────────────────────────────────────────────────────────

def fmt_rp(value):
    """Format Rupiah: 717000000 → '717M', 1200000000 → '1.2B'"""
    if value is None:
        return "—"
    value = int(value)
    if value >= 1_000_000_000:
        return f"{value/1_000_000_000:.1f}B".replace(".0B", "B")
    elif value >= 1_000_000:
        return f"{value/1_000_000:.0f}M"
    elif value >= 1_000:
        return f"{value/1_000:.0f}K"
    return str(value)


def fmt_pct(value, plus=True):
    """Format percentage with optional + sign."""
    if value is None:
        return "—"
    value = float(value)
    sign = "+" if value > 0 and plus else ""
    return f"{sign}{value:.1f}%"


def ach_class(pct):
    """Return CSS class for achievement color."""
    if pct is None:
        return "ach-amber"
    pct = float(pct)
    if pct >= 90:
        return "ach-green"
    elif pct >= 70:
        return "ach-amber"
    return "ach-red"


def ach_emoji(pct):
    if pct is None:
        return "🟡"
    pct = float(pct)
    if pct >= 90:
        return "🟢"
    elif pct >= 70:
        return "🟡"
    return "🔴"


def momentum(jan_ach, feb_ach_proj):
    """Return momentum arrow based on Jan vs Feb projected achievement."""
    if jan_ach is None or feb_ach_proj is None:
        return "→"
    diff = float(feb_ach_proj) - float(jan_ach)
    if diff > 5:
        return "↑ Membaik"
    elif diff < -5:
        return "↓ Melambat"
    return "→ Stabil"


def momentum_color(jan_ach, feb_ach_proj):
    if jan_ach is None or feb_ach_proj is None:
        return "#6b7280"
    diff = float(feb_ach_proj) - float(jan_ach)
    if diff > 5:
        return "#16a34a"
    elif diff < -5:
        return "#d97706"
    return "#6b7280"


def classify_bcg(yoy_pct, ytd_now, median_volume):
    """Classify series into BCG quadrant."""
    if yoy_pct is None:
        return "new"
    yoy = float(yoy_pct)
    vol = int(ytd_now)
    if yoy >= 0 and vol >= median_volume:
        return "star"
    elif yoy >= 0 and vol < median_volume:
        return "qmark"
    elif yoy < 0 and vol >= median_volume:
        return "cashcow"
    else:
        return "dog"


# ─── HTML Marker Update ──────────────────────────────────────────────────────

def replace_marker(html, marker, new_value):
    """Replace content between <!-- BM:marker --> ... <!-- /BM:marker --> tags."""
    pattern = rf'<!-- BM:{re.escape(marker)} -->(.*?)<!-- /BM:{re.escape(marker)} -->'
    replacement = f'<!-- BM:{marker} -->{new_value}<!-- /BM:{marker} -->'
    new_html, count = re.subn(pattern, replacement, html, flags=re.DOTALL)
    if count == 0:
        print(f"  ⚠️  Marker not found: {marker}")
    return new_html


# ─── Branch Update ───────────────────────────────────────────────────────────

def update_branch(branch_key, dry_run=False):
    cfg = BRANCHES[branch_key]
    label = cfg["label"]
    stores = cfg["stores"]
    deck_folder = cfg["deck_folder"]
    html_path = Path(deck_folder) / "index.html"

    print(f"\n{'='*60}")
    print(f"🏪 Updating BM Deck: {label}")
    print(f"{'='*60}")

    # ── Query data ──────────────────────────────────────────
    year, month, day_elapsed, days_in_month = get_current_period()
    today_str = date.today().strftime("%-d %b %Y")
    projection_factor = days_in_month / day_elapsed if day_elapsed > 0 else 1

    print(f"  📅 Period: {year} | Day {day_elapsed}/{days_in_month} | Proj factor: {projection_factor:.2f}")

    print("  🔌 Connecting to DB...")
    conn = get_connection(DB_URL)

    print("  📊 Querying revenue per store...")
    revenue_rows = get_store_revenue(conn, stores, year)

    print("  🎯 Querying targets...")
    target_rows = get_store_targets(conn, stores, year)

    print("  📐 Querying FF/FA/FS...")
    ff_rows = get_ff_fa_fs(conn, stores)

    print("  📦 Querying BCG series data...")
    bcg_rows = get_bcg_series(conn, stores, year)

    conn.close()
    print("  ✅ DB queries done")

    # ── Parse data into dicts ────────────────────────────────
    # Revenue: {store_name: {rev_jan, rev_feb, rev_jan_ly, rev_feb_ly}}
    rev_data = {}
    for row in revenue_rows:
        store, rev_jan, rev_feb, rev_jan_ly, rev_feb_ly = row
        rev_data[store.lower()] = {
            "rev_jan": int(rev_jan or 0),
            "rev_feb": int(rev_feb or 0),
            "rev_jan_ly": int(rev_jan_ly or 0),
            "rev_feb_ly": int(rev_feb_ly or 0),
        }

    # Targets: {store_name_lower: {jan, feb, ...}}
    tgt_data = {}
    for row in target_rows:
        store = row[0]
        tgt_data[store.lower()] = {
            "jan": int(row[1] or 0), "feb": int(row[2] or 0),
            "mar": int(row[3] or 0), "apr": int(row[4] or 0),
        }

    # FF/FA/FS: {store_name_lower: {ff, fa, fs, date}}
    ff_data = {}
    for row in ff_rows:
        store, ff, fa, fs, snap_date = row
        ff_data[store.lower()] = {
            "ff": float(ff or 0), "fa": float(fa or 0),
            "fs": float(fs or 0), "date": snap_date,
        }

    # ── Branch totals ────────────────────────────────────────
    total_rev_jan = sum(v["rev_jan"] for v in rev_data.values())
    total_rev_feb = sum(v["rev_feb"] for v in rev_data.values())
    total_jan_ly = sum(v["rev_jan_ly"] for v in rev_data.values())
    total_tgt_jan = sum(v.get("jan", 0) for v in tgt_data.values())
    total_tgt_feb = sum(v.get("feb", 0) for v in tgt_data.values())

    branch_ach_jan = (total_rev_jan / total_tgt_jan * 100) if total_tgt_jan > 0 else None
    branch_yoy_jan = (total_rev_jan / total_jan_ly - 1) * 100 if total_jan_ly > 0 else None
    feb_projected = total_rev_feb * projection_factor
    branch_ach_feb_proj = (feb_projected / total_tgt_feb * 100) if total_tgt_feb > 0 else None

    avg_ff = sum(v["ff"] for v in ff_data.values()) / len(ff_data) if ff_data else 0
    stores_below_ff_70 = sum(1 for v in ff_data.values() if v["ff"] < 70)

    run_rate_pct = (total_rev_feb / total_tgt_feb * 100) if total_tgt_feb > 0 else None
    time_elapsed_pct = day_elapsed / days_in_month * 100

    print(f"  💰 Branch total Jan: {fmt_rp(total_rev_jan)} | Target: {fmt_rp(total_tgt_jan)} | Ach: {branch_ach_jan:.0f}%")
    print(f"  📈 YoY Jan: {branch_yoy_jan:+.1f}%")
    print(f"  📐 Avg FF: {avg_ff:.1f}%")

    # ── Update HTML markers ──────────────────────────────────
    print(f"  📝 Reading HTML: {html_path}")
    html = html_path.read_text()

    # Cover KPIs
    html = replace_marker(html, "cover_stores_count", str(len([s for s in stores if "wholesale" not in s and "pusat" not in s])))
    html = replace_marker(html, "cover_rev_jan", fmt_rp(total_rev_jan))
    html = replace_marker(html, "cover_ach_jan", f"{branch_ach_jan:.0f}%" if branch_ach_jan else "—")
    html = replace_marker(html, "cover_avg_ff", f"{avg_ff:.0f}%")
    html = replace_marker(html, "last_update_date", today_str)

    # Feb run rate badge
    behind_warning = ""
    if run_rate_pct is not None and time_elapsed_pct > 0:
        if run_rate_pct < time_elapsed_pct - 5:
            behind_warning = f"⚠️ BEHIND ({time_elapsed_pct:.0f}% waktu, {run_rate_pct:.0f}% tercapai)"
        else:
            behind_warning = f"✅ On track ({run_rate_pct:.0f}% dari target)"
    html = replace_marker(html, "feb_run_rate_warning", behind_warning)
    html = replace_marker(html, "feb_ytd_rev", fmt_rp(total_rev_feb))
    html = replace_marker(html, "feb_proj_rev", fmt_rp(int(feb_projected)))
    html = replace_marker(html, "feb_tgt", fmt_rp(total_tgt_feb))

    print(f"  ✅ HTML markers updated (or logged if not found)")

    # ── Write HTML ───────────────────────────────────────────
    if not dry_run:
        html_path.write_text(html)
        print(f"  💾 HTML written: {html_path}")

        # ── Deploy to Vercel ─────────────────────────────────────
        print(f"  🚀 Deploying to Vercel...")
        result = subprocess.run(
            [VERCEL_BIN, VERCEL_CLI, "--prod", "--yes", "--token", VERCEL_TOKEN],
            cwd=deck_folder,
            capture_output=True, text=True, timeout=120,
        )
        if result.returncode == 0:
            # Extract deployment URL
            deploy_url = None
            for line in result.stdout.splitlines():
                if "Production:" in line or "https://" in line:
                    deploy_url = line.strip().split()[-1]
            print(f"  ✅ Deployed: {deploy_url}")

            # Set alias
            if deploy_url:
                alias = cfg["vercel_alias"]
                alias_result = subprocess.run(
                    [VERCEL_BIN, VERCEL_CLI, "alias", "set", deploy_url, alias, "--token", VERCEL_TOKEN],
                    capture_output=True, text=True, timeout=30,
                )
                if alias_result.returncode == 0:
                    print(f"  🔗 Alias set: https://{alias}")
                else:
                    print(f"  ⚠️  Alias failed: {alias_result.stderr[:200]}")
        else:
            print(f"  ❌ Deploy failed: {result.stderr[:500]}")
            return False
    else:
        print(f"  🔍 DRY RUN — not deploying")

    # ── Log result ───────────────────────────────────────────
    log_path = Path(__file__).parent / "update_log.md"
    with open(log_path, "a") as f:
        status = "DRY" if dry_run else "✅"
        f.write(f"| {datetime.now().strftime('%Y-%m-%d %H:%M')} | {label} | {fmt_rp(total_rev_jan)} | {branch_ach_jan:.0f}% | {avg_ff:.1f}% FF | {status} |\n")

    return True


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Weekly BM Deck Updater")
    parser.add_argument("--branch", help="Specific branch key (e.g. jatim)")
    parser.add_argument("--dry-run", action="store_true", help="Preview without deploying")
    args = parser.parse_args()

    print(f"\n🌸 BM Deck Updater — {datetime.now().strftime('%Y-%m-%d %H:%M WIB')}")
    print(f"{'='*60}")

    branches_to_update = [args.branch] if args.branch else list(BRANCHES.keys())
    results = {}

    for branch_key in branches_to_update:
        if branch_key not in BRANCHES:
            print(f"❌ Branch not found: {branch_key}. Available: {list(BRANCHES.keys())}")
            continue
        try:
            success = update_branch(branch_key, dry_run=args.dry_run)
            results[branch_key] = "✅" if success else "❌"
        except Exception as e:
            print(f"  ❌ Error updating {branch_key}: {e}")
            import traceback
            traceback.print_exc()
            results[branch_key] = f"❌ {e}"

    print(f"\n{'='*60}")
    print("📋 Summary:")
    for branch, status in results.items():
        print(f"  {status} {branch} ({BRANCHES[branch]['label']})")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
