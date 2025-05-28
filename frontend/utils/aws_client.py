import os
import boto3
import streamlit as st
from typing import Optional
from dotenv import load_dotenv
load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
REGION_NAME = os.getenv("AWS_DEFAULT_REGION", "eu-central-1")
KNOWLEDGE_BASE_ID = os.getenv("KNOWLEDGE_BASE_ID", "")
S3_BUCKET = os.getenv("S3_BUCKET", "")


class AWSClient:
    def __init__(self):
        self._init_clients()

    def _init_clients(self):
        self.bedrock_client = boto3.client(
            'bedrock-agent-runtime',
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name=REGION_NAME
        )

        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name=REGION_NAME
        )

    def upload_to_s3(self, file, filename: str) -> Optional[str]:
        try:
            self.s3_client.upload_fileobj(file, S3_BUCKET, filename)
            return f"s3://{S3_BUCKET}/{filename}"
        except boto3.exceptions.S3UploadFailedError as e:
            st.error(f"S3 upload failed: {e}")
        except Exception as e:
            st.error(f"An unexpected error occurred during S3 upload: {e}")
        return None

    def check_aws_connection(self) -> bool:
        try:
            self.s3_client.head_bucket(Bucket=S3_BUCKET)
            return True
        except boto3.exceptions.Boto3Error as e:
            st.error(f"Failed to connect to AWS S3: {e}")
        except Exception as e:
            st.error(f"An unexpected error occurred while checking AWS connection: {e}")
        return False