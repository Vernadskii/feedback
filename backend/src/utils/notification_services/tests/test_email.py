from django.test import TestCase

from utils.notification_services.email import EmailSender


class EmailTestCase(TestCase):

    def test_send_email(self):
        to_address = "d.vernadskii@gmail.com"
        subject = "Test Email"
        body = "This is a test email."
        self.assertEqual(True, EmailSender.send_email(to_address, subject, body))
