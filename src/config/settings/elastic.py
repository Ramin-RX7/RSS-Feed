import elasticsearch

from .base import BASE_ENV


__all__ = ("ES_CONNECTION",)


ES_CONNECTION = elasticsearch.Elasticsearch(BASE_ENV("ELASTIC_URL"))




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
