from botocore.client import BaseClient
from fastapi import APIRouter, Depends

from app.dependencies import s3_auth

router = APIRouter()


@router.get("/files")
def get_buckets(s3: BaseClient = Depends(s3_auth)):
    response = s3.list_buckets()

    return response['Buckets']
