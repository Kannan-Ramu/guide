from storages.backends.s3boto3 import S3Boto3Storage


class DocStorage(S3Boto3Storage):
    bucket_name = 'django-guide-project-new'


class MediaStorage(S3Boto3Storage):
    bucket_name = 'django-guide-project-new'
    # location = 'videos'
