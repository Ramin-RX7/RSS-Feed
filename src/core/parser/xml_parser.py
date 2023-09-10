import requests

from core import xmltodict




def get_rss_content(rss_object) -> dict:
    url = rss_object.url
    response = requests.get(url)

    o = xmltodict.parse(response.text)
    main_content = o["rss"]["channel"]

    return main_content

def get_rss_main_content(rss_object):
    full_content = get_rss_content(rss_object)
    if full_content.get("item"):
        full_content.pop("item")
    return full_content



