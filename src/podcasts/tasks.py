import logging

from celery import shared_task, group, chord, chain, Task
from celery.worker.request import Request
from celery.exceptions import Retry

from django.apps import apps

from config.settings import CELERY_MAX_CONCURRENCY,CELERY_MAX_RETRY
from .models import PodcastRSS



logger = logging.getLogger('celery-logger')




def divide_tasks(tasks, n):
    return [group(tasks[i:i+n]) for i in range(0, len(tasks), n)]




class PodcastRequest(Request):
    'A minimal custom request to log failures and hard time limits.'

    def on_failure(self, exc_info, send_failed_event=True, return_ok=False):
        if type(exc_info.exception) != Retry:
            error_name = type(exc_info.exception).__name__
            message = str(exc_info.exception)
            podcast_id = self.kwargs["podcast_id"]
            submit_record_podcast_update({
                "title" : "fail",
                "message" : "Failed to update podcast",
                "podcast_id" : podcast_id,
                "error_name" : error_name,
                "error_message" : message,
                "args" : self.args,
                "kwargs" : self.kwargs,
            })
        return super().on_failure(
            exc_info,
            send_failed_event=send_failed_event,
            return_ok=return_ok
        )
    def on_retry(self, exc_info):
        error_name = type(exc_info.exception.exc).__name__
        message = str(exc_info.exception.exc)
        podcast_id = self.kwargs["podcast_id"]
        submit_record_podcast_update({
            "title" : "fail",
            "message" : "Failed to update podcast, retrying...",
            "podcast_id" : podcast_id,
            "error_name" : error_name,
            "error_message" : message,
            "args" : self.args,
            "kwargs" : self.kwargs,
        })
        return super().on_retry(exc_info)
    def on_success(self, failed__retval__runtime, **kwargs):
        # logger.info(kwargs)
        submit_record_podcast_update({
            "title" : "success",
            "message" : "podcast updated",
            "podcast_id" : self.kwargs["podcast_id"],
            "args" : self.args,
            "kwargs" : self.kwargs,
        })
        return super().on_success(failed__retval__runtime, **kwargs)


class BaseTask(Task):
    Request = PodcastRequest
    autoretry_for = (Exception,)
    max_retries = CELERY_MAX_RETRY
    # retry_backoff_max = 32
    # default_retry_delay = 1
    # retry_kwargs = {'max_retries': 5}   # READMORE
    retry_backoff = True  # 1
    retry_jitter = False



@shared_task(base=BaseTask, bind=True)
def update_podcast(self, podcast_id):
    # logger.info(f"XXXXXX - {self.request.retries}, {podcast_id}")
    podcast = PodcastRSS.objects.get(id=podcast_id)
    podcast.update_episodes()
    # raise ValueError("wtf")
    logger.info(f'Successfully updated podcast: {podcast.name}')



@shared_task
def update_podcasts_episodes():
    logger.info("Request to update podcasts episodes")
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


@shared_task
def process_parsing_results(results:list[dict[int:bool]]):
    print(f"in pro res: {results}")
