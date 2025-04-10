import re
from bs4 import BeautifulSoup

def preprocess_email(email_content):
    """Improved preprocessing to clean and retain key phishing indicators."""
    # Parse email content to extract visible text
    soup = BeautifulSoup(email_content, "html.parser")
    email_text = soup.get_text()
    
    # Retain and extract URLs instead of removing them
    urls = re.findall(r"http\S+|www\S+|https\S+", email_text)
    
    # Clean the text but preserve numbers and symbols for phishing clues
    email_text = re.sub(r"[^a-zA-Z0-9\s@._%-]", "", email_text, flags=re.MULTILINE)
    
    # Normalize the text by lowercasing and stripping unnecessary whitespace
    email_text = email_text.lower().strip()
    
    # Optionally return extracted URLs as part of preprocessing output
    return email_text, urls