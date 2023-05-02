import os
import ssl
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class Email:
    @classmethod
    def send(self, sender_email, password, receiver_email, subject, content):
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = sender_email
        message["To"] = receiver_email

        part = MIMEText(content, "html")
        message.attach(part)

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(
                sender_email, receiver_email, message.as_string()
            )

    @classmethod
    def verify_account(self, receiver_email, name, token):
        sender_email = os.environ.get("EMAIL")
        password = os.environ.get("PASSWORD")
        subject = "Verify your email"

        # Create the plain-text and HTML version of your message
        html = f"""\
        <html>
        <body>
            <p>Hi {name},<br>
            Please click <a href="http://localhost:8000/api/v1/user/verify/{token}">here</a> to verify your account or access this bellow link:<br>
            [http://localhost:8000/api/v1/user/verify/{token}]<br>
            Thank you so much,<br>
            BPSky
            </p>
        </body>
        </html>
        """
        self.send(sender_email, password, receiver_email, subject, html)

    @classmethod
    def reset_password(self, receiver_email, name, token):
        sender_email = os.environ.get("EMAIL")
        password = os.environ.get("PASSWORD")
        subject = "Reset password"

        # Create the plain-text and HTML version of your message
        html = f"""\
        <html>
        <body>
            <p>Hi {name},<br>
            Please click <a href="http://localhost:5173/reset-password?token={token}">here</a> to reset password or access this bellow link:<br>
            [http://localhost:5173/reset-password?token={token}]<br>
            Thank you so much,<br>
            BPSky
            </p>
        </body>
        </html>
        """
        self.send(sender_email, password, receiver_email, subject, html)
