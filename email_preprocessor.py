import re
from bs4 import BeautifulSoup

def preprocess_email(email_content):
    # Code for cleaning and extracting text
    soup = BeautifulSoup(email_content, "html.parser")
    email_text = soup.get_text()
    email_text = re.sub(r"http\S+|www\S+|https\S+", "", email_text, flags=re.MULTILINE)
    email_text = re.sub(r"[^a-zA-Z\s]", "", email_text)
    email_text = email_text.lower().strip()
    return email_text
