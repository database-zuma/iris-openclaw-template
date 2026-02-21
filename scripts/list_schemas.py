#!/usr/bin/env python3
import psycopg2

conn = psycopg2.connect(
    host='76.13.194.120',
    database='openclaw_ops',
    user='openclaw_app',
    password='Zuma-0psCl4w-2026!'
)

cur = conn.cursor()

# List all schemas
cur.execute("""
SELECT schema_name 
FROM information_schema.schemata 
WHERE schema_name NOT IN ('pg_catalog', 'information_schema', 'pg_toast')
ORDER BY schema_name;
""")

schemas = cur.fetchall()

print("📊 Available Schemas:\n")
for schema in schemas:
    schema_name = schema[0]
    
    # Count tables in each schema
    cur.execute(f"""
    SELECT COUNT(*) 
    FROM information_schema.tables 
    WHERE table_schema = '{schema_name}';
    """)
    
    table_count = cur.fetchone()[0]
    print(f"• {schema_name} ({table_count} tables)")

cur.close()
conn.close()
