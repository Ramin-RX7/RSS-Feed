import os
import time
import json
from datetime import datetime
from multiprocessing import Process

import pika
import django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()


from django.db import transaction

from config.settings import RABBIT_URL

from core import elastic
from accounts.models import UserTracking,User
from podcasts.models import PodcastRSS
from interactions.models import Notification,Subscribe,UserNotification





def track_user(data):
    """Save the latest login info of user in db"""
    user_id = data["user_id"]

    user_track, updated = UserTracking.objects.update_or_create(user_id=user_id, defaults={
        "last_login" : datetime.fromtimestamp(data["timestamp"]),
        "login_type" : data["action"],
        "user_agent" : data["user_agent"],
        "ip" : data["ip"],
    })
    if user_track.login_type == "login":
        user_track.last_userlogin = user_track.last_login
    user_track.save()

    elastic.submit_record("auth", "info",{  # No log for failure of this function
        "user_id": user_id,
        "timestamp": time.time(),
        "message": "user last activity saved",
        "action" : "system-track-user",
    })


def auth_notification(data):
    if data["action"] not in ("register", "login",):
        return
    with transaction.atomic():
        notification = Notification.objects.create(name="Auth", data=json.dumps({
            "action": data["action"],
            "msg": f"Your latest activity: {data['action']}"
        }))
        user = User.objects.get(id=data["user_id"])
        UserNotification.objects.create(user=user, notification=notification)
        elastic.submit_record("auth", "info",{   # This has to be notification log (not podcast_update)
            "type":"success",
            "message": "User action notification created",
            "user": user.id
        })
        return
    elastic.submit_record("auth", "info", {   # This has to be notification log (not podcast_update)
        "type": "fail",
        "message": "could not create notification for user auth action",
        "notif_body": body,
        "user": data["user_id"],
    })


def auth_callback(ch, method, properties, body):
    # consumer received auth queue callback
    data = json.loads(body)
    track_user(data)
    # auth_notification(data)



def podcast_update_notification(body):
    """Create podcast update Notification objects based on received body"""
    data = json.loads(body)
    podcast_id = data["podcast_id"]
    episodes = data["new_episodes"]
    podcast = PodcastRSS.objects.get(id=podcast_id)

    with transaction.atomic():
        notification = Notification.objects.create(name="Podcast_Update", data=body)
        user_notifications = []
        for subscription in Subscribe.objects.filter(rss=podcast,notification=True):
            user_notifications.append(UserNotification(
                user = subscription.user,
                notification = notification
            ))
        UserNotification.objects.bulk_create(user_notifications)
        elastic.submit_record("podcast_update", "info",{   # This has to be notification log (not podcast_update)
            "type":"success",
            "message": "podcast update notification created",
        })
        return
    elastic.submit_record("podcast_update", "info", {   # This has to be notification log (not podcast_update)
        "type": "fail",
        "message": "did not create podcast update notification",
        "notif_body": body
    })


def podcast_update_callback(ch, method, properties, body):
    # consumer received podcast update callback
    data = json.loads(body)
    podcast_update_notification(body)





def auth_listener():
    connection = pika.BlockingConnection(RABBIT_URL)
    channel = connection.channel()
    channel.queue_declare(queue='auth')
    channel.basic_consume(queue='auth', on_message_callback=auth_callback, auto_ack=True)
    channel.start_consuming()

def podcast_update_listener():
    connection = pika.BlockingConnection(RABBIT_URL)
    channel = connection.channel()
    channel.queue_declare(queue='podcast_update')
    channel.basic_consume(queue='podcast_update', on_message_callback=podcast_update_callback, auto_ack=True)
    channel.start_consuming()




if __name__ == "__main__":
    podcast_update = Process(target=podcast_update_listener)
    auth = Process(target=auth_listener)

    podcast_update.start()
    auth.start()



def reconnect_on_fail(method):
    def wrapper(self, *args, **kwargs):
        try:
            getattr(self, method.__name__)(*args, **kwargs)
        except:  # BUG: Except what exception?
            self.__init__()
            getattr(self, method.__name__)(*args, **kwargs)
    return wrapper

class BaseConsumer:
    def __init__(self, queue) -> None:
        self.connection = pika.BlockingConnection(RABBIT_URL)
        self.channel = self.connection.channel()
        self.queue = self.channel.queue_declare(queue='auth')

    def _consume(self):
        self.channel.basic_consume(queue='auth', on_message_callback=auth_callback, auto_ack=True)
        self.channel.start_consuming()

    def consume(self):
        while True:
            self._consume()
            self.__init__(queue=self.queue)
