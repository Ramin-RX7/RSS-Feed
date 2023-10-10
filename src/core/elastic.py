from datetime import datetime

import pytz

from config.settings import ES_CONNECTION,TIME_ZONE



INDEX_PREFIX = "IND"
tz = pytz.timezone(TIME_ZONE)



def submit_record(data):
    tz_now = datetime.now(tz)
    today = tz_now.strftime("%Y-%m-%d")
    ES_CONNECTION.index(f"{INDEX_PREFIX}-{today}", body=data)
