import os
import json
import logging
from multiprocessing import Process

import pika
import django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()


from django.db import transaction

from config.settings import RABBIT_URL

from core.utils import get_nows
from accounts.models import UserTracking,User
from podcasts.models import PodcastRSS
from interactions.models import Notification,Subscribe,UserNotification
from podcasts.notification import PodcastUpdateNotificaiton

logger = logging.getLogger("elastic")




def track_user(data):
    """Save the latest login info of user in db"""
    user_id = data["user_id"]
    body = {
        "last_login" : data["timestamp"],
        "login_type" : data["action"],
        "user_agent" : data["user_agent"],
        "ip" : data["ip"],
    }
    user_track = UserTracking.objects.filter(user_id=user_id)
    if user_track.exists():
        if body["login_type"] == "login":
            body.update({"last_userlogin":body["last_login"]})
        user_track.update(**body)
    else:
        body.update({"last_userlogin":body["last_login"]})
        user_track = UserTracking.objects.create(
            user_id=user_id,
            **body
        )

    logger.info({
        "event_type": "auth",
        "user_id": user_id,
        "timestamp": get_nows(),
        "message": "user last activity saved",
        "action" : "system-track-user",
    })


def auth_notification(data):
    if data["action"] not in ("register", "login",):
        return
    notif_data = {
        "action": data["action"],
        "msg": f"Your latest activity: {data['action']}"
    }
    try:
        with transaction.atomic():
            notification = Notification.objects.create(name="auth", data=json.dumps(notif_data))
            user = User.objects.get(id=data["user_id"])
            UserNotification.objects.create(user=user, notification=notification)
    except:
        logger.error({
            "event_type":"notification",
            "name": "auth",
            "notif_data": data,
            "message": "could not create notification for user auth action",
            "user": data["user_id"],
        })
    else:
        logger.info({
            "event_type":"notification",
            "name":notification.name,
            "notif_data": notification.data,
            "user": user.id,
            "message": "User action notification created",
        })


def auth_callback(ch, method, properties, body):
    # consumer received auth queue callback
    data = json.loads(body)
    track_user(data)
    auth_notification(data)



def podcast_update_notification(body):
    """Create podcast update Notification objects based on received body"""
    data = json.loads(body)
    podcast_id = data["podcast_id"]
    episodes = data["new_episodes"]
    podcast = PodcastRSS.objects.get(id=podcast_id)

    user_notifications = []
    users_ids = []
    users = []

    notification = Notification(name="podcast_update", data=json.dumps({**data,"subject": "podcast Updated"}))
    for subscription in Subscribe.objects.filter(rss=podcast,notification=True).prefetch_related("user"):
        user_notifications.append(UserNotification(
            user = subscription.user,
            notification = notification
        ))
        users.append(subscription.user)
        users_ids.append(subscription.user.id)

    try:
        with transaction.atomic():
            notification.save()
            UserNotification.objects.bulk_create(user_notifications)
            PodcastUpdateNotificaiton(notification, users).send_bulk()
    except Exception as e: # BUG: what exception?
        logger.error({
            "event_type":"notification",
            "name": "podcast_update",
            "notif_body": str(data),
            "user": users_ids,
            "message": "did not create podcast update notification",
        })
    else:
        logger.info({
            "event_type":"notification",
            "name":"podcast_update",
            "notif_data": str(data),
            "user": users_ids,
            "message": "podcast update notification created",
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
