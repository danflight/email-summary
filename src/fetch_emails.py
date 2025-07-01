"""
src/fetch_emails.py

Handles Gmail API authentication and provides functions to fetch recent emails
with sender, subject, date, and snippet/body information.
"""

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from gmail_auth import get_gmail_service
import os

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
TOKEN_PATH = 'token.json'
CREDENTIALS_PATH = 'credentials.json'


def fetch_recent_emails(max_results=20):
    """
    Fetches the most recent emails from the user's Gmail account.

    Args:
        max_results (int): Number of recent emails to fetch (default: 20).

    Returns:
        List[dict]: List of emails, each as a dict with sender, subject, date, and snippet/body.
    """
    service = get_gmail_service()
    results = service.users().messages().list(userId='me', maxResults=max_results).execute()
    messages = results.get('messages', [])
    emails = []
    for msg in messages:
        msg_data = service.users().messages().get(userId='me', id=msg['id'], format='full').execute()
        headers = msg_data['payload']['headers']
        email_info = {
            'sender': next((h['value'] for h in headers if h['name'] == 'From'), None),
            'subject': next((h['value'] for h in headers if h['name'] == 'Subject'), None),
            'date': next((h['value'] for h in headers if h['name'] == 'Date'), None),
            'snippet': msg_data.get('snippet', None)
        }
        emails.append(email_info)
    return emails
