"""
Uses GmailService class to send emails
See https://developers.google.com/gmail/api/guides/sending#python
"""
import base64
from email.message import EmailMessage


class EmailBuilder():
    def __init__(self, sender: str, recipient: str, message_file: str, subject="", ):
        self.message = EmailMessage()
        with open(message_file, 'r') as f:
            self.message_template = f.read()
        self.message["From"] = sender
        self.message["Subject"] = subject
        self.message["To"] = recipient

    def build(self, fields: dict = None):
        message_body = self.message_template
        if fields:
            for field, value in fields.items():
                if field == "Email":
                    continue
                message_body = message_body.replace(
                    f"{{{{{field}}}}}", value, 1)
        if "{{" in message_body or "}}" in message_body:
            raise Exception("Email Template missing field value")
        self.message.set_content(message_body)
        print(self)
        # encoded message
        encoded_message = base64.urlsafe_b64encode(
            self.message.as_bytes()).decode()
        return {"raw": encoded_message}

    def __str__(self) -> str:
        return str(self.message)


if __name__ == "__main__":
    test = EmailBuilder(sender="test@gmail.com",
                        recipient="test@gmail.com",
                        message_file="test/email_message.txt",
                        subject="TEST")
    print(test.build(
        fields={"Name": "Bob", "Topic": "Topic A", "Meeting Date": "Wednesday 11AM"}))
