import smtplib

from feedback.settings import EMAIL_USERNAME, EMAIL_PASSWORD, EMAIL_ADDRESS


class EmailSender:

    @staticmethod
    def send_email(dest_email, subject, content):
        server = smtplib.SMTP('smtp.yandex.ru', 587)
        server.ehlo()  # Кстати, зачем это?
        server.starttls()
        server.login(EMAIL_USERNAME, EMAIL_PASSWORD)

        email_text = 'Text'
        message = 'From: %s\nTo: %s\nSubject: %s\n\n%s' % (EMAIL_USERNAME, dest_email, subject, email_text)

        server.set_debuglevel(1)  # Необязательно; так будут отображаться данные с сервера в консоли
        server.sendmail(EMAIL_ADDRESS, dest_email, message)
        server.quit()
