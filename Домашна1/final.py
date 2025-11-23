import requests
from psycopg2.extras import execute_values

from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from typing import Optional, List

from db_connection import connect_db
import time

COINGECKO_API_BASE = "https://api.coingecko.com/api/v3"
COINGECKO_FRONTEND_BASE = "https://www.coingecko.com"
LOOKBACK_YEARS = 10

@dataclass
class CoinMeta:
    id: str
    symbol: str
    name: str
    market_cap_rank: Optional[int]

def convert_date(ts_ms: float) -> date:
    if ts_ms > 10_000_000_000:
        ts_ms = ts_ms / 1000.0
    dt = datetime.fromtimestamp(ts_ms, tz=timezone.utc)
    return dt.date()


def fetch_markets_page(page: int, per_page: int = 250) -> list[dict]:

    url = f"{COINGECKO_API_BASE}/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": per_page,
        "page": page,
        "sparkline": "false",
    }
    resp = requests.get(url, params=params, timeout=30)
    resp.raise_for_status()
    return resp.json()


def get_cryptocurrencies() -> List[CoinMeta]:

    all_coins: List[CoinMeta] = []

    for page in range(1, 5):
        rows = fetch_markets_page(page=page, per_page=250)
        for row in rows:
            all_coins.append(
                CoinMeta(
                    id=row["id"],
                    symbol=row["symbol"],
                    name=row["name"],
                    market_cap_rank=row.get("market_cap_rank"),
                )
            )

    return all_coins


def build_meta_by_id() -> dict[str, CoinMeta]:
    coins = get_cryptocurrencies()
    return {c.id: c for c in coins}


def fetch_ohlc_data(coin_meta: CoinMeta) -> list[list[float]]:

    numeric_id = coin_meta.market_cap_rank
    url = f"{COINGECKO_FRONTEND_BASE}/ohlc/{numeric_id}/series/usd/max.json"

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept": "application/json, text/plain, */*",
        "Referer": f"{COINGECKO_FRONTEND_BASE}/en/coins/{coin_meta.id}",
    }

    resp = requests.get(url, headers=headers, timeout=60)
    resp.raise_for_status()
    data = resp.json()

    if isinstance(data, dict) and "ohlc" in data:
        return data["ohlc"]
    if isinstance(data, list):
        return data

    raise ValueError(f"Unexpected OHLC JSON format for {coin_meta.id}: {type(data)}")

def fetch_volume_data(coin_meta: CoinMeta) -> dict:

    url = f"{COINGECKO_FRONTEND_BASE}/price_charts/{coin_meta.id}/usd/max.json"

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept": "application/json, text/plain, */*",
        "Referer": f"{COINGECKO_FRONTEND_BASE}/en/coins/{coin_meta.id}",
    }

    resp = requests.get(url, headers=headers, timeout=60)
    resp.raise_for_status()
    return resp.json()


def daily_ohlcv_data(coin_meta: CoinMeta, start_date: date):

    print(f"Fetching OHLC for {coin_meta.id}.")

    ohlc_list = fetch_ohlc_data(coin_meta)


    volumes_by_date = {}
    try:
        stats_json = fetch_volume_data(coin_meta)
        for ts, vol in stats_json.get("total_volumes", []):
            d = convert_date(ts)
            volumes_by_date[d] = vol
        print(f"Loaded {len(volumes_by_date)} volume points for {coin_meta.id}.")
    except Exception as e:
        print(f"Error: Could not fetch volume for {coin_meta.id}: {e}")

    rows = []
    for row in ohlc_list:
        if len(row) < 5:
            continue

        ts, o, h, l, c = row[:5]
        d = convert_date(ts)

        if d < start_date:
            continue

        volume_24h = volumes_by_date.get(d)
        market_cap = None
        liquidity = None

        rows.append(
            (
                coin_meta.id,
                d,
                float(o),
                float(h),
                float(l),
                float(c),
                volume_24h,
                market_cap,
                liquidity,
            )
        )

    rows.sort(key=lambda r: r[1])
    return rows


def save_daily_rows(rows):

    if not rows:
        print("No rows to save.")
        return

    sql = """
    INSERT INTO daily_market_data (
        crypto_id, date,
        open_price, high_price, low_price, close_price,
        volume_24h, market_cap, liquidity
    )
    VALUES %s
    ON CONFLICT (crypto_id, date) DO UPDATE
        SET open_price  = EXCLUDED.open_price,
            high_price  = EXCLUDED.high_price,
            low_price   = EXCLUDED.low_price,
            close_price = EXCLUDED.close_price,
            volume_24h  = COALESCE(EXCLUDED.volume_24h, daily_market_data.volume_24h),
            market_cap  = EXCLUDED.market_cap,
            liquidity   = EXCLUDED.liquidity;
    """

    conn = connect_db()
    cur = conn.cursor()
    execute_values(cur, sql, rows)
    conn.commit()
    cur.close()
    conn.close()
    print(f"Saved {len(rows)} rows to daily_market_data.")


def run_filter2():

    today = date.today()
    ten_years_ago = date(today.year - LOOKBACK_YEARS, today.month, today.day)

    meta_by_id = build_meta_by_id()
    print(f"Filter 2: CoinMeta for {len(meta_by_id)} coins.\n")

    conn = connect_db()
    cur = conn.cursor()

    cur.execute("SELECT id, symbol, name FROM cryptocurrencies;")

    coins = cur.fetchall()
    jobs_for_filter3 = []

    print(f"Filter 2: Processing {len(coins)} coins...")

    for coin_id, symbol, name in coins:
        coin_meta = meta_by_id.get(coin_id)
        if not coin_meta:
            print(f"\nFilter 2: Error: No CoinMeta for {coin_id}, skipping.")
            continue

        cur.execute(
            "SELECT MAX(date) FROM daily_market_data WHERE crypto_id = %s;",
            (coin_id,),
        )
        (last_date,) = cur.fetchone()

        if last_date is None:

            start_date = ten_years_ago
            print(f"\nFilter 2: {coin_id} has NO data, downloading last 10 years from {start_date}...")
            rows = daily_ohlcv_data(coin_meta, start_date)
            save_daily_rows(rows)

            if rows:
                last_date_inserted = rows[-1][1]
                print(f"Latest date inserted for {coin_id}: {last_date_inserted}")
        else:

            start_date = last_date + timedelta(days=1)
            jobs_for_filter3.append(
                {
                    "id": coin_id,
                    "symbol": symbol,
                    "name": name,
                    "last_date": last_date,
                    "start_date": start_date,
                }
            )
            print(
                f"\nFilter 2: {coin_id} has data up to {last_date}, "
                f"next start_date = {start_date}"
            )

    cur.close()
    conn.close()

    return jobs_for_filter3

def run_filter3():

    jobs = run_filter2()

    if not jobs:
        print("Filter 3: No coins need backfill.")
        return


    meta_by_id = build_meta_by_id()
    print(f"Filter 3: CoinMeta for {len(meta_by_id)} coins.\n")


    processed = 0

    for job in jobs:
        coin_id = job["id"]
        start_date = job["start_date"]
        last_date = job["last_date"]

        coin_meta = meta_by_id.get(coin_id)
        if not coin_meta:
            print(f"Filter 3: Error: No CoinMeta for {coin_id}, skipping.")
            continue

        rows = daily_ohlcv_data(coin_meta, start_date)

        if not rows:
            print(f"Filter 3: No new rows for {coin_id} after {last_date}.")
        else:
            save_daily_rows(rows)

        processed += 1


    print(f"\nFilter 3: finished backfill for {processed} coins.")


if __name__ == "__main__":
    start_time = time.perf_counter()
    run_filter2()
    run_filter3()
    end_time = time.perf_counter()
    elapsed = end_time - start_time

    print(f"\nTime: {elapsed} seconds.")

