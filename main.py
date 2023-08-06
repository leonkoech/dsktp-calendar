from rainmeter import RainMeterService
from calendarAPI import CalendarAPIService

def main():
    query = CalendarAPIService.getCalendar(maxResults=5)
    result = {}
    try:
        result = query.get("results") # type: ignore
        skin_name="dsktp calendar"
        destination =  r"C:\Users\{computerName}\Documents\Rainmeter\Skins\{skinName}".format(computerName="17866", skinName=skin_name)
        rainmeter = r"C:\Program Files\Rainmeter\Rainmeter.exe"
        print("\n{}\n{}\n{}\n{}".format( result, destination, rainmeter, "dsktp calendar"))
        
        try:
            RainMeterService.createSkin(event_details=result, destination=destination, rainmeter=rainmeter, skin_name=skin_name)
        except Exception as e:
            print(e)
        print("done")
    except:
        result = {"queryError:" : query.get("error")}# type: ignore

if __name__ == '__main__':
    main()