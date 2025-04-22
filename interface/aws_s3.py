import boto3
import tempfile

from util import logger

log = logger.setup_logger()

def download(bucket_name, object_key, destination):
    log.info(f"Downloading file {object_key}")

    s3_client = boto3.client('s3')
    s3_client.download_file(bucket_name, object_key, destination)

    print(f"File '{object_key}' downloaded from S3 bucket '{bucket_name}' and saved to '{destination}'")

def upload(bucket_name, source_file, object_key):
    log.info(f"Uploading file {object_key}")
    s3_client = boto3.client('s3')
    s3_client.upload_file(source_file, bucket_name, f'public/{object_key}')

    print(f"file '{source_file}' uploaded to '{bucket_name}/{object_key}'")
