from django.test import TestCase

from feedback import settings
from utils.notification_services.email import EmailSender


class EmailTestCase(TestCase):

    def test_send_email(self):
        subject = "Test Email"
        body = "This is a test email."
        self.assertEqual(True, EmailSender.send_email(settings.EMAIL_ADDRESS, subject, body))
