from fastapi import Depends
from mypy_boto3_s3 import S3Client
from app.core.s3 import s3

def get_s3_client() -> S3Client:
    return s3
