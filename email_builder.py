"""
Uses GmailService class to send emails
See https://developers.google.com/gmail/api/guides/sending#python
"""
import base64
from email.message import EmailMessage


class EmailBuilder():
    def __init__(self, sender: str, message_file: str):
        self.message = EmailMessage()
        with open(message_file, 'r') as f:
            self.message.set_content(f.read())
        self.message["From"] = sender

    def set_subject(self, subject: str):
        self.message["Subject"] = subject

    def set_receiver(self, email: str):
        self.message["To"] = email

    def build(self):
        # encoded message
        encoded_message = base64.urlsafe_b64encode(
            self.message.as_bytes()).decode()
        return {"raw": encoded_message}

    def __str__(self) -> str:
        return str(self.message)


if __name__ == "__main__":
    test = EmailBuilder(sender="test@gmail.com",
                        message_file="test/email_message.txt")
    test.set_subject("TEST")
    test.set_receiver("test@gmail.com")
    print(test)
    print(test.build())
