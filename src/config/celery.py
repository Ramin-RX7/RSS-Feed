import os
from celery import Celery
from celery.schedules import crontab



os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")


app = Celery("app")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "update-podcasts-every-hour": {
        "task": "podcasts.tasks.update_podcasts_episodes",
        "schedule": crontab(minute="*/15"),  # every 15 minutes
    },
}
