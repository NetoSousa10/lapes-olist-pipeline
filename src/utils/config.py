import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PG_USER = os.getenv("POSTGRES_USER", "admin")
    PG_PASSWORD = os.getenv("POSTGRES_PASSWORD", "admin")
    PG_DB = os.getenv("POSTGRES_DB", "datalake")
    PG_HOST = os.getenv("POSTGRES_HOST", "postgres")
    PG_PORT = int(os.getenv("POSTGRES_PORT", 5432))

    MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "http://minio:9000")
    MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "admin")
    MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "admin123")
    MINIO_BUCKET = os.getenv("MINIO_BUCKET", "datalake")

settings = Settings()
