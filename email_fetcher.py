def fetch_emails(service):
    """Fetch emails from the user's Gmail account."""
    results = service.users().messages().list(userId="me", maxResults=10).execute()
    messages = results.get("messages", [])
    for message in messages:
        msg = service.users().messages().get(userId="me", id=message["id"]).execute()
        print(f"Message snippet: {msg['snippet']}")
