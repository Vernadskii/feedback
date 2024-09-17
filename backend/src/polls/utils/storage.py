import os

import boto3
from django.core.files.storage import FileSystemStorage

from botocore.client import Config
from django.urls import reverse

from feedback import settings

import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


class MinioStorage:
    def __init__(self):
        self.bucket_name = settings.S3_STORAGE_BUCKET_NAME
        self.client = boto3.resource(
            's3',
            endpoint_url=settings.S3_ENDPOINT_URL,
            aws_access_key_id=settings.S3_ACCESS_KEY_ID,
            aws_secret_access_key=settings.S3_SECRET_ACCESS_KEY,
            verify=settings.S3_VERIFY,
            config=Config(signature_version='s3v4')
        )

    def upload_file(self, file_path, full_path):
        try:
            bucket = self.client.Bucket(self.bucket_name)
            bucket.upload_file(full_path, file_path)
        except Exception as err:
            logger.error(
                f'error minio uploading file {file_path} {err}',
                extra={'event': 'minio_upload_file'}
            )

    def download_file(self, file_path, full_path):
        try:
            bucket = self.client.Bucket(self.bucket_name)
            bucket.download_file(file_path, full_path)
        except Exception as err:
            logger.error(
                f'error minio downloading file {file_path} {err}',
                extra={'event': 'minio_download_file'}
            )

    @staticmethod
    def get_file_path(file_path):
        return '%s/%s/%s' % (settings.S3_ENDPOINT_URL, settings.S3_STORAGE_BUCKET_NAME, file_path)

    @staticmethod
    def get_proxy_file_path(file_path):
        path_parts = file_path.split('/')
        file_name = path_parts.pop()
        api = settings.URLS['API']
        view_name = 's3-media'
        # TODO: add reverse?
        return f"{api}{view_name}/{'/'.join(path_parts)}/{file_name}"


class S3ProxyFileSystemStorage(FileSystemStorage):
    @staticmethod
    def download_file(file_path):
        dir_name = file_path.split('/')[-2]
        full_path = settings.MEDIA_ROOT + '/' + dir_name + '/'
        if not os.path.exists(os.path.dirname(full_path)):
            os.makedirs(os.path.dirname(full_path))

        MinioStorage().download_file(file_path, full_path + file_path.split('/')[-1])

    def _save(self, name, content):
        file_name = super()._save(name, content)
        MinioStorage().upload_file(name, settings.MEDIA_ROOT + '/' + name)
        return file_name

    def get_available_name(self, name, max_length=None):
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name
