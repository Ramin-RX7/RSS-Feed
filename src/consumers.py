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


connection = pika.BlockingConnection(pika.ConnectionParameters('rabbit'))





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

def auth_listener():
    channel = connection.channel()
    channel.queue_declare(queue='auth')
    channel.basic_consume(queue='auth', on_message_callback=auth_callback, auto_ack=True)
    channel.start_consuming()

