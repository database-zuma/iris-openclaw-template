# BM Deck Updater

Weekly automated updater untuk Branch Manager review decks.  
Runs every **Monday 07:00 WIB** via Mac mini cron.

## Architecture

```
update_bm_decks.py     ← main script (loop all branches)
config.py              ← branch configs (stores, Vercel alias, folder)
queries.py             ← SQL queries (revenue, targets, FF/FA/FS, BCG)
update_log.md          ← auto-generated run history
```

## How It Works

1. Query PostgreSQL (core.sales_with_product + portal.store_monthly_target + mart.ff_fa_fs_daily)
2. Update HTML markers (`<!-- BM:marker --> ... <!-- /BM:marker -->`) in each branch's index.html
3. Deploy to Vercel via CLI
4. Set permanent alias (e.g. zuma-bm-jatim.vercel.app stays the same)
5. Log result to update_log.md

## HTML Markers Required in index.html

Add these comment markers around dynamic values in the HTML files:

```html
<!-- BM:cover_stores_count -->11<!-- /BM:cover_stores_count -->
<!-- BM:cover_rev_jan -->717M<!-- /BM:cover_rev_jan -->
<!-- BM:cover_ach_jan -->87%<!-- /BM:cover_ach_jan -->
<!-- BM:cover_avg_ff -->66%<!-- /BM:cover_avg_ff -->
<!-- BM:last_update_date -->17 Feb 2026<!-- /BM:last_update_date -->
<!-- BM:feb_ytd_rev -->360M<!-- /BM:feb_ytd_rev -->
<!-- BM:feb_proj_rev -->593M<!-- /BM:feb_proj_rev -->
<!-- BM:feb_tgt -->688M<!-- /BM:feb_tgt -->
<!-- BM:feb_run_rate_warning -->⚠️ BEHIND (61% waktu, 52% tercapai)<!-- /BM:feb_run_rate_warning -->
```

⚠️ **TODO**: Add these markers to bm-jatim/index.html — currently the HTML has hardcoded values.  
The script will log "Marker not found" warnings until markers are added.

## Usage

```bash
# Update all branches
cd ~/.openclaw/workspace/scripts/bm-deck-updater
python3 update_bm_decks.py

# Update specific branch
python3 update_bm_decks.py --branch jatim

# Dry run (preview without deploying)
python3 update_bm_decks.py --dry-run
```

## Adding a New Branch

1. Create the HTML deck in `zuma-business-skills/references/decks/bm-{branch}/index.html`
2. Add BM markers to the HTML (see above)
3. Add branch config to `config.py` under `BRANCHES`
4. Test: `python3 update_bm_decks.py --branch {branch} --dry-run`
5. Run: `python3 update_bm_decks.py --branch {branch}`

## Cron Schedule

```
Mac mini cron — every Monday 07:00 WIB (00:00 UTC)
0 0 * * 1 cd ~/.openclaw/workspace/scripts/bm-deck-updater && python3 update_bm_decks.py >> ~/logs/bm-deck-updater.log 2>&1
```

## Active Branches

| Branch | URL | Status |
|--------|-----|--------|
| Jawa Timur | https://zuma-bm-jatim.vercel.app | ✅ Live |
| Bali | https://zuma-bm-bali.vercel.app | 🔜 Pending |
| Jakarta | https://zuma-bm-jakarta.vercel.app | 🔜 Pending |
| Sumatra | https://zuma-bm-sumatra.vercel.app | 🔜 Pending |
| Sulawesi | https://zuma-bm-sulawesi.vercel.app | 🔜 Pending |
| Batam | https://zuma-bm-batam.vercel.app | 🔜 Pending |
