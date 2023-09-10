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





class RSSXMLParser:
    def __init__(self, rss_object):
        self.rss_object = rss_object
        self.rss_path_object = rss_object.main_fields_path


    def fill_rss(self):
        """fill self.rss_object based on the rss_path and rss_object.url"""
        main_content = get_rss_main_content(self.rss_object)
        rss = self.rss_object
        paths = self.rss_path_object

        for field in self.rss_path_object._meta.fields:
            field_name = field.name

            try:
                route:list = getattr(paths, field_name).split(" ")
            except (TypeError,AttributeError):
                continue

            c = main_content.copy()
            while route:
                c = c[route.pop(0)]

            setattr(self.rss_object, field_name, c)

        return rss



