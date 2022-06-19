import os

from boto3.session import Session

aws_access_key_id = os.getenv('S3_USER')
aws_secret_access_key = os.getenv('S3_PASSWORD')
endpoint_url = os.getenv('S3_ENDPOINT_URL')

session = Session(aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
s3 = session.resource('s3', endpoint_url=endpoint_url)