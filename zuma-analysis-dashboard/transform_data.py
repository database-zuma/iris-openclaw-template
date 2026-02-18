#!/usr/bin/env python3
"""Transform existing data.json to add new KPI fields."""
import json

# Load existing data
with open('/Users/database-zuma/.openclaw/workspace/zuma-analysis-dashboard/data.json', 'r') as f:
    data = json.load(f)

print(f"Loaded {len(data['articles'])} articles")

# Add new fields to each article
for article in data['articles']:
    # New stock fields
    article['total_stock_wh'] = 0  # Warehouse stock - to be populated from DB
    article['total_stock_store'] = article.get('total_stock', 0)  # Retail store stock
    article['stock_wh_by_store'] = {}  # Warehouse stock by store
    
    # New sales fields
    article['sales_retail_3mo'] = article.get('sales_3mo', 0)  # Retail sales
    article['sales_online_3mo'] = 0  # Online MBB sales
    article['sales_nonretail_3mo'] = 0  # Non-retail sales (event, konsinyasi, wholesale)
    
    # Ensure total_stock includes both warehouse and store
    article['total_stock'] = article['total_stock_wh'] + article['total_stock_store']

# Calculate KPI totals
kpi_totals = {
    'total_stock_wh': sum(a['total_stock_wh'] for a in data['articles']),
    'total_stock_store': sum(a['total_stock_store'] for a in data['articles']),
    'total_sales_retail': sum(a['sales_retail_3mo'] for a in data['articles']),
    'total_sales_online': sum(a['sales_online_3mo'] for a in data['articles']),
    'total_sales_nonretail': sum(a['sales_nonretail_3mo'] for a in data['articles']),
    'total_sales_all': sum(a['sales_3mo'] for a in data['articles']),
}

# Add KPI totals and new metadata
data['metadata']['kpi_totals'] = kpi_totals
data['warehouse_stores'] = []  # Will be populated from DB
data['store_category'] = {}  # Will map store names to categories

print("\nKPI Totals:")
for k, v in kpi_totals.items():
    print(f"  {k}: {v:,.0f}")

# Save transformed data
with open('/Users/database-zuma/.openclaw/workspace/zuma-analysis-dashboard/data.json', 'w') as f:
    json.dump(data, f, separators=(',', ':'), ensure_ascii=False)

print("\n✓ data.json updated with new KPI fields")
