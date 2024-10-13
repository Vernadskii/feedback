import logging
import os

import boto3
from botocore.client import Config
from django.core.files.storage import FileSystemStorage

from feedback import settings


# Get an instance of a logger
logger = logging.getLogger(__name__)


class MinioStorage:
    def __init__(self) -> None:
        self.bucket_name = settings.S3_STORAGE_BUCKET_NAME
        self.client = boto3.resource(
            's3',
            endpoint_url=settings.S3_ENDPOINT_URL,
            aws_access_key_id=settings.S3_ACCESS_KEY_ID,
            aws_secret_access_key=settings.S3_SECRET_ACCESS_KEY,
            verify=settings.S3_VERIFY,
            config=Config(signature_version='s3v4'),
        )

    def upload_file(self, file_path, full_path):
        try:  # noqa: WPS229
            bucket = self.client.Bucket(self.bucket_name)
            bucket.upload_file(full_path, file_path)
        except Exception as err:
            logger.error(
                f'error minio uploading file {file_path} {err}',
                extra={'event': 'minio_upload_file'},
            )

    def download_file(self, file_path, full_path):
        try:  # noqa: WPS229
            bucket = self.client.Bucket(self.bucket_name)
            bucket.download_file(file_path, full_path)
        except Exception as err:
            logger.error(
                f'error minio downloading file {file_path} {err}',
                extra={'event': 'minio_download_file'},
            )

    @staticmethod
    def get_file_path(file_path) -> str:
        return f'{settings.S3_ENDPOINT_URL}/{settings.S3_STORAGE_BUCKET_NAME}/{file_path}'

    @staticmethod
    def get_proxy_file_path(file_path) -> str:
        path_parts = file_path.split('/')
        file_name = path_parts.pop()
        api = settings.URLS['API']
        view_name = 's3-media'
        # TODO: add reverse?
        return f"{api}{view_name}/{'/'.join(path_parts)}/{file_name}"  # noqa: WPS237, WPS221


class S3ProxyFileSystemStorage(FileSystemStorage):
    @staticmethod
    def download_file(file_path) -> None:
        dir_name = file_path.split('/')[-2]
        full_path = f"{settings.MEDIA_ROOT}/{dir_name}/"
        if not os.path.exists(os.path.dirname(full_path)):
            os.makedirs(os.path.dirname(full_path))

        MinioStorage().download_file(file_path, full_path + file_path.split('/')[-1])  # noqa: WPS221

    def get_available_name(self, name, max_length=None):
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name

    def _save(self, name, content) -> str:
        file_name = super()._save(name, content)
        MinioStorage().upload_file(name, f"{settings.MEDIA_ROOT}/{name}")
        return file_name
