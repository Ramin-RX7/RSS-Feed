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
    if full_content.get("item"):
        full_content.pop("item")
    return full_content





class RSSXMLParser:
    def __init__(self, rss_object, main_fields_model):
        self.rss_object = rss_object
        self.rss_path_object = rss_object.main_fields_path
        self.main_fields_model = main_fields_model


    def fill_rss(self):
        """fill self.rss_object based on the rss_path and rss_object.url"""
        main_content = get_rss_main_content(self.rss_object)
        rss = self.rss_object
        paths = self.rss_path_object
        main_fields = self.main_fields_model()

        for field in self.rss_path_object._meta.fields:
            field_name = field.name

            try:
                if attr:=getattr(paths, field_name):
                    route:list = attr.split(" ")
                else:
                    continue
            except (TypeError,AttributeError):
                continue

            c = main_content.copy()
            while route:
                c = c[route.pop(0)]

            setattr(rss, field_name, c)

        main_fields.save()
        rss.main_fields = main_fields

        return rss




class EpisodeXMLParser:
    def __init__(self, rss_object, episode_model:type):
        self.rss_object = rss_object
        self.episode_model = episode_model
        self.episode_paths = rss_object.episode_attributes_path


    def create_new_episode(self, new_episode_item:dict):

        episode = self.episode_model(rss=self.rss_object)

        for field in self.episode_paths._meta.fields:

            elements_route = getattr(self.episode_paths, field).split(" ")

            obj = new_episode_item
            while elements_route:
                obj = obj[elements_route.pop(0)]

            setattr(episode, field, obj)
        return episode.save()
