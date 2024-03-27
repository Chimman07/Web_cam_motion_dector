import smtplib
from email.message import EmailMessage
import imghdr

username = "sonichimman@gmail.com"
password = "WzsAc4S85WFLxJ"


def send_email(filepath):
    email_message = EmailMessage()
    email_message["Subject"] = "New person detected"
    email_message.set_content("Hey a new person is detected")

    with open(filepath, "rb") as file:
        content = file.read()

    email_message.add_attachment(content, maintype="image", subtype=imghdr.what(None, content))

    gmail = smtplib.SMTP("smtp.gmail.com", 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(username, password)

