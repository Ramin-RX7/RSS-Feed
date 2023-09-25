from .models import PodcastRSS

from celery import shared_task, group, chord




def divide_tasks(seq, n):
    q, r = divmod(len(seq), n)
    ret = []
    stop = 0
    for i in range(1, n + 1):
        start = stop
        stop += q + 1 if i <= r else q
        ret.append(group(seq[start:stop]))
    return ret





MAX_CONCURRENCY = 3
MAX_RETRY = 4

# @shared_task(autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={'max_retries': 6}, retry_jitter=True)
@shared_task
def update_podcast(podcast_id, retry_count=0):
    podcast = PodcastRSS.objects.get(id=podcast_id)
    try:
        podcast.update_episodes()
        return True
    except Exception as e:
        if retry_count < MAX_RETRY:
            raise update_podcast.retry(exc=e, countdown=(2**retry_count))
        else:
            pass



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
