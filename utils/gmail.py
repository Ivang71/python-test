import os.path, base64, requests

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from email.mime.text import MIMEText


SCOPES = [
    # "https://www.googleapis.com/auth/gmail.readonly",
    "openid",
    # "https://mail.google.com/",
    "https://www.googleapis.com/auth/userinfo.profile",
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/userinfo.email",
]
PORT = 5788


class Gmail:
    creds = None
    mail_service = None
    
    
    def __init__(self):
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first time.
        if os.path.exists("token.json"):
            self.creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
                self.creds = flow.run_local_server(port=PORT)
            # Save the credentials for the next run
            with open("token.json", "w") as token:
                token.write(self.creds.to_json())
                
        self.mail_service = build('gmail', 'v1', credentials=self.creds)   
        
    def get_user_profile(self):
        userinfo_endpoint = 'https://www.googleapis.com/oauth2/v3/userinfo'
        headers = {'Authorization': f'Bearer {self.creds.token}'}
        response = requests.get(userinfo_endpoint, headers=headers)
        if response.status_code == 200:
            user_profile = response.json()
            return user_profile
        else:
            print(f"Failed to fetch user profile: {response.status_code} - {response.text}")
            return None


    def send(self, to, subject, body):
        if not self.creds:
            print("Error: No credentials found. Please set up Application Default Credentials.")
            return
        try:
            user = self.get_user_profile()
            message = MIMEText(body)
            message['to'] = to
            message['from'] = f'{user["name"]} \u003c{user["email"]}\u003e'
            message['subject'] = subject
            raw = base64.urlsafe_b64encode(message.as_bytes())
            raw = raw.decode()
            message = self.mail_service.users().messages().send(userId='me', body={'raw': raw}).execute()
        except HttpError as error:
            print('An error occurred: %s' % error)
        
        
    
    