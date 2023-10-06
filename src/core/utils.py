def get_request_data(request):
    try:
        request_data = request.data
    except AttributeError as _:
        if request.method in ("GET","POST"):
            request_data = getattr(request, request.method)
        else:
            request_data = None

    return request_data
