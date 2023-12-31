import pytz
import logging
from datetime import datetime
from logging import LogRecord

import elasticsearch

from django.utils import timezone

from config.settings import TIME_ZONE
from .base import BASE_ENV

from core.utils import get_nows



__all__ = ("ES_CONNECTION",)


ELASTIC_INDEX_PREFIX = "ind"
ES_CONNECTION = elasticsearch.Elasticsearch(BASE_ENV("ELASTIC_URL"))
tz = pytz.timezone(TIME_ZONE)




class ElasticLogHandler(logging.Handler):
    def __init__(self, *, elastic_url, **kwargs):
        self.elastic_connection = elasticsearch.Elasticsearch(elastic_url)
        super().__init__(**kwargs)

    def emit(self, record: LogRecord) -> None:
        data = record.msg
        data["level"] = record.levelname
        data["log_timestamp"] = get_nows()
        today = datetime.now(tz).strftime("%Y_%m_%d")
        self.elastic_connection.index(f"{ELASTIC_INDEX_PREFIX}_{today}", body=data)




_Action = [
    "login", "register", "refresh", "access",
    "change-password", "change-password-request",
    "reset-password" , "reset-password-request",
    "logout", "logout-all", "logout-other",
    "system-*"  # e.g: "system-send-email", "system-track-user"
]
AUTH_PATTERN = {
    "user_id": int,
    "timestamp": int,  # Time since epoch in ms
    "message": str,
    "action" : str, # of _Action
    "user_agent": str,  # if action != "system-*"
    "ip": str,          # if action != "system-*"
}


API_CALLS_PATTERN = {
    "request_timestamp" : int,
    "response_timestamp" : int,
    "url_name": str,
    "url_path": str,
    "request_data": dict,
    "http_method": str,  # HTTP method
    "user_id": int,
    "user_agent": str,
    "ip": str,
    "response_code": int,
}


PODCAST_UPDATE_PATTERN = {
    "message" : str,
    "podcast_id" : int,
    "args" : list,
    "kwargs" : dict,
    "error_name" : str,      # only if level >= "warning"
    "error_message" : str,   # only if level >= "warning"
}


json = dict
NOTIFICATION_PATTERN = {
    "name": str,
    "notif_data": json,
    "user": int,   # 0 if users not set
    "message": str,
}
