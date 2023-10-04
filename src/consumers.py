import json
import os
from datetime import datetime
from multiprocessing import Process
from threading import Thread

import pika
import django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()


from accounts.models import UserTracking
from podcasts.models import PodcastRSS
from interactions.models import Notification,Subscribe





def track_user(data):
    """Save the latest login info of user in db"""
    # assert data["type"] in ("register", "login", "access", "refresh", "other")
    user_id = data["user_id"]
    user_tracking,created = UserTracking.objects.get_or_create(user_id=user_id)
    user_tracking.last_login = datetime.fromtimestamp(data["time"])
    user_tracking.login_type = data["type"]
    user_tracking.user_agent = data["user_agent"]
    user_tracking.ip = data["ip"]
    if user_tracking.login_type == "login":
        user_tracking.last_userlogin = user_tracking.last_login
    user_tracking.save()

def log_signin(data):
    """Log user login data"""
    # use elastic search to log data

def auth_callback(ch, method, properties, body):
    data = json.loads(body)
    track_user(data)
    log_signin(data)





def podcast_update_notification(body):
    """Create podcast update Notification objects based on received body"""
    data = json.loads(body)
    podcast_id = data["podcast_id"]
    episodes = data["episodes"]
    podcast = PodcastRSS.objects.get(id=podcast_id)

    notifications = []
    for subscription in Subscribe.objects.filter(rss=podcast,notification=True):
        user = subscription.user
        notifications.append(Notification(
            name = "Podcast Update",
            user = user,
            data = body
        ))
    Notification.objects.bulk_create(notifications)
    # Notification.objects.bulk_create([
    #     Notification(user=subscription.user,title="Podcast Update", data=body) for
    #         subscription in Subscribe.objects.filter(rss=podcast,notification=True)
    # ])

def podcast_log(body):
    """Log podcast updates"""
    # use elastic search to log data

def podcast_update_callback(ch, method, properties, body):
    notif = Thread(target=podcast_update_notification, args=(body,))
    log = Thread(target=podcast_log, args=(body,))
    log.start()
    notif.start()
    log.join()
    notif.join()






def auth_listener():
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbit'))
    channel = connection.channel()
    channel.queue_declare(queue='auth')
    channel.basic_consume(queue='auth', on_message_callback=auth_callback, auto_ack=True)
    channel.start_consuming()

def podcast_update_listener():
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbit'))
    channel = connection.channel()
    channel.queue_declare(queue='podcast_update')
    channel.basic_consume(queue='podcast_update', on_message_callback=podcast_update_callback, auto_ack=True)
    channel.start_consuming()





if __name__ == "__main__":
    podcast_update = Process(target=podcast_update_listener)
    auth = Process(target=auth_listener)

    podcast_update.start()
    auth.start()