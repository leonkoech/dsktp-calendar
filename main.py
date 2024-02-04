from rainmeter import RainMeterService
from calendarAPI import CalendarAPIService

def main():
    max_events = 7
    query = CalendarAPIService.getCalendar(maxResults=max_events)
    result = {}
    try:
        result = query.get("results") # type: ignore
        skin_name="dsktp calendar"
        computer_name="17866"
        destination =  r"C:\Users\{computerName}\Documents\Rainmeter\Skins\{skinName}".format(computerName=computer_name, skinName=skin_name)
        rainmeter = r"C:\Program Files\Rainmeter\Rainmeter.exe"
        # print("\n{}\n{}\n{}\n{}".format( result, destination, rainmeter, skin_name))
        
        try:
            RainMeterService.createSkin(event_details=result, destination=destination, rainmeter=rainmeter, skin_name=skin_name, max_events = max_events)
        except Exception as e:
            pass
            # print(e)
        # print("done")
    except:
        result = {"queryError:" : query.get("error")}# type: ignore

if __name__ == '__main__':
    main()