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
Create files
```
├── .data
│   ├── email_message.txt
|   ├── emails.csv
|   ├── my_email.txt
|   ├── subject.txt
```


```bash
python bulk_email_sender.py
```