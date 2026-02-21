
import psycopg2
import csv
import os

# Database connection details
db_config = {
    "host": "76.13.194.120",
    "port": "5432",
    "dbname": "openclaw_ops",
    "user": "openclaw_app",
    "password": "Zuma-0psCl4w-2026!"
}

# SQL Query
sql_query = """
SELECT
  store_name AS "Nama Toko",
  DATE_TRUNC('month', transaction_date)::date AS "Bulan",
  SUM(qty) AS "Total Qty (Pairs)",
  SUM(total_revenue_after_discount) AS "Total Revenue"
FROM
  public.sales_summary_plano
WHERE
  store_name ILIKE '%Nagoya Hills%'
  AND transaction_date >= '2026-01-01' AND transaction_date < '2026-02-21'
GROUP BY
  "Nama Toko", "Bulan"
ORDER BY
  "Bulan";
"""

# Output file path
output_path = os.path.expanduser("~/.openclaw/workspace/outbox/sales_nagoya_hills_ftz.csv")
os.makedirs(os.path.dirname(output_path), exist_ok=True)


try:
    # Connect to the database
    conn = psycopg2.connect(**db_config)
    cur = conn.cursor()

    # Execute the query
    cur.execute(sql_query)
    rows = cur.fetchall()
    
    # Get header from cursor description
    header = [desc[0] for desc in cur.description]

    # Write to CSV
    with open(output_path, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(header)
        csv_writer.writerows(rows)

    print(f"SUCCESS: Data successfully exported to {output_path}")

except Exception as e:
    print(f"ERROR: {e}")

finally:
    # Close the connection
    if 'conn' in locals() and conn is not None:
        cur.close()
        conn.close()

