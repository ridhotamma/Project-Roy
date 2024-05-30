import boto3
from fastapi import status
from fastapi.exceptions import HTTPException
from botocore.exceptions import NoCredentialsError
from app.config import (
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
    AWS_REGION,
    AWS_S3_BUCKET_NAME,
    AWS_CLOUDFRONT_DOMAIN_NAME,
)


def upload_to_s3(file_name, object_name=None):

    if object_name is None:
        object_name = file_name

    s3_client = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION,
    )

    try:
        s3_client.upload_file(file_name, AWS_S3_BUCKET_NAME, object_name)
    except FileNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "status_code": status.HTTP_404_NOT_FOUND,
                "message": "[S3 Upload] File Not found",
            },
        )
    except NoCredentialsError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "status_code": status.HTTP_404_NOT_FOUND,
                "message": "[S3 Upload] Credentials Is not Provided",
            },
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "status_code": status.HTTP_404_NOT_FOUND,
                "message": f"[S3 Upload] Unexpected Error: {e}",
            },
        )

    cloudfront_url = f"{AWS_CLOUDFRONT_DOMAIN_NAME}/{object_name}"
    return cloudfront_url
