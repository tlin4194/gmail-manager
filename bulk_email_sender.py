"""
Python class to send email to a list of
emails from a spreadsheet
"""

import csv
import os
from email_builder import EmailBuilder
from gmail_service import GmailService

MY_EMAIL = "test@gmail.com"
SUBJECT = "test subject"

# switch between real and test data dir
DATA_DIR = ".data"
if os.path.exists(DATA_DIR):
    with open(os.path.join(DATA_DIR, "my_email.txt"), mode='r') as file:
        MY_EMAIL = file.readline()

    with open(os.path.join(DATA_DIR, "subject.txt"), mode='r') as file:
        SUBJECT = file.readline()

# reading mailing list csv
with open(os.path.join(DATA_DIR, "emails.csv"), mode='r') as file:
    email_csv = csv.DictReader(file, skipinitialspace=True)

    g = GmailService("credentials.json")
    eb = EmailBuilder(sender=MY_EMAIL, message_file=os.path.join(
        DATA_DIR, "email_message.txt"))
    for row in email_csv:
        eb.set_subject(f"{SUBJECT} with {row["Name"]}?")
        eb.set_receiver(row["Email"])
        g.send_email(eb.build())
