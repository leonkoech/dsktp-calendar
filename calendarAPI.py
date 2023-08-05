import datetime

class CalendarAPIService:
    def __init__(self, service):
        self.service = service
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

    def fetchCalendarEvents(self, calendarId, maxResults):
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        events_result = self.service.events().list(calendarId=calendarId, timeMin=now,
                                                maxResults=maxResults, singleEvents=True,
                                                orderBy='startTime').execute()
        return events_result.get('items', [])
    
    def formatEvent(self, event):
        start = event['start'].get('dateTime', event['start'].get('date'))
        end = event['end'].get('dateTime', event['end'].get('date'))
        htmlLink  = event['htmlLink']
        title = event['summary']
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
