import boto3
from botocore import UNSIGNED
from botocore.client import Config
import os
import logging
from botocore.exceptions import ClientError
from dotenv import dotenv_values



def upload_file_s3(file_name):
    """
    Upload a file to an S3 bucket
    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """
    config = dotenv_values()
    bucket_name = config['BUCKET_NAME']
    object_name = os.path.basename(file_name)
    s3 = boto3.client('s3', config=Config(signature_version=UNSIGNED))
    try:
        response = s3.upload_file(file_name, bucket_name, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

