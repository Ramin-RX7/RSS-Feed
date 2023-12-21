import logging

from celery import shared_task, group, chain, Task

from config.settings import CELERY_MAX_CONCURRENCY, CELERY_MAX_RETRY
from core import rabbitmq
from core.utils import get_nows
from .models import PodcastRSS



logger = logging.getLogger("elastic")



def divide_tasks(tasks, n):
    return [group(tasks[i : i + n]) for i in range(0, len(tasks), n)]


class BasePodcastTask(Task):
    autoretry_for = (Exception,)
    max_retries = CELERY_MAX_RETRY
    retry_backoff = True  # 1
    retry_jitter = False
    acks_late = True
    # Keep code below commented for future logic changes
    # retry_backoff_max = 32
    # default_retry_delay = 1

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        error_name = type(exc).__name__
        message = str(exc)
        logger.critical({"event_type": "podcast_update",
            "message": "Failed to update podcast",
            "podcast_id": kwargs["podcast_id"],
            "error_name": error_name,
            "error_message": message,
            "args": args,
            "kwargs": kwargs,
        })
        return super().on_failure(exc, task_id, args, kwargs, einfo)

    def on_success(self, retval, task_id, args, kwargs):
        logger.info({"event_type": "podcast_update",
            "message": "podcast updated",
            "podcast_id": kwargs["podcast_id"],
            "args": args,
            "kwargs": kwargs,
        })
        return super().on_success(retval, task_id, args, kwargs)

    def on_retry(self, exc, task_id, args, kwargs, einfo):
        error_name = type(exc).__name__
        message = str(exc)
        logger.error({"event_type": "podcast_update",
            "message": "Failed to update podcast, retrying...",
            "podcast_id": kwargs["podcast_id"],
            "error_name": error_name,
            "error_message": message,
            "args": args,
            "kwargs": kwargs,
        })
        return super().on_retry(exc, task_id, args, kwargs, einfo)


@shared_task(base=BasePodcastTask, bind=True)
def update_podcast(self, podcast_id, explicit_request=False):
    # XXX: Also check self.request.retries for simpler logic
    request_type = "explicit" if explicit_request else "scheduled"
    logger.info({"event_type": "podcast_update",
        "message": f"{request_type} update request recieved",
        "podcast_id": podcast_id,
        "args": [],
        "kwargs": {},
    })
    podcast = PodcastRSS.objects.get(id=podcast_id)
    new_episodes = podcast.update_episodes()
    if new_episodes:  # XXX: publish an updated podcast with no new episodes?
        data = {
            "timestamp": get_nows(),
            "podcast_id": podcast_id,
            "new_episodes": list(map(lambda episode: episode.id, new_episodes)),
        }
        rabbitmq.publish_podcast_update(data)
    return len(new_episodes)


@shared_task
def update_podcasts_episodes(explicit_request=False):
    # XXX: Log update podcast request?
    if explicit_request:
        logger.info({"event_type": "podcast_update",
            "message": "explicit update request recieved (for all rss)",
            "podcast_id": 0,
            "args": [],
            "kwargs": {},
        })
    podcasts = PodcastRSS.objects.all()

    tasks = [
        update_podcast.s(podcast_id=podcast.id, explicit_request=explicit_request)
        for podcast in podcasts
    ]
    task_groups = divide_tasks(tasks, CELERY_MAX_CONCURRENCY)

    initial_chain = chain()
    for task_group in task_groups:
        initial_chain = initial_chain | task_group

    initial_chain.apply_async()
