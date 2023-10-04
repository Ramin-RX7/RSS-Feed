import logging

from django.urls import resolve

logger = logging.getLogger("django")


class APICallLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        match = resolve(request.path_info)
        url_name = match.url_name
        user = request.user
        user_id = user.id
        user_agent = request.headers.get("user-agent")
        ip = request.META.get('REMOTE_ADDR')

        logger.info(f"Request: {request.method} {url_name}({request.path}) {user.username}({user_id})")
        logger.info(f"Response: {response.status_code}")

        return response
