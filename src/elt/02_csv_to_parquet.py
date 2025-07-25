import glob, os
import polars as pl

LANDING = "./landing/olist"
BRONZE_DIR = "./bronze/olist"

def main():
    os.makedirs(BRONZE_DIR, exist_ok=True)
    for csv_file in glob.glob(os.path.join(LANDING, "*.csv")):
        name = os.path.basename(csv_file).replace(".csv", "")
        df = pl.read_csv(csv_file, try_parse_dates=True)
        out_path = os.path.join(BRONZE_DIR, f"{name}.parquet")
        df.write_parquet(out_path)
        print(f"{name}.csv → {name}.parquet")

if __name__ == "__main__":
    main()
