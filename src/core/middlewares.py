import logging

from django.urls import resolve
from django.utils import timezone

from core.utils import get_request_data,get_nows



logger = logging.getLogger("elastic")



class APICallLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request_timestamp = get_nows()
        response = self.get_response(request)
        user = request.user

        logger.info({"event_type": "api_call",
            "request_timestamp" : request_timestamp,
            "response_timestamp" : get_nows(),

            "url_name": resolve(request.path_info).url_name,
            "url_path": request.path,

            "request_data": get_request_data(request),
            "http_method": request.method,

            "user_id": user.id if user.is_authenticated else 0,
            "user_agent": request.headers.get("user-agent"),
            "ip": request.META.get('REMOTE_ADDR'),

            "response_code": response.status_code
        })
        return response
