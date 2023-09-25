import logging

from celery import shared_task, group, chord

from .models import PodcastRSS


logger = logging.getLogger('celery-logger')


MAX_CONCURRENCY = 3
MAX_RETRY = 4




def divide_tasks(seq, n):
    q, r = divmod(len(seq), n)
    ret = []
    stop = 0
    for i in range(1, n + 1):
        start = stop
        stop += q + 1 if i <= r else q
        ret.append(group(seq[start:stop]))
    return ret




# @shared_task(autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={'max_retries': 6}, retry_jitter=True)
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
            raise update_podcast.retry(exc=e, countdown=(2**retry_count))
        else:
            logger.error(f'Retries exhausted for podcast: {podcast.name}. Moving on...')



@shared_task
def update_podcasts_episodes():
    podcasts = PodcastRSS.objects.all()

    tasks = [update_podcast.s(podcast.id) for podcast in podcasts]
    task_groups = divide_tasks(tasks, MAX_CONCURRENCY)

    print(f"task_group {task_groups}")
    # chords = [chord(task_group)(process_parsing_results.s()) for task_group in task_groups]
    for g in task_groups: g()



# @shared_task
# def process_parsing_results(results:list[dict[int:bool]]):
    # print(f"in pro res: {results}")
