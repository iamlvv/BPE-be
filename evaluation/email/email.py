import os
import ssl
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class Email:
    @classmethod
    def verify_account(self, receiver_email, name, token):
        sender_email = os.environ.get("EMAIL")
        password = os.environ.get("PASSWORD")

        message = MIMEMultipart("alternative")
        message["Subject"] = "Verify your email"
        message["From"] = sender_email
        message["To"] = receiver_email

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

        # Turn these into plain/html MIMEText objects
        part2 = MIMEText(html, "html")

        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        message.attach(part2)

        # Create secure connection with server and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(
                sender_email, receiver_email, message.as_string()
            )
