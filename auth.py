import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly",
          "https://www.googleapis.com/auth/gmail.modify", 
          "https://www.googleapis.com/auth/gmail.labels"
]

def authenticate_gmail():
    """Authenticate and connect to the Gmail API."""
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("C:\FYP\credentials.json", SCOPES)
            creds = flow.run_local_server(port=57500)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    service = build("gmail", "v1", credentials=creds)
    return service

def fetch_emails(service):
    """Fetch emails from the user's Gmail account."""
    results = service.users().messages().list(userId="me", maxResults=10).execute()
    messages = results.get("messages", [])
    return messages