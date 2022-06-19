import uuid
import time_uuid

from app.storage.connection import s3
from app.database.schemas.inbox import InboxCreate


def create_bucket(bucket):
    if s3.Bucket(bucket) not in s3.buckets.all():
        s3.create_bucket(Bucket=bucket)
    return bucket


def retrieve_uuid():
    return uuid.uuid1()


def retrieve_datetime_from_uuid(id):
    return time_uuid.TimeUUID(bytes=id.bytes).get_datetime()


def save_files(files, format_bucket='%Y%m%d', formate_file='jpg'):
    results = []

    for file in files:
        object_uuid = retrieve_uuid()
        object_timestamp = retrieve_datetime_from_uuid(object_uuid)

        filename = f'{object_uuid}.{formate_file}'

        bucket = create_bucket(object_timestamp.strftime(format_bucket))
        s3.Bucket(bucket).upload_fileobj(file.file, filename)

        results.append(InboxCreate(filename=filename, timestamp=object_timestamp))

    return results


def delete_file(inbox, format_bucket='%Y%m%d'):
    check = False

    bucket = inbox.timestamp.strftime(format_bucket)
    active = s3.Bucket(bucket).delete_objects(Delete={'Objects': [{'Key': inbox.filename}]})

    if active['ResponseMetadata']['HTTPStatusCode'] == 200:
        check = True

    return check

