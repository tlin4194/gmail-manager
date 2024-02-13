# gmail-manager
Automating some basic Gmail tasks with Python + SMTP

## Prerequisites

- [Python 3.x](https://www.python.org/downloads/)
- Pip (Python package installer)
- Virtual Env (Recommended)

```bash
python -m venv <env-name>
pip install requirements.txt
```
## Google Cloud Setup
1. Create a project in the [Google Cloud Console](https://console.cloud.google.com/projectselector2/home/dashboard).
2. Following the [Quickstart Guide](https://developers.google.com/gmail/api/quickstart/python), enable the Gmail API and create OAuth credentials (OAuth client ID) and download the JSON file.

[Gmail API Documentation](https://console.cloud.google.com/apis/library/gmail.googleapis.com)

Note: Check [Gmail API Usage Limits](https://developers.google.com/gmail/api/reference/quota) first.

## Usage
Create data directory, using the test directory as a template
```
├── data
│   ├── email_message.txt -> email message body
|   ├── emails.csv        -> emails + fields to replace in email message
```

Create `.env` file in project directory, add subject and sender email address as environment variables.
```
SUBJECT="This is my email subject"
EMAIL="sender@gmail.com"
```

Run script to send an email to each name/email row in `emails.csv`. 
* All fields enclosed with `{{field name}}` in `email_message.txt` must correspond to a column header in `emails.csv`, with values to replace `{{field name}}` in the actual email message bodies. This can be used to customize names, specific words in individual emails.
* `-d` tag specifies name of data directory described above. Defaults to `test/` directory.


```bash
python bulk_email_sender.py -d .data
```

### Example
`emails.csv`:
```
Email,Name,Project Topics
test@gmail.com,Alice,The Forever Waterbottle
```

Email will be formatted as shown:
```
From: <My Email>
Subject: New Project with <Name 1>
To: <Email 1>

Hello {{Name}},
This is a test email! Would you be interested in our new product {{Product Name}}
```