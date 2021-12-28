import boto3
from botocore.client import BaseClient

from app.database.database import SessionLocal
from app.config import settings


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def s3_auth() -> BaseClient:
    s3 = boto3.client(service_name='s3',
                      endpoint_url=settings.MINIO_URI,
                      aws_access_key_id=settings.ACCESS_KEY_ID,
                      aws_secret_access_key=settings.SECRET_ACCESS_KEY
                      )

    return s3
