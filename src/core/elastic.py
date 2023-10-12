from datetime import datetime

import pytz

from config.settings import ES_CONNECTION,TIME_ZONE



INDEX_PREFIX = "ind"
tz = pytz.timezone(TIME_ZONE)



def submit_record(event:str, data:dict):
    tz_now = datetime.now(tz)
    today = tz_now.strftime("%Y_%m_%d")
    data["event_type"] = event
    ES_CONNECTION.index(f"{INDEX_PREFIX}_{today}", body=data)
