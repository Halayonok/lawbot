import smtplib
import os

class EmailSender:
    def __init__(self):
        self.EMAIL = os.environ.get("EMAIL_ADDRESS")
        self.PASSWORD = os.environ.get("EMAIL_PASSWORD")

    def send_email(self, message):
        with smtplib.SMTP('smpt.gmail.com', 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            smtp.login(self.EMAIL, self.PASSWORD)

            msg = f"Subject: Law bot error\n\n{message}"
            smtp.sendmail(self.EMAIL, "a.halayonok@gmail.com", msg)