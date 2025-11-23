import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def connect_db():
    return psycopg2.connect(
        host=os.getenv("PG_HOST"),
        port=os.getenv("PG_PORT"),
        user=os.getenv("PG_USER"),
        password=os.getenv("PG_PASSWORD"),
        dbname=os.getenv("PG_DB"),
    )

def init_schema():
    create_cryptocurrency = """
    CREATE TABLE IF NOT EXISTS cryptocurrencies (
        id TEXT PRIMARY KEY,
        symbol TEXT NOT NULL,
        name TEXT NOT NULL
    );
    """

    create_daily_data = """
    CREATE TABLE IF NOT EXISTS daily_market_data (
        id BIGSERIAL PRIMARY KEY,
        crypto_id TEXT NOT NULL REFERENCES cryptocurrencies(id),
        date DATE NOT NULL,
        open_price DOUBLE PRECISION,
        high_price DOUBLE PRECISION,
        low_price DOUBLE PRECISION,
        close_price DOUBLE PRECISION,
        volume_24h DOUBLE PRECISION,
        market_cap DOUBLE PRECISION,
        liquidity DOUBLE PRECISION,
        UNIQUE (crypto_id, date)
    );
    """

    conn = connect_db()
    cur = conn.cursor()
    cur.execute(create_cryptocurrency)
    cur.execute(create_daily_data)
    conn.commit()
    cur.close()
    conn.close()

    print("Tables created successfully.")

if __name__ == "__main__":
    init_schema()
