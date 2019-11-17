import boto3

from django.conf import settings

def upload_file_to_s3(file_object, object_name):
    bucket = settings.AWS_S3_BUCKET
    s3_client = boto3.client('s3')
    try:
        s3_client.upload_fileobj(file_object, bucket, object_name)
    except:
        return False
    return True

def delete_file_to_s3(object_name):
    bucket = settings.AWS_S3_BUCKET
    s3_client = boto3.client('s3')
    try:
        s3_client.delete_object(Bucket=bucket, Key=object_name)
    except:
        return False
    return True

def create_presigned_url_s3(object_name, expiration=21600):
    bucket = settings.AWS_S3_BUCKET
    s3_client = boto3.client('s3')
    try:
        url = s3_client.generate_presigned_url('get_object', Params={'Bucket': bucket, 'Key': object_name}, ExpiresIn=expiration)
    except:
        return ''
    return url

def copy_file_to_s3(src_object_name, dest_object_name):
    bucket = settings.AWS_S3_BUCKET
    s3_client = boto3.client('s3')

    copy_source = {'Bucket': bucket, 'Key': src_object_name}
    try:
        s3_client.copy_object(CopySource=copy_source, Bucket=bucket, Key=dest_object_name)
    except:
        return False
    return True