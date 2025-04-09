from flask import Flask, jsonify
from auth import authenticate
from preprocessing import preprocess_email
from bert_analysis import analyze_with_bert

app = Flask(__name__)

@app.route('/process-emails', methods=['GET'])
def process_emails():
    try:
        # Authenticate and get Gmail service
        service = authenticate()

        # Fetch email messages
        results = service.users().messages().list(userId="me").execute()
        messages = results.get("messages", [])

        if not messages:
            return jsonify({"message": "No emails found."}), 200

        analyzed_emails = []
        for message in messages:
            msg = service.users().messages().get(userId="me", id=message["id"]).execute()
            email_body = msg.get("snippet", "")  # Extract email snippet/content
            
            # Preprocess and analyze the email
            processed_email = preprocess_email(email_body)
            bert_analysis = analyze_with_bert(processed_email)
            
            # Store the result
            analyzed_emails.append({
                "email_id": message["id"],
                "processed_email": processed_email,
                "bert_analysis": bert_analysis
            })

        return jsonify(analyzed_emails), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(port=5000, debug=True)
