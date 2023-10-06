from config.settings import ES_CONNECTION



def submit_record(index, data):
    ES_CONNECTION.index(index, body=data)


def submit_record_auth(data):
    return submit_record(index="auth",data=data)

def submit_record_podcast_update(data):
    return submit_record(index="podcast_update",data=data)

def submit_record_requests(data):
    return submit_record(index="api_calls",data=data)
