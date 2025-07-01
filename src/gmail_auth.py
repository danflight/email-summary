"""
src/gmail_auth.py

Handles Gmail API OAuth2 authentication and returns an authenticated Gmail service client.
"""

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import os

SCOPES = ['https://www.googleapis.com/auth/gmail.send']
TOKEN_PATH = 'token.json'
CREDENTIALS_PATH = 'credentials.json'

def get_gmail_service():
    """
    Authenticates the user with Gmail API using OAuth2 and returns a Gmail service client.

    Returns:
        googleapiclient.discovery.Resource: Authenticated Gmail API service client.

    Side Effects:
        - Opens a browser window for OAuth2 flow if no valid token is found.
        - Stores/refreshes tokens in 'token.json'.
    """
    creds = None
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_PATH, 'w') as token:
            token.write(creds.to_json())
    service = build('gmail', 'v1', credentials=creds)
    return service
