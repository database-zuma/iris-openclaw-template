# iSeller Data Refresh Commands
# Source this file: source ~/.openclaw/workspace/scripts/iseller_commands.sh

alias iseller-refresh='bash /Users/database-zuma/.openclaw/workspace/scripts/refresh_iseller_data.sh'
alias iseller-refresh-manual='bash /Users/database-zuma/.openclaw/workspace/scripts/manual_refresh_iseller.sh'
alias iseller-status='PGPASSWORD="Zuma-0psCl4w-2026!" /Users/database-zuma/homebrew/Cellar/libpq/18.1_1/bin/psql -h 76.13.194.120 -p 5432 -U openclaw_app -d openclaw_ops -c "SELECT MAX(sale_date) as last_data_date, COUNT(*) as total_rows FROM mart.mv_iseller_summary;"'

echo "iSeller commands loaded:"
echo "  iseller-refresh        - Run full refresh (CSV upload + mart refresh)"
echo "  iseller-refresh-manual - Run manual refresh with confirmation"
echo "  iseller-status         - Check current data status"
