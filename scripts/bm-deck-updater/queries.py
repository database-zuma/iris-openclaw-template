"""
BM Deck Updater — SQL Queries
Returns fresh data for each branch.
"""

import psycopg2
from datetime import datetime, date
import calendar


def get_connection(db_url):
    return psycopg2.connect(db_url)


def get_current_period():
    """Returns current year, current month, days elapsed, days in month."""
    today = date.today()
    days_in_month = calendar.monthrange(today.year, today.month)[1]
    return today.year, today.month, today.day, days_in_month


def get_store_revenue(conn, stores, year, month):
    """Revenue per store for a given year/month."""
    store_list = ", ".join(f"'{s}'" for s in stores)
    with conn.cursor() as cur:
        cur.execute(f"""
            SELECT
                matched_store_name,
                SUM(CASE WHEN EXTRACT(YEAR FROM transaction_date)={year}
                              AND EXTRACT(MONTH FROM transaction_date)=1
                         THEN quantity * unit_price ELSE 0 END) AS rev_jan,
                SUM(CASE WHEN EXTRACT(YEAR FROM transaction_date)={year}
                              AND EXTRACT(MONTH FROM transaction_date)=2
                         THEN quantity * unit_price ELSE 0 END) AS rev_feb,
                SUM(CASE WHEN EXTRACT(YEAR FROM transaction_date)={year-1}
                              AND EXTRACT(MONTH FROM transaction_date)=1
                         THEN quantity * unit_price ELSE 0 END) AS rev_jan_ly,
                SUM(CASE WHEN EXTRACT(YEAR FROM transaction_date)={year-1}
                              AND EXTRACT(MONTH FROM transaction_date)=2
                         THEN quantity * unit_price ELSE 0 END) AS rev_feb_ly
            FROM core.sales_with_product
            WHERE is_intercompany = FALSE
              AND LOWER(matched_store_name) IN ({store_list})
              AND EXTRACT(YEAR FROM transaction_date) IN ({year}, {year-1})
            GROUP BY matched_store_name
            ORDER BY rev_jan DESC
        """)
        return cur.fetchall()


def get_store_targets(conn, stores, year):
    """Monthly targets per store from portal.store_monthly_target."""
    store_list = ", ".join(f"'{s}'" for s in stores)
    with conn.cursor() as cur:
        cur.execute(f"""
            SELECT store_name, jan, feb, mar, apr, may, jun,
                   jul, aug, sep, oct, nov, dec
            FROM portal.store_monthly_target
            WHERE year = {year}
              AND LOWER(TRIM(store_name)) IN ({store_list})
        """)
        return cur.fetchall()


def get_ff_fa_fs(conn, stores):
    """Latest FF/FA/FS per store from mart.ff_fa_fs_daily."""
    store_list = ", ".join(f"'{s}'" for s in stores)
    with conn.cursor() as cur:
        cur.execute(f"""
            SELECT DISTINCT ON (store_name)
                store_name,
                ff_pct,
                fa_pct,
                fs_pct,
                snapshot_date
            FROM mart.ff_fa_fs_daily
            WHERE LOWER(store_name) IN ({store_list})
            ORDER BY store_name, snapshot_date DESC
        """)
        return cur.fetchall()


def get_bcg_series(conn, stores, year):
    """Series-level BCG data for the branch: volume + YoY growth."""
    store_list = ", ".join(f"'{s}'" for s in stores)
    with conn.cursor() as cur:
        cur.execute(f"""
            SELECT
                series,
                SUM(CASE WHEN EXTRACT(YEAR FROM transaction_date)={year}
                              AND EXTRACT(MONTH FROM transaction_date) IN (1,2)
                         THEN quantity ELSE 0 END) AS ytd_now,
                SUM(CASE WHEN EXTRACT(YEAR FROM transaction_date)={year-1}
                              AND EXTRACT(MONTH FROM transaction_date) IN (1,2)
                         THEN quantity ELSE 0 END) AS ytd_last,
                ROUND((
                    SUM(CASE WHEN EXTRACT(YEAR FROM transaction_date)={year}
                                  AND EXTRACT(MONTH FROM transaction_date) IN (1,2)
                             THEN quantity ELSE 0 END)::numeric /
                    NULLIF(SUM(CASE WHEN EXTRACT(YEAR FROM transaction_date)={year-1}
                                        AND EXTRACT(MONTH FROM transaction_date) IN (1,2)
                                   THEN quantity ELSE 0 END), 0) - 1
                ) * 100, 1) AS yoy_pct
            FROM core.sales_with_product
            WHERE is_intercompany = FALSE
              AND series IS NOT NULL
              AND LOWER(matched_store_name) IN ({store_list})
              AND EXTRACT(YEAR FROM transaction_date) IN ({year}, {year-1})
            GROUP BY series
            HAVING SUM(CASE WHEN EXTRACT(YEAR FROM transaction_date)={year}
                                AND EXTRACT(MONTH FROM transaction_date) IN (1,2)
                           THEN quantity ELSE 0 END) > 50
            ORDER BY ytd_now DESC
        """)
        return cur.fetchall()


def get_top_products(conn, stores, year):
    """Top 10 articles by qty in branch YTD."""
    store_list = ", ".join(f"'{s}'" for s in stores)
    with conn.cursor() as cur:
        cur.execute(f"""
            SELECT
                product_name,
                series,
                SUM(CASE WHEN EXTRACT(YEAR FROM transaction_date)={year}
                              AND EXTRACT(MONTH FROM transaction_date) IN (1,2)
                         THEN quantity ELSE 0 END) AS qty,
                SUM(CASE WHEN EXTRACT(YEAR FROM transaction_date)={year}
                              AND EXTRACT(MONTH FROM transaction_date) IN (1,2)
                         THEN quantity * unit_price ELSE 0 END) AS rev
            FROM core.sales_with_product
            WHERE is_intercompany = FALSE
              AND product_name IS NOT NULL
              AND LOWER(matched_store_name) IN ({store_list})
              AND EXTRACT(YEAR FROM transaction_date) = {year}
              AND EXTRACT(MONTH FROM transaction_date) IN (1,2)
            GROUP BY product_name, series
            ORDER BY qty DESC
            LIMIT 10
        """)
        return cur.fetchall()
