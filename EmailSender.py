import smtplib
import os

class EmailSender:
    def __init__(self):
        self.EMAIL = os.environ.get("EMAIL_ADDRESS")
        self.PASSWORD = os.environ.get("EMAIL_PASSWORD")

    def send_email(self, exception, message):
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            smtp.login(self.EMAIL, self.PASSWORD)

            msg = f"Subject: Law bot error\n\nException: {exception}\n Message: {message}"
            smtp.sendmail(self.EMAIL, "a.halayonok@gmail.com", msg)
            return "Возвращаюсь с пустыми руками. Что-то пошло не так. Я отправил разработчику письмо и он обязательно разберется с этим."