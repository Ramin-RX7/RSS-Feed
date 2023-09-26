import time
import logging

from celery import shared_task, group, chord

from .models import PodcastRSS



logger = logging.getLogger('celery-logger')


MAX_CONCURRENCY = 3
MAX_RETRY = 4




def divide_tasks(tasks, n):
    return [group(tasks[i:i+n]) for i in range(0, len(tasks), n)]





@shared_task
def update_podcast(podcast_id, retry_count=0):
    podcast = PodcastRSS.objects.get(id=podcast_id)
    try:
        podcast.update_episodes()
        logger.info(f'Successfully updated podcast: {podcast.name}')
        # return True
    except Exception as e:
        if retry_count < MAX_RETRY:
            logger.warning(f'Failed to update podcast: {podcast.name}. Retrying...')
            # raise update_podcast.retry(exc=e, countdown=(2**retry_count))
            time.sleep(2**retry_count)
            update_podcast(podcast_id, retry_count+1)
        else:
            logger.error(f'Retries exhausted for podcast: {podcast.name}. Moving on...')
            logger.error(f'{type(e).__name__}: {e}')



@shared_task
def update_podcasts_episodes():
    podcasts = PodcastRSS.objects.all()

    tasks = [update_podcast.s(podcast.id) for podcast in podcasts]
    task_groups = divide_tasks(tasks, MAX_CONCURRENCY)

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
    # print(f"in pro res: {results}")

class PodcastRequest(Request):
    'A minimal custom request to log failures and hard time limits.'

    def on_failure(self, exc_info, send_failed_event=True, return_ok=False):
        if type(exc_info.exception) != Retry:
            error_name = type(exc_info.exception).__name__
            message = str(exc_info.exception)
            logger.critical(
                f'Failed to update podcast: : "{error_name}: {message}". Failed',
            )
        return super().on_failure(
            exc_info,
            send_failed_event=send_failed_event,
            return_ok=return_ok
        )
    def on_retry(self, exc_info):
        error_name = type(exc_info.exception.exc).__name__
        message = str(exc_info.exception.exc)
        logger.error(
            f'Failed to update podcast: : "{error_name}: {message}". retrying',
        )
        return super().on_retry(exc_info)
    def on_success(self, failed__retval__runtime, **kwargs):
        logger.info(kwargs)
        logger.info("successful update")
        return super().on_success(failed__retval__runtime, **kwargs)

