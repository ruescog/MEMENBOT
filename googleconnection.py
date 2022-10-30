import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def get_creds():
    creds = None
    path = ".secrets/token.json"
    if os.path.exists(path):
        creds = Credentials.from_authorized_user_file(path, SCOPES)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('.secrets/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open(path, 'w') as token:
            token.write(creds.to_json())
    
    return Credentials.from_authorized_user_file(path, SCOPES)