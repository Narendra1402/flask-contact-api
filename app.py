from flask import Flask, request, jsonify
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Enables CORS so frontend (e.g. GitHub Pages) can talk to this backend

@app.route("/send", methods=["POST"])
def send_email():
    data = request.get_json()

    SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")
    EMAIL_SENDER = os.environ.get("EMAIL_USER")  # Should be verified in SendGrid

    if not SENDGRID_API_KEY or not EMAIL_SENDER:
        return jsonify({"error": "Missing SendGrid API Key or Sender Email"}), 500

    # Build HTML content for better deliverability
    html_content = f"""
        <html>
            <body>
                <h2>New Contact Form Submission</h2>
                <p><strong>Name:</strong> {data.get('fullname')}</p>
                <p><strong>Email:</strong> {data.get('email')}</p>
                <p><strong>Subject:</strong> {data.get('visit')}</p>
                <p><strong>Message:</strong> {data.get('meeting')}</p>
                <hr>
                <p style="font-size:12px; color:gray;">
                    This message was sent via your portfolio contact form.<br>
                    If you received this in error, you can ignore it.
                </p>
            </body>
        </html>
    """

    # Create the email message
    message = Mail(
        from_email=Email(EMAIL_SENDER, "Portfolio Site"),
        to_emails=EMAIL_SENDER,
        subject=f"New Contact Form: {data.get('visit', 'No Subject')}",
        html_content=html_content
    )

    # Add reply-to so you can respond directly
    message.reply_to = Email(data.get("email"))

    # Send email
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        print("SendGrid response:", response.status_code)
        return jsonify({"message": "Email sent successfully"}), 200

    except Exception as e:
        print("SendGrid error:", e)
        return jsonify({"error": str(e)}), 500

# Needed for Render or other deployment platforms
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
