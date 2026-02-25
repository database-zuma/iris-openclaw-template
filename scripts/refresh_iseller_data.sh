#!/bin/bash
# Script to refresh iSeller data daily
# Documentation: ~/.openclaw/docs/iseller-data-workflow.md

WORKSPACE_ROOT="/Users/database-zuma/.openclaw/workspace"
METIS_WORKSPACE="/Users/database-zuma/.openclaw/workspace-metis"
DB_HOST="76.13.194.120"
DB_USER="openclaw_app"
DB_NAME="openclaw_ops"
export PGPASSWORD="Zuma-0psCl4w-2026!"
PSQL="/Users/database-zuma/homebrew/Cellar/libpq/18.1_1/bin/psql"

echo "--- iSeller Data Refresh Start: $(date) ---"

# Step 1: Upload CSV to raw
echo "Step 1: Uploading CSV data to raw.iseller_2026..."
cd "$METIS_WORKSPACE"
python3 upload_iseller_2026.py

# Step 2: Refresh Mart & Materialized View
echo "Step 2: Refreshing PostgreSQL mart tables and summary views..."
"$PSQL" -h "$DB_HOST" -p 5432 -U "$DB_USER" -d "$DB_NAME" -c "SELECT mart.refresh_iseller_marts(); REFRESH MATERIALIZED VIEW mart.mv_iseller_summary;"

# Step 3: Verification
echo "Step 3: Verifying data date..."
"$PSQL" -h "$DB_HOST" -p 5432 -U "$DB_USER" -d "$DB_NAME" -t -c "SELECT MAX(sale_date) FROM mart.mv_iseller_summary;"

echo "--- iSeller Data Refresh Finished: $(date) ---"
