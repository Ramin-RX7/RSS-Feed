import json
import os
from datetime import datetime
from multiprocessing import Process
from threading import Thread

import pika
import django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()


from config.settings import RABBIT_URL

from core import elastic
from accounts.models import UserTracking
from podcasts.models import PodcastRSS
from interactions.models import Notification,Subscribe,UserNotification





def track_user(data):
    """Save the latest login info of user in db"""
    # assert data["type"] in ("register", "login", "access", "refresh", "other")
    user_id = data["user_id"]
    user_track = UserTracking.objects.filter(user_id=user_id)
    if user_track.exists():
        user_track = user_track.get()
    else:
        user_track = UserTracking(user_id=user_id)
        user_track.last_userlogin = datetime.fromtimestamp(0)

    user_track.last_login = datetime.fromtimestamp(data["timestamp"])
    user_track.login_type = data["method"]
    user_track.user_agent = data["user_agent"]
    user_track.ip = data["ip"]
    if user_track.login_type == "login":
        user_track.last_userlogin = user_track.last_login
    user_track.save()


def log_signin(data):
    """Log user login data"""
    elastic.submit_record_auth(data)
    # use elastic search to log data


def auth_callback(ch, method, properties, body):
    data = json.loads(body)
    track = Thread(target=track_user, args=(data,))
    log = Thread(target=log_signin, args=(data,))
    log.start()
    track.start()




def podcast_update_notification(body):
    """Create podcast update Notification objects based on received body"""
    data = json.loads(body)
    podcast_id = data["podcast_id"]
    episodes = data["new_episodes"]
    podcast = PodcastRSS.objects.get(id=podcast_id)

    notification = Notification.objects.create(
        name = "Podcast_Update",
        data = body
    )
    user_notifications = []
    for subscription in Subscribe.objects.filter(rss=podcast,notification=True):
        user_notifications.append(UserNotification(
            user = subscription.user,
            notification = notification
        ))
    UserNotification.objects.bulk_create(user_notifications)
    # UserNotification.objects.bulk_create([
    #     UserNotification(
    #         user=subscription.user,
    #         notification=notification,
    #     ) for subscription in Subscribe.objects.filter(rss=podcast,notification=True)
    # ])


def podcast_log(data):
    """Log podcast updates"""
    elastic.submit_record_podcast_update(data)
    # use elastic search to log data


def podcast_update_callback(ch, method, properties, body):
    data = json.dumps(body)
    notif = Thread(target=podcast_update_notification, args=(body,))
    log = Thread(target=podcast_log, args=(data,))
    log.start()
    notif.start()
    log.join()
    notif.join()





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
