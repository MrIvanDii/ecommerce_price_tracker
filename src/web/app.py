import psycopg2
import psycopg2.extras
from flask import Flask, render_template
import os
from collections import defaultdict

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
    rows = query_db("""
        SELECT
            coin_family,
            weight,
            year,
            dealer,
            MIN(price) as price
        FROM price_latest
        WHERE coin_family IS NOT NULL
        GROUP BY coin_family, weight, year, dealer
        ORDER BY coin_family, weight, year, dealer
    """)

    dealers = ['ukbullion', 'atkinsons', 'acl', 'royalmint']

    family_order = [
        'britannia', 'sovereign', 'krugerrand',
        'queens_beast', 'tudor_beast', 'st_george',
        'lion_eagle', 'buffalo', 'koala', 'other'
    ]

    pivot = defaultdict(lambda: defaultdict(dict))
    for r in rows:
        family = r['coin_family'] or 'other'
        key = (r['weight'], r['year'])
        pivot[family][key][r['dealer']] = r['price']

    def family_sort(f):
        if f is None:
            return 100
        return family_order.index(f) if f in family_order else 99

    pivot_sorted = {
        f: dict(sorted(pivot[f].items(), key=lambda x: (x[0][0] or '', x[0][1] or '')))
        for f in sorted(pivot.keys(), key=family_sort)
    }

    # Конвертируем в float и считаем min_price per row
    min_prices = {}
    for family, rows_data in pivot_sorted.items():
        for key, dealer_prices in rows_data.items():
            prices = []
            for d in dealer_prices:
                if dealer_prices[d] is not None:
                    dealer_prices[d] = float(dealer_prices[d])
                    prices.append(dealer_prices[d])
            min_prices[(family, key)] = min(prices) if prices else None

    last_updated = query_db("SELECT MAX(timestamp) as ts FROM price_latest")
    last_updated = last_updated[0]["ts"] if last_updated else None

    return render_template(
        "dashboard.html",
        pivot=pivot_sorted,
        dealers=dealers,
        min_prices=min_prices,
        last_updated=last_updated,
    )


if __name__ == "__main__":
    app.run(debug=True)