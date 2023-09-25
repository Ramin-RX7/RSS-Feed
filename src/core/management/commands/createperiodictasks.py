from celery import Celery

from django.core.management.base import BaseCommand
from django_celery_beat.models import PeriodicTask, IntervalSchedule



class Command(BaseCommand):
    help = 'Define and schedule a periodic task for Celery Beat'

    def handle(self, *args, **kwargs):
        celery_app = Celery('your_project')
        celery_app.config_from_object('django.conf:settings', namespace='CELERY')
        interval,_ = IntervalSchedule.objects.get_or_create(every=1, period=IntervalSchedule.HOURS)
        task = PeriodicTask.objects.create(
            interval=interval,
            name='Podcast_Episode_Updater',
            task='podcasts.tasks.update_podcasts_episodes',  # Replace with your actual Celery task
        )
        self.stdout.write(self.style.SUCCESS(f'Successfully defined and scheduled the periodic task "{task}"'))
