#!/usr/bin/env python3
import psycopg2

conn = psycopg2.connect(
    host='76.13.194.120',
    database='openclaw_ops',
    user='openclaw_app',
    password='Zuma-0psCl4w-2026!'
)

cur = conn.cursor()

# Check table structure
cur.execute("""
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_schema = 'public' 
  AND table_name = 'sales_summary_plano'
ORDER BY ordinal_position;
""")

columns = cur.fetchall()

print("📋 Table Structure: public.sales_summary_plano\n")
for col in columns:
    print(f"  • {col[0]} ({col[1]})")

# Check sample data for Nagoya/SKA
print("\n\n📊 Sample Data Check:\n")

cur.execute("""
SELECT DISTINCT matched_store_name
FROM public.sales_summary_plano
WHERE matched_store_name LIKE '%nagoya%' OR matched_store_name LIKE '%ska%'
ORDER BY matched_store_name;
""")

stores = cur.fetchall()
for store in stores:
    print(f"  • {store[0]}")

cur.close()
conn.close()
