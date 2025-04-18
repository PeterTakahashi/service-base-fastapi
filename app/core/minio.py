import boto3
import uuid
from fastapi import UploadFile
import os

MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "minio:9000")
MINIO_ACCESS_KEY = os.getenv("MINIO_ROOT_USER", "admin")
MINIO_SECRET_KEY = os.getenv("MINIO_ROOT_PASSWORD", "password")
BUCKET_NAME = "sample"

s3 = boto3.client(
    "s3",
    endpoint_url=f"http://{MINIO_ENDPOINT}",
    aws_access_key_id=MINIO_ACCESS_KEY,
    aws_secret_access_key=MINIO_SECRET_KEY,
)

def upload_image(file: UploadFile) -> str:
    ext = file.filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    s3.upload_fileobj(file.file, BUCKET_NAME, filename, ExtraArgs={"ContentType": file.content_type})
    return f"http://{MINIO_ENDPOINT}/{BUCKET_NAME}/{filename}"
