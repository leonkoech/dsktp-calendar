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
        now = datetime.datetime.utcnow()
        min_time = now.isoformat() + 'Z'
        max_time = now.replace(hour=23, minute=59, second=0, microsecond=0).isoformat() + 'Z'
        events_result = self.service.events().list(calendarId=calendarId, timeMin=min_time, timeMax=max_time,
                                                maxResults=maxResults, singleEvents=True,
                                                orderBy='startTime').execute()
        print(events_result)
        return events_result.get('items', [])
    
    def formatEvent(self, event):
        
        start = event['start'].get('dateTime', event['start'].get('date'))
        end = event['end'].get('dateTime', event['end'].get('date'))
        print(start)
        print(end)
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
