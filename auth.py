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
    """Authenticate and connect to the Gmail API with robust token handling."""
    creds = None

    # Attempt to load credentials from token.json
    if os.path.exists("token.json"):
        try:
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        except Exception as e:
            print(f"Error loading token.json: {e}")
    
    # Check if credentials are valid or need refreshing
    if creds and creds.expired and creds.refresh_token:
        try:
            print("Refreshing token...")
            creds.refresh(Request())
        except Exception as e:
            print(f"Failed to refresh token: {e}")
            creds = None  # Force re-authentication if refresh fails
    
    # If credentials are missing or invalid, prompt user re-authentication
    if not creds or not creds.valid:
        try:
            flow = InstalledAppFlow.from_client_secrets_file(r"C:\FYP\credentials.json", SCOPES)
            creds = flow.run_local_server(port=57500)
        except Exception as e:
            print(f"Authentication failed: {e}")
            return None
    
    # Save valid credentials back to token.json
    try:
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    except Exception as e:
        print(f"Failed to save token.json: {e}")
    
    # Build and return the Gmail service
    try:
        service = build("gmail", "v1", credentials=creds)
        return service
    except Exception as e:
        print(f"Failed to build Gmail service: {e}")
        return None

def fetch_emails(service):
    """Fetch emails from the user's Gmail account."""
    results = service.users().messages().list(userId="me", maxResults=10).execute()
    messages = results.get("messages", [])
    return messages