import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.exceptions import RefreshError


class CredentialsAPIservice:

        def __init__(self):
             self.__scope__ = ['https://www.googleapis.com/auth/calendar.readonly']
             self.credentials = None
             self.token_file = ".env/token.json"
             self.credentials_file = '.env/credentials.json'

        def run_local_server(self):
            flow = InstalledAppFlow.from_client_secrets_file(
                self.credentials_file, self.__scope__)
            self.credentials = flow.run_local_server(port=8080)

        def auth(self):
            # The file token.json stores the user's access and refresh tokens, and is
            # created automatically when the authorization flow completes for the first
            # time.
            if os.path.exists(self.token_file):
                self.credentials = Credentials.from_authorized_user_file(self.token_file, self.__scope__)
            # If there are no (valid) self.credentials available, let the user log in.
            if not self.credentials or not self.credentials.valid:
                if self.credentials and self.credentials.expired and self.credentials.refresh_token:
                    try:
                        self.credentials.refresh(Request())
                    except RefreshError:
                        # delete  token file if refresh error happens. Naturally call the function again
                        os.remove(self.token_file) 
                        self.run_local_server()
                else:
                    self.run_local_server()
                # Save the credentials for the next run
                with open(self.token_file, 'w') as token:
                    token.write(self.credentials.to_json())
                    token.close()
            return self.credentials
        
        @classmethod
        def getCredentials(cls):
             return cls().auth()
        
        def user_email(self):
             print("primary")