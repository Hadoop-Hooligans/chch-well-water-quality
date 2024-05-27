import boto3
from botocore import UNSIGNED
from botocore.client import Config
import os
import logging
from botocore.exceptions import ClientError
from dotenv import dotenv_values


def download_file_s3(file_name):
    config = dotenv_values()
    bucket_name = config['BUCKET_NAME']
    object_name = os.path.basename(file_name)
    s3 = boto3.client('s3', config=Config(signature_version=UNSIGNED))
    s3.download_file(bucket_name, object_name, file_name)

