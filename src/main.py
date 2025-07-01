from fetch_emails import fetch_recent_emails, get_gmail_service
from summary import summarize_emails_snippets
import base64
from email.mime.text import MIMEText

EMAIL_SUMMARY = False

def format_emails_vertical(emails):
    """Format emails as a vertical, readable list."""
    lines = []
    for idx, email in enumerate(emails, 1):
        lines.append(f"Email {idx}:")
        lines.append(f"From: {email['sender']}")
        lines.append(f"Subject: {email['subject']}")
        lines.append(f"Date: {email['date']}")
        lines.append(f"Snippet: {email['snippet']}")
        lines.append("")
    return "\n".join(lines)

def send_email_via_gmail(subject, body, to_email):
    """Send an email using the authenticated Gmail API client."""
    service = get_gmail_service()
    message = MIMEText(body)
    message['to'] = to_email
    message['subject'] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    message_body = {'raw': raw}
    service.users().messages().send(userId='me', body=message_body).execute()



def main():
    emails = fetch_recent_emails(20)
    if not emails:
        print("No emails found.")
        return
    print("\nYour 20 most recent emails:\n")
    print(format_emails_vertical(emails))
    snippets = [email['snippet'] for email in emails if email.get('snippet')]
    if not snippets:
        print("No email snippets found.")
        return
    
    summary = summarize_emails_snippets(snippets, method='transformers')
    print("\nSummary of your 20 most recent emails:\n")
    print(summary)

    if EMAIL_SUMMARY:
        # Email the summary to myself
        send_email_via_gmail(
            subject="Your Daily Email Summary",
            body=summary,
            to_email=emails[0]['sender'] if emails else 'me'  # fallback to 'me' if no sender
        )
        print("\nSummary emailed to you!")

if __name__ == "__main__":
    main()
