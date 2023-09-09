import requests
import xmltodict

from django.shortcuts import render
from django.http import HttpResponse

from . import utils
from .models import PodcastEpisode,PodcastRSS


def test(request):

    url = "https://rss.art19.com/apology-line"
    response = requests.get(url)

    o = xmltodict.parse(response.text)
    items = o["rss"]["channel"]["item"]
    item = items[0]

    rss = PodcastRSS.objects.get(id=1)
    parser = utils.XMLParser(rss, PodcastEpisode)
    parser.create_new_episode(item)
    return HttpResponse("OK")
