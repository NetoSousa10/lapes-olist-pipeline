import os
import polars as pl
import sqlalchemy as sa
from src.utils.config import settings

BRONZE_DIR = "./bronze/olist"

# Mapeamento de arquivos para tabelas English-named
MAP_TABLE = {
    "olist_orders_dataset":        "bronze.orders",
    "olist_order_items_dataset":   "bronze.order_items",
    "olist_order_payments_dataset": "bronze.order_payments",
    "olist_order_reviews_dataset": "bronze.order_reviews",
    "olist_customers_dataset":     "bronze.customers",
    "olist_sellers_dataset":       "bronze.sellers",
    "olist_products_dataset":      "bronze.products",
    "olist_geolocation_dataset":   "bronze.geolocation",
}

def main():
    engine = sa.create_engine(
        f"postgresql+psycopg://{settings.PG_USER}:"
        f"{settings.PG_PASSWORD}@{settings.PG_HOST}:"
        f"{settings.PG_PORT}/{settings.PG_DB}"
    )

    # 1) Truncate Bronze tables for idempotency
    with engine.begin() as conn:
        conn.execute(sa.text("""
            TRUNCATE TABLE
                bronze.orders,
                bronze.order_items,
                bronze.order_payments,
                bronze.order_reviews,
                bronze.customers,
                bronze.sellers,
                bronze.products,
                bronze.geolocation
            RESTART IDENTITY;
        """))
        print("Truncated Bronze tables")

    # 2) Load Parquet files into Bronze
    with engine.begin() as conn:
        for file in os.listdir(BRONZE_DIR):
            if not file.endswith(".parquet"):
                continue
            key = file.replace(".parquet", "")
            if key not in MAP_TABLE:
                print(f"Ignored: {file}")
                continue

            schema, table = MAP_TABLE[key].split('.')
            df = pl.read_parquet(os.path.join(BRONZE_DIR, file)).to_pandas()
            df.to_sql(table, conn, schema=schema, if_exists="append", index=False)
            print(f"Loaded into {schema}.{table}: {len(df)} records")

    # 3) Copy Bronze -> Silver for orders (example)
    with engine.begin() as conn:
        conn.execute(sa.text("""
            INSERT INTO silver.orders_raw
            SELECT * FROM bronze.orders
            ON CONFLICT DO NOTHING;
        """))
        print("Copied bronze.orders -> silver.orders_raw")

if __name__ == "__main__":
    main()
