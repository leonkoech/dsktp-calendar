import datetime
from timeService import TimeService

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from credentialsAPI import CredentialsAPIservice
"""
Calendar API Service class that performs some services in relation to the google 
calendar API;
- fetching calendar IDs
- fetch Calendar Events
- format events
"""
class CalendarAPIService:
    def __init__(self):
        self.service = None

    @classmethod
    def getCalendar(cls, maxResults):
        return cls().calendarAPI(maxResults)
    
    """
    Main entry point of tha calendar API, does everything from auth to fetching calendar
    """
    def calendarAPI(self, maxResults):
        result = []
        credentials = CredentialsAPIservice.getCredentials()
        try:
            self.service = build('calendar', 'v3', credentials=credentials)
            #fetch calendar ID objects
            # calendar_ids = self.fetchCalendarIds()
            # print(calendar_ids)
            # Call the Calendar API
            events = self.fetchCalendarEvents(calendarId="primary", maxResults=maxResults)
            print("found {} events".format(len(events)))
            if not events:
                print('No upcoming events found.')
                return {}

            # Prints the start and name of the next n events. n is the parameter
            for event in events:
                formatted_event = self.formatEvent(event)
                result.append(formatted_event)
            return {"results": result}

        except HttpError as error:
            return{error: error}

    """
    Fetch calendar IDS, will enable a user to select a calendar ID and use that fetch
    """
    def fetchCalendarIds(self):
        calendar_list=[]
        page_token = None
        while True:
            fetched_calendar_list = self.service.calendarList().list(pageToken=page_token).execute()
            for calendar_list_entry in fetched_calendar_list['items']:
                calendar_list.append(calendar_list_entry['summary'])
            page_token = fetched_calendar_list.get('nextPageToken')
            if not page_token:
                break
        return calendar_list

    """
    Fetch calendar IDs based on calendarIds
    """
    def fetchCalendarEvents(self, calendarId, maxResults):
        time_service = TimeService()
        min_time =  time_service.min_time
        max_time = time_service.max_time

        events_result = self.service.events().list(calendarId=calendarId, timeMin=min_time, timeMax=max_time,
                                                maxResults=maxResults, singleEvents=True,
                                                orderBy='startTime').execute()
        print(events_result)
        print("--------------------------")
        return events_result.get('items', [])

    """
    Formats an event into a format that can be used when creating the skin for the desktop
    """
    def formatEvent(self, event):
        start = event['start'].get('dateTime', event['start'].get('date'))
        end = event['end'].get('dateTime', event['end'].get('date'))
        htmlLink  = event['htmlLink']
        title = event.get("summary", "(no title)")
        status = event['status']
        description = event.get("description", "")
        return {
            "start": (datetime.datetime.strptime(start,  "%Y-%m-%dT%H:%M:%S%z")).strftime("%H:%M"),
            "end": (datetime.datetime.strptime(end,  "%Y-%m-%dT%H:%M:%S%z")).strftime("%H:%M"),
            "htmlLink": htmlLink,
            "title": title,
            "status": status,
            "description": description,
        }
    
