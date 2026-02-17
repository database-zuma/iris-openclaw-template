#!/bin/bash
# Daily STO tool regeneration + Vercel deploy
# Runs after mart.sto_analysis is rebuilt by cron
# Schedule: 06:10 WIB daily (after Atlas 05:30 + mart rebuild 06:00)

set -e
LOG="/Users/database-zuma/logs/daily-updater.log"
WORKSPACE="/Users/database-zuma/.openclaw/workspace"
BIN_NODE="/Users/database-zuma/homebrew/Cellar/node/25.6.0/bin/node"
VERCEL="$HOME/homebrew/lib/node_modules/vercel/dist/index.js"
PSQL="/Users/database-zuma/homebrew/Cellar/libpq/18.1_1/bin/psql"
DB_URL="postgresql://openclaw_app:Zuma-0psCl4w-2026!@76.13.194.120/openclaw_ops"

mkdir -p "$(dirname "$LOG")"
echo "[$(date '+%Y-%m-%d %H:%M:%S')] === Daily STO + BM Update Start ===" >> "$LOG"

source "$WORKSPACE/.env"

# 1. Rebuild mart.sto_analysis
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Rebuilding mart.sto_analysis..." >> "$LOG"
$PSQL "$DB_URL" -c "SELECT mart.rebuild_sto_analysis();" >> "$LOG" 2>&1 && \
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] mart.sto_analysis rebuilt ✅" >> "$LOG" || \
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] mart.sto_analysis FAILED ❌" >> "$LOG"

# 2. Regenerate STO tool HTML
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Generating STO HTML..." >> "$LOG"
python3 /tmp/gen_sto_v4.py >> "$LOG" 2>&1

# 3. Deploy STO tool
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Deploying STO tool..." >> "$LOG"
cd "$WORKSPACE/zuma-bm-decks/sto-jatim"
DEPLOY_URL=$($BIN_NODE "$VERCEL" --prod --yes --token "$VERCEL_TOKEN" 2>&1 | grep "Production:" | awk '{print $2}')
echo "[$(date '+%Y-%m-%d %H:%M:%S')] STO deployed: $DEPLOY_URL" >> "$LOG"

# Re-alias to permanent URL
$BIN_NODE "$VERCEL" alias set "$DEPLOY_URL" zuma-sto.vercel.app --token "$VERCEL_TOKEN" >> "$LOG" 2>&1
echo "[$(date '+%Y-%m-%d %H:%M:%S')] STO alias zuma-sto.vercel.app ✅" >> "$LOG"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] === Done ===" >> "$LOG"
