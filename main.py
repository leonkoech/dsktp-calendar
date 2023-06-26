from __future__ import print_function

import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from rainmeter import createSkin

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def calendarAPI(maxResults):
    result = []
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('.env/token.json'):
        creds = Credentials.from_authorized_user_file('.env/token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                '.env/credentials.json', SCOPES)
            creds = flow.run_local_server(port=8080)
        # Save the credentials for the next run
        with open('.env/token.json', 'w') as token:
            token.write(creds.to_json())
            token.close()

    try:
        service = build('calendar', 'v3', credentials=creds)

        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        events_result = service.events().list(calendarId='primary', timeMin=now,
                                              maxResults=maxResults, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
            return {}

        # Prints the start and name of the next n events. n is the parameter
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            end = event['end'].get('dateTime', event['end'].get('date'))
            htmlLink  = event['htmlLink']
            title = event['summary']
            status = event['status']
            description = event.get("description", "")
            obj = {
                "start": (datetime.datetime.strptime(start,  "%Y-%m-%dT%H:%M:%S%z")).strftime("%H:%M"),
                "end": (datetime.datetime.strptime(end,  "%Y-%m-%dT%H:%M:%S%z")).strftime("%H:%M"),
                "htmlLink": htmlLink,
                "title": title,
                "status": status,
                "description": description,
            }
            result.append(obj)
        return {"results": result}

    except HttpError as error:
        return{error: error}

def main():
    query = calendarAPI(2)
    result = {}
    try:
        result = query.get("results") # type: ignore
        createSkin(result)
    except:
        result = {"queryError:" : query.get("error")}# type: ignore

if __name__ == '__main__':
    main()