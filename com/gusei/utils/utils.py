from datetime import datetime
import pytz

IST = pytz.timezone('Asia/Kolkata')

class Utils:

    def get_current_datetime_str(self):
        return datetime.now(IST).strftime("%d-%m-%Y %H:%M:%S")

    def get_current_datetime(self):
        datetime_str=datetime.now(IST).strftime("%d-%m-%Y %H:%M:%S")
        return datetime.strptime(datetime_str,"%d-%m-%Y %H:%M:%S")

    def convert_datetime(self,datetime_str):
        return datetime.strptime(datetime_str,"%d-%m-%Y %H:%M:%S")
