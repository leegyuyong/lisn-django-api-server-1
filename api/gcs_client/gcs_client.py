from google.cloud import storage
from django.conf import settings
import datetime

def upload_file_to_gcs(file_object, object_name):
    try:
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(settings.GCS_BUCKET)
        blob = storage.Blob(object_name, bucket)
        blob.upload_from_file(file_object)
    except:
        return False
    return True

def delete_file_to_gcs(object_name):
    try:
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(settings.GCS_BUCKET)
        bucket.delete_blob(object_name)
    except:
        return False
    return True

def create_presigned_url_gcs(object_name):
    try:
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(settings.GCS_BUCKET)
        blob = storage.Blob(object_name, bucket)
        url = blob.generate_signed_url(expiration=datetime.timedelta(hours=6))
    except:
        return ''
    return url

def copy_file_to_gcs(src_object_name, dest_object_name):
    try:
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(settings.GCS_BUCKET)
        blob = storage.Blob(src_object_name, bucket)
        bucket.copy_blob(blob, bucket, dest_object_name)
    except:
        return False
    return True