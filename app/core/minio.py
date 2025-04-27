import boto3
import uuid
from fastapi import UploadFile
import os

MINIO_ENDPOINT: str = os.getenv("MINIO_ENDPOINT", "minio:9000")
MINIO_ACCESS_KEY: str = os.getenv("MINIO_ROOT_USER", "admin")
MINIO_SECRET_KEY: str = os.getenv("MINIO_ROOT_PASSWORD", "password")
BUCKET_NAME: str = os.getenv("MINIO_BUCKET_NAME", "manga-translator")

s3 = boto3.client(
    "s3",
    endpoint_url=f"http://{MINIO_ENDPOINT}",
    aws_access_key_id=MINIO_ACCESS_KEY,
    aws_secret_access_key=MINIO_SECRET_KEY,
)
