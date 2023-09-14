from .utils import *
from .xml_parser import *
from podcasts.models import PodcastRSS,PodcastEpisode



def update_rss(rss_object:PodcastRSS):
    parser = RSSXMLParser.update_init(rss_object)
    rss = parser.fill_rss()
    rss.save()


def update_episodes(rss_object:PodcastRSS, episodes_model:PodcastEpisode):
    live_episodes = get_rss_episodes(rss_object)
    db_episode = episodes_model.objects.filter(rss=rss_object)

    diff = len(live_episodes) > db_episode.count()
    print(diff)
    if diff > 0:
        unparsed_episodes = live_episodes[:diff]
        parser = EpisodeXMLParser()
        new_episode_objects = parser.parse_multiple_episodes(unparsed_episodes)
        episodes_model.objects.bulk_create(new_episode_objects)
    elif diff == 0:
        print("Up to date")
        return
    else: raise SystemError("How?! (This happens when older episodes get deleted)")
