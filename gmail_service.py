"""
Use Gmail API with OAuth
See https://developers.google.com/gmail/api/quickstart/python
https://developers.google.com/gmail/api/reference/rest 
"""
import os.path

from email_builder import EmailBuilder
from email.message import EmailMessage

from google.auth.transport.requests import Request
import google.auth.exceptions
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly",
          "https://www.googleapis.com/auth/gmail.send"]
TOKEN_PATH = ".token.json"


class GmailService():
    def __init__(self, file) -> None:
        self.credentials_filepath = file
        self.credentials = None
        self.setup_credentials()
        self.start_service()

    def setup_credentials(self):
        """Shows basic usage of the Gmail API.
        Lists the user's Gmail labels.
        """
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(TOKEN_PATH):
            self.credentials = Credentials.from_authorized_user_file(
                TOKEN_PATH, SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not self.credentials or not self.credentials.valid:
            if self.credentials and self.credentials.expired and self.credentials.refresh_token:
                self.credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_filepath, SCOPES
                )
                self.credentials = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(TOKEN_PATH, "w") as token:
                token.write(self.credentials.to_json())

    def start_service(self):
        try:
            self.service = build("gmail", "v1", credentials=self.credentials)
        except google.auth.exceptions.MutualTLSChannelError as error:
            print(f"Error starting Gmail service: {error}")
        except HttpError as error:
            print(f"An error occurred: {error}")

    def send_email(self, message: EmailMessage):
        try:
            sent_msg = (self.service.users().messages().send(
                userId='me', body=message).execute())
            print(f'Message Id: {sent_msg["id"]}')
        except HttpError as error:
            print(f"Error sending email: {error}")
            sent_msg = None
        return sent_msg

    def get_labels(self):
        try:
            results = self.service.users().labels().list(userId="me").execute()
            labels = results.get("labels", [])

            if not labels:
                print("No labels found.")
                return
            print("Labels:")
            for label in labels:
                print(label["name"])

        except HttpError as error:
            print(f"Error getting labels: {error}")


if __name__ == "__main__":
    g = GmailService(".credentials.json")
    g.get_labels()
    test_email = EmailBuilder(sender="test@gmail.com",
                              recipient="test@gmail.com",
                              message_file="test/email_message.txt",
                              subject="TEST")
    g.send_email(test_email.build())
