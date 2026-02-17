#!/usr/bin/env python3
import psycopg2

conn = psycopg2.connect(
    host='76.13.194.120',
    database='openclaw_ops',
    user='openclaw_app',
    password='Zuma-0psCl4w-2026!'
)

cur = conn.cursor()

schemas = ['raw', 'portal', 'core', 'mart', 'public']

for schema in schemas:
    print(f"\n{'='*50}")
    print(f"📁 SCHEMA: {schema.upper()}")
    print(f"{'='*50}\n")
    
    cur.execute(f"""
    SELECT table_name 
    FROM information_schema.tables 
    WHERE table_schema = '{schema}'
    ORDER BY table_name;
    """)
    
    tables = cur.fetchall()
    for table in tables:
        print(f"  • {schema}.{table[0]}")

cur.close()
conn.close()
