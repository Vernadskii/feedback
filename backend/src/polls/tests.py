import os
import tempfile

from django.test import TestCase

from polls.utils.storage import MinioStorage


class MinioStorageIntegrationTestCase(TestCase):

    def setUp(self):
        # Create a temporary file for testing
        self.test_file = tempfile.NamedTemporaryFile(delete=False)
        self.test_file.write(b'This is a test file.')
        self.test_file.close()

        # Initialize the MinioStorage instance
        self.storage = MinioStorage()

        # Ensure the test bucket exists
        self.storage.client.create_bucket(Bucket=self.storage.bucket_name)

    def tearDown(self):
        # Clean up the test file
        os.remove(self.test_file.name)

        # Optionally, clean up the bucket
        self.storage.client.Bucket(self.storage.bucket_name).objects.all().delete()
        self.storage.client.Bucket(self.storage.bucket_name).delete()

    def test_upload_file(self):
        file_path = 'uploads/test_file.txt'
        full_path = self.test_file.name

        # Act: Upload the file
        self.storage.upload_file(file_path, full_path)

        # Assert: Check if the file exists in the bucket
        objects = list(self.storage.client.Bucket(self.storage.bucket_name).objects.filter(Prefix='uploads/'))
        self.assertTrue(any(obj.key == file_path for obj in objects))

    def test_download_file(self):
        file_path = 'uploads/test_file.txt'
        full_path = self.test_file.name

        # First, upload the file
        self.storage.upload_file(file_path, full_path)

        # Act: Download the file to a new location
        download_path = tempfile.NamedTemporaryFile(delete=False).name
        self.storage.download_file(file_path, download_path)

        # Assert: Check if the downloaded file matches the original
        with open(download_path, 'rb') as f:
            downloaded_content = f.read()

        with open(self.test_file.name, 'rb') as f:
            original_content = f.read()

        self.assertEqual(downloaded_content, original_content)

        # Clean up the downloaded file
        os.remove(download_path)
