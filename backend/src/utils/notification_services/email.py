import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from feedback.settings import EMAIL_PASSWORD, EMAIL_ADDRESS


class EmailSender:

    @staticmethod
    def send_email(sent_to: str, subject: str, content: str):
        smtpserver = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtpserver.ehlo()
        smtpserver.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

        # Создание сообщения
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = sent_to
        msg['Subject'] = subject

        # Добавление текста сообщения
        msg.attach(MIMEText(content, 'plain'))

        try:
            smtpserver.sendmail(EMAIL_ADDRESS, sent_to, msg.as_string())  # Отправка письма
        except Exception as ex:
            print(f"Failed to send email: {ex}")
            return False
        finally:
            smtpserver.close()  # Закрытие соединения

        return True
