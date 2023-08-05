import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from rainmeter import RainMeterService
from calendarAPI import CalendarAPIService

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
        #fetch calendar ID objects
        calendar_service = CalendarAPIService(service=service)
        calendar_ids = calendar_service.fetchCalendarIds()
        print(calendar_ids)
        # Call the Calendar API
        events = calendar_service.fetchCalendarEvents(calendarId="primary", maxResults=maxResults)
        
        if not events:
            print('No upcoming events found.')
            return {}

        # Prints the start and name of the next n events. n is the parameter
        for event in events:
            formatted_event = calendar_service.formatEvent(event)
            result.append(formatted_event)
        return {"results": result}

    except HttpError as error:
        return{error: error}

def main():
    query = calendarAPI(5)
    result = {}
    try:
        result = query.get("results") # type: ignore
        destination_dir =  os.getcwd() + "\\dsktp calendar cpy"
        rainmeter_location = "C:\Program Files\Rainmeter\Rainmeter.exe"
        rainmeter_skin_service = RainMeterService(event_details=result,destination=destination_dir, rainmeter=rainmeter_location)
        rainmeter_skin_service.createSkin()
    except:
        result = {"queryError:" : query.get("error")}# type: ignore

if __name__ == '__main__':
    main()