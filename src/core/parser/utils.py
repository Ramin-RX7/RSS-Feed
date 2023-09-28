import requests

from core.lib import xmltodict




def get_rss_content(rss_object) -> dict:
    url = rss_object.url
    response = requests.get(url)
    o = xmltodict.parse(response.text)
    main_content = o["rss"]["channel"]
    return main_content


def get_rss_main_content(rss_object):
    full_content = get_rss_content(rss_object)
    # if full_content.get("item"):
    full_content.pop("item")
    return full_content


def get_rss_episodes(rss_object):
    full_content = get_rss_content(rss_object)
    return full_content.get("item")


def get_unparsed_episodes(rss_object, episodes_model):
    db_episodes_count = episodes_model.objects.filter(rss=rss_object).count()
    live_episodes = get_rss_episodes(rss_object)
    live_episodes_count = len(live_episodes)
    diff = live_episodes_count - db_episodes_count
    if diff > 0:
        return (live_episodes[:diff])[::-1]
    else:
        return []
