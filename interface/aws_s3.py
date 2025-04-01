import boto3
import tempfile

from util import logger

log = logger.setup_logger()

class AwsS3: 
    def __init__(self, bucket_name):
        self.s3_client = boto3.client('s3')
        self.bucket_name = bucket_name
        
    def download(self, object_key, destination):
        log.info(f"Downloading file {object_key}")
        self.s3_client.download_file(self.bucket_name, object_key, destination)

        print(f"File '{object_key}' downloaded from S3 bucket '{self.bucket_name}' and saved to '{destination}'")

    def upload(self, source_file, object_key):
        log.info(f"Uploading file {object_key}")
        self.s3_client.upload_file(source_file, self.bucket_name, object_key)

        print(f"file '{source_file}' uploaded to '{self.bucket_name}/{object_key}'")
