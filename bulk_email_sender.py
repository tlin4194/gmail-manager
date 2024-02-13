"""
Python class to send email to a list of
emails from a spreadsheet
"""

import argparse
import csv
import os
from email_builder import EmailBuilder
from gmail_service import GmailService
from dotenv import load_dotenv


load_dotenv()


class BulkEmailSender():
    sender_email = os.environ['EMAIL']
    subject = os.environ['SUBJECT']

    def __init__(self, data_dir: str) -> None:
        self.data_dir = data_dir
        if not os.path.exists(self.data_dir):
            raise FileNotFoundError("Data directory does not exist")

    def send(self) -> None:
        # reading mailing list csv
        with open(os.path.join(self.data_dir, "emails.csv"), mode='r') as file:
            email_csv = csv.DictReader(file, skipinitialspace=True)

            g = GmailService("credentials.json")
            for row in email_csv:
                eb = EmailBuilder(sender=BulkEmailSender.sender_email,
                                  recipient=row["Email"],
                                  message_file=os.path.join(
                                      self.data_dir, "email_message.txt"),
                                  subject=BulkEmailSender.subject)
                g.send_email(eb.build(fields=row))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--data", dest="data_dir",
                        default="test", help="Path To Data Directory")
    args = parser.parse_args()
    print(f"Sending emails from emails.csv in {args.data_dir}")
    email_sender = BulkEmailSender(args.data_dir)
    email_sender.send()
