from rainmeter import RainMeterService
from calendarAPI import CalendarAPIService

def main():
    query = CalendarAPIService.getCalendar(maxResults=10)
    result = {}
    try:
        result = query.get("results") # type: ignore
        skin_name="dsktp calendar"
        computer_name="17866"
        destination =  r"C:\Users\{computerName}\Documents\Rainmeter\Skins\{skinName}".format(computerName=computer_name, skinName=skin_name)
        rainmeter = r"C:\Program Files\Rainmeter\Rainmeter.exe"
        print("\n{}\n{}\n{}\n{}".format( result, destination, rainmeter, skin_name))
        
        try:
            RainMeterService.createSkin(event_details=result, destination=destination, rainmeter=rainmeter, skin_name=skin_name)
        except Exception as e:
            print(e)
        print("done")
    except:
        result = {"queryError:" : query.get("error")}# type: ignore

if __name__ == '__main__':
    main()