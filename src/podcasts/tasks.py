import time
import logging

from celery import shared_task, group, chord, chain, Task
from celery.worker.request import Request
from celery.exceptions import Retry

from django.apps import apps

from config.settings import CELERY_MAX_CONCURRENCY,CELERY_MAX_RETRY
from core import rabbitmq
from core.utils import get_nows
from .models import PodcastRSS



logger = logging.getLogger('elastic')




def divide_tasks(tasks, n):
    return [group(tasks[i:i+n]) for i in range(0, len(tasks), n)]




class BasePodcastTask(Task):
    autoretry_for = (Exception,)
    max_retries = CELERY_MAX_RETRY
    # retry_backoff_max = 32
    # default_retry_delay = 1
    retry_backoff = True  # 1
    retry_jitter = False
    acks_late=True

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        error_name = type(exc).__name__
        message = str(exc)
        logger.critical({"event_type": "podcast_update",
            "message" : "Failed to update podcast",
            "podcast_id" : kwargs["podcast_id"],
            "error_name" : error_name,
            "error_message" : message,
            "args" : args,
            "kwargs" : kwargs,
        })
        return super().on_failure(
            exc, task_id, args, kwargs, einfo
        )

    def on_success(self, retval, task_id, args, kwargs):
        logger.info({"event_type": "podcast_update",
            "message" : "podcast updated",
            "podcast_id" : kwargs["podcast_id"],
            "args" : args,
            "kwargs" : kwargs,
        })
        return super().on_success(retval, task_id, args, kwargs)

    def on_retry(self, exc, task_id, args, kwargs, einfo):
        error_name = type(exc).__name__
        message = str(exc)
        logger.error({"event_type": "podcast_update",
            "message" : "Failed to update podcast, retrying...",
            "podcast_id" : kwargs["podcast_id"],
            "error_name" : error_name,
            "error_message" : message,
            "args" : args,
            "kwargs" : kwargs,
        })
        return super().on_retry(exc, task_id, args, kwargs, einfo)




@shared_task(base=BasePodcastTask, bind=True)
def update_podcast(self, podcast_id):
    # self.request.retries
    podcast = PodcastRSS.objects.get(id=podcast_id)
    new_episodes = podcast.update_episodes()
    if new_episodes:  #? Should I publish that a podcast updated with no new episodes?
        data = {
            "timestamp": get_nows(),
            "podcast_id": podcast_id,
            "new_episodes": new_episodes
        }
        rabbitmq.publish_podcast_update(data)
    # logger.info(f'Successfully updated podcast: {podcast.name}')



@shared_task
def update_podcasts_episodes():
    # logger.info("Request to update podcasts episodes")
    podcasts = PodcastRSS.objects.all()

    tasks = [update_podcast.s(podcast_id=podcast.id) for podcast in podcasts]
    task_groups = divide_tasks(tasks, CELERY_MAX_CONCURRENCY)

    initial_chain = chain()
    for task_group in task_groups:
        initial_chain = initial_chain | task_group

    # result = initial_chain | process_parsing_results.s()
    initial_chain.apply_async()

# @shared_task
# def update_podcasts_episodes():
    # podcasts = PodcastRSS.objects.all()
    # for podcast in podcasts:
        # update_podcast.delay(podcast.id)


# @shared_task
# def process_parsing_results(results:list[dict[int:bool]]):
#     print(f"in pro res: {results}")
