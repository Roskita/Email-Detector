from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from config import scopes, creds_path, token_path, email

def gmail_watcher():
    creds = None

    try:
        creds = Credentials.from_authorized_user_file(token_path, scopes)
    finally:
        pass

    if not creds or creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                creds_path, scopes
            )
            creds = flow.run_local_server(port=0)

    return build("gmail", "v1", credentials=creds)


def gmail_checker(service):
    results = service.users().messages().list(
        userId="me",
        q=f"is:unread from:{email}"
    ).execute()

    messages = results.get('messages', [])
    return len(messages) > 0