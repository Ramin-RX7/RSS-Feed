from datetime import datetime

from config.settings import TZ_INFO



def get_request_data(request):
    try:
        request_data = request.data
    except AttributeError as _:
        if request.method in ("GET", "POST"):
            request_data = getattr(request, request.method)
        else:
            request_data = None

    return request_data


def get_now():
    return datetime.now(TZ_INFO)


def get_nows():
    return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
