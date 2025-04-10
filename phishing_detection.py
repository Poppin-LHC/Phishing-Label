from transformers import pipeline
from email_preprocessor import preprocess_email  # Preprocess email content
from auth import authenticate_gmail, fetch_emails  # Import Gmail API logic

def fetch_email_details(service, message_id):
    """Fetch specific email details like subject and sender."""
    msg = service.users().messages().get(userId="me", id=message_id).execute()
    headers = msg["payload"]["headers"]
    subject = next((header["value"] for header in headers if header["name"] == "Subject"), "No Subject")
    sender = next((header["value"] for header in headers if header["name"] == "From"), "Unknown Sender")
    snippet = msg.get("snippet", "No Snippet Available")
    return subject, sender, snippet
    
def get_label_id(service, label_name="Phishing Detected"):
    results = service.users().labels().list(userId="me").execute()
    labels = results.get("labels", [])
    for label in labels:
        if label["name"] == label_name:
            return label["id"]
    return None

def apply_label(service, message_id, label_id):
    body = {"addLabelIds": [label_id], "removeLabelIds": []}
    service.users().messages().modify(userId="me", id=message_id, body=body).execute()

def analyze_emails(service, pipe, label_id):
    messages = fetch_emails(service)
    for message in messages:
        message_id = message["id"]
        subject, sender, snippet = fetch_email_details(service, message_id)
        
        # Update to unpack the two returned values from preprocess_email
        cleaned_email, urls = preprocess_email(snippet)
        
        # Pass only the cleaned_email to the classification pipeline
        result = pipe(cleaned_email)
        label = result[0]["label"]
        score = result[0]["score"]

        print(f"Analyzing email:\nCleaned Content: {cleaned_email}\nURLs: {urls}\nLabel: {label}\nScore: {score}")
        
        if label == "phishing" and score > 0.9:
            apply_label(service, message_id, label_id)
            print(f"Labeled email from {sender} with subject '{subject}' as PHISHING.")

def create_label(service, label_name):
    """Create a Gmail label."""
    label = {
        "name": label_name,
        "labelListVisibility": "labelShow",
        "messageListVisibility": "show"
    }
    created_label = service.users().labels().create(userId="me", body=label).execute()
    return created_label["id"]

def main():
    service = authenticate_gmail()
    if not service:
        print("Failed to authenticate Gmail API")
        return
    
    pipe = pipeline("text-classification", model="ealvaradob/bert-finetuned-phishing")
    label_name = "Phishing"
    label_id = get_label_id(service, label_name)
    if not label_id:
        print(f"Label '{label_name}' not found. Creating it in Gmail...")
        label_id = create_label(service, label_name)
        print(f"Label '{label_name}' created successfully.")
    analyze_emails(service, pipe, label_id)


if __name__ == "__main__":
    main()