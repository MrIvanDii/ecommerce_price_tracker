import psycopg2
import psycopg2.extras
from flask import Flask, render_template
import os

app = Flask(__name__)

DATABASE_URL = os.environ.get("DATABASE_URL")


def query_db(sql: str) -> list[dict]:
    conn = None
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(sql)
        return cursor.fetchall()
    except Exception as e:
        print(f"DB error: {e}")
        return []
    finally:
        if conn:
            conn.close()


@app.route("/")
def dashboard():
    latest = query_db("""
        SELECT dealer, product_name_clean, coin_family, weight,
               year, price, price_per_oz, currency, availability
        FROM price_latest
        ORDER BY coin_family, weight, price
    """)

    best = query_db("""
        SELECT coin_family, weight, best_price, best_price_per_oz,
               dealer, product_name_clean, year, currency
        FROM price_best
        ORDER BY coin_family, weight
    """)

    spread = query_db("""
        SELECT
            coin_family,
            weight,
            MIN(price) as min_price,
            MAX(price) as max_price,
            ROUND(CAST(MAX(price) - MIN(price) AS NUMERIC), 2) as spread,
            COUNT(DISTINCT dealer) as dealer_count
        FROM price_latest
        GROUP BY coin_family, weight
        HAVING COUNT(DISTINCT dealer) > 1
        ORDER BY spread DESC
    """)

    last_updated = query_db("""
        SELECT MAX(timestamp) as ts FROM price_latest
    """)
    last_updated = last_updated[0]["ts"] if last_updated else None

    return render_template(
        "dashboard.html",
        latest=latest,
        best=best,
        spread=spread,
        last_updated=last_updated,
    )


if __name__ == "__main__":
    app.run(debug=True)