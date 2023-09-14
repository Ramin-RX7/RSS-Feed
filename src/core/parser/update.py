from .utils import *
from .xml_parser import *
from podcasts.models import PodcastRSS,PodcastEpisode



def update_rss(rss_object:PodcastRSS):
    parser = RSSXMLParser.update_init(rss_object)
    rss = parser.fill_rss()
    rss.save()


