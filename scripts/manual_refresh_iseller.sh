#!/bin/bash
# Manual trigger for iSeller data refresh
# Usage: ./manual_refresh_iseller.sh

echo "🚀 Manual iSeller Data Refresh Triggered"
echo "=========================================="
echo ""
echo "Running: bash /Users/database-zuma/.openclaw/workspace/scripts/refresh_iseller_data.sh"
echo ""

bash /Users/database-zuma/.openclaw/workspace/scripts/refresh_iseller_data.sh

exit_code=$?

echo ""
echo "=========================================="
if [ $exit_code -eq 0 ]; then
    echo "✅ Refresh completed successfully!"
else
    echo "❌ Refresh failed with exit code: $exit_code"
fi
