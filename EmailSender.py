import smtplib
import os
from email.mime.text import MIMEText
from email.header import Header

class EmailSender:
    def __init__(self):
        self.EMAIL = os.environ.get("EMAIL_ADDRESS")
        self.PASSWORD = os.environ.get("EMAIL_PASSWORD")

    def send_email(self, exception):
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            smtp.login(self.EMAIL, self.PASSWORD)

            msg = f"Subject: Law bot error\n\nException: {exception}"
            smtp.sendmail(self.EMAIL, "a.halayonok@gmail.com", msg)
            return "Возвращаюсь с пустыми руками. Что-то пошло не так. Я отправил разработчику письмо и он обязательно разберется с этим."

    def send_new_user_email(self, message):
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            smtp.login(self.EMAIL, self.PASSWORD)

            msg = MIMEText(f'Username: {message.from_user.first_name} {message.from_user.last_name} {message.from_user.id} {message.from_user.username}', 'plain', 'utf-8')
            msg['Subject'] = f"Telegram new user"
            msg['From'] = self.EMAIL
            msg['To'] = "a.halayonok@gmail.com"

            smtp.sendmail(self.EMAIL, "a.halayonok@gmail.com", msg.as_string())