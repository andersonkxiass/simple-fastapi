from pydantic import BaseSettings
import os


class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URI: str = os.getenv("SQLALCHEMY_DATABASE_URI",
                                             "postgresql://postgres:postgres@127.0.0.1:5432/test")
    MINIO_URI: str = os.getenv("MINIO_URI", "http://localhost:9000")
    ACCESS_KEY_ID: str = os.getenv("ACCESS_KEY_ID", "minio")
    SECRET_ACCESS_KEY: str = os.getenv("ACCESS_KEY_ID", "minio123")


settings = Settings()
