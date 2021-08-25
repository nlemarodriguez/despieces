from abc import ABC

from storages.backends.s3boto3 import S3Boto3Storage


class StaticStorage(S3Boto3Storage, ABC):
    location = 'static'
    default_acl = 'public-read'


class PublicMediaStorage(S3Boto3Storage, ABC):
    location = 'media'
    default_acl = 'public-read'
    file_overwrite = False
