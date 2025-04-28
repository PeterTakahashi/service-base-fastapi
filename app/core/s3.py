import boto3
import uuid
from fastapi import UploadFile
import os

S3_ENDPOINT: str = os.getenv("S3_ENDPOINT", "s3.amazonaws.com")
S3_ACCESS_KEY: str = os.getenv("S3_ACCESS_KEY", "admin")
S3_SECRET_KEY: str = os.getenv("S3_SECRET_KEY", "password")
BUCKET_NAME: str = os.getenv("S3_BUCKET_NAME", "manga-translator-dev")

s3 = boto3.client(
    "s3",
    endpoint_url=f"https://{S3_ENDPOINT}",
    aws_access_key_id=S3_ACCESS_KEY,
    aws_secret_access_key=S3_SECRET_KEY,
)

def generate_s3_object_key(table_name: str, display_id: str, column_name: str, extension: str = "jpg") -> str:
    """
    S3に保存するオブジェクトキーを生成する
    例: users/1234/avatar.jpg
    """
    return f"{table_name}/{display_id}/{column_name}.{extension}"

# upload_file_to_s3 and return storege key
def upload_file_to_s3(file: UploadFile, object_key) -> str:
    """
    Upload a file to s3 and return the storage key.
    """
    # Generate a unique object key
    # object_key = f"{table_name}/{display_id}/{column_name}.{file.filename.split('.')[-1]}"
    # Upload the file to s3
    s3.upload_fileobj(file.file, BUCKET_NAME, object_key)
    return object_key

def delete_file_from_s3(object_key: str) -> None:
    """
    Delete a file from s3.
    """
    try:
        s3.delete_object(Bucket=BUCKET_NAME, Key=object_key)
    except Exception as e:
        print(f"Error deleting file from S3: {e}")
        raise e
    return None

def get_file_url(object_key: str) -> str:
    """
    Get the file URL from s3.
    """
    try:
        url = s3.generate_presigned_url(
            'get_object',
            Params={'Bucket': BUCKET_NAME, 'Key': object_key},
            ExpiresIn=3600  # URL expiration time in seconds
        )
    except Exception as e:
        print(f"Error generating presigned URL: {e}")
        raise e
    return url
