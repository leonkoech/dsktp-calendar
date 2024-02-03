from datetime import datetime, timedelta
"""
Class that calculates the time to input into the calendar API based on location, utc, etc.
"""
class TimeService:
    def __init__(self):
        self.max_time = None
        self.min_time = None
        self.find_times()

    """
    Function to calculate max and min time based on utc. computes the results into the class's 
    """
    def find_times(self):
        time_difference = self._find_time_difference()
        now = datetime.utcnow()
        min_origin_time =  now.replace(hour=00, minute=00, second=0, microsecond=0)
        max_origin_time = now.replace(hour=23, minute=59, second=59, microsecond=0)

        self.max_time = self._calculate_times(time_difference, max_origin_time)
        self.min_time = self._calculate_times(time_difference, min_origin_time)

    """
    function takes in time_origin and returns time after time difference calculation
    """
    def _calculate_times(self, time_difference, time_origin):
        iso_format_with_z = (time_origin - timedelta(hours = time_difference)).isoformat() + "Z"
        return iso_format_with_z
    
    """
    function to find the time difference between system and utc
    """
    def _find_time_difference(self):
        utc_now = datetime.utcnow().strftime("%H")
        current_time = datetime.now().strftime("%H")
        return int(current_time)-int(utc_now)
