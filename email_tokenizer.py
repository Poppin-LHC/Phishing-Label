from transformers import BertTokenizer

def tokenize_email(text):
    tokenizer = BertTokenizer.from_pretrained("ealvaradob/bert-model-name")
    tokens = tokenizer(text, padding=True, truncation=True, return_tensors="pt")
    return tokens
