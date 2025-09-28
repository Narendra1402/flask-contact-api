from flask import Flask, request, jsonify
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all domains

@app.route("/send", methods=["POST", "OPTIONS"])
def send_email():
    if request.method == "OPTIONS":
        return jsonify({"message": "Preflight OK"}), 200

    data = request.get_json()

    SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")
    EMAIL_SENDER = os.environ.get("EMAIL_USER")

    if not SENDGRID_API_KEY or not EMAIL_SENDER:
        return jsonify({"error": "Missing SendGrid API Key or Sender Email"}), 500

    message = Mail(
        from_email=EMAIL_SENDER,
        to_emails=EMAIL_SENDER,  # Receiving email (your own)
        subject=f"New Contact Form Submission from {data.get('fullname', 'Unknown')}",
        plain_text_content=f"""
        You received a contact form submission:

        Name: {data.get('fullname')}
        Email: {data.get('email')}
        Message: {data.get('meeting')}
        """
    )

    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        print("SendGrid response:", response.status_code)
        return jsonify({"message": "Email sent successfully"}), 200

    except Exception as e:
        print("SendGrid error:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

