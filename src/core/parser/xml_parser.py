from django.db.models import Model

from .utils import *



class RSSXMLParser:
    def __init__(self, rss_object, main_fields_model:Model):
        self.rss_object = rss_object
        self.rss_path_object = rss_object.main_fields_path
        self.main_fields = main_fields_model()

    @classmethod
    def update_init(cls, rss_object):
        return cls(rss_object, lambda x:rss_object.main_fields)


    def fill_rss(self):
        """fill self.rss_object based on the rss_path and rss_object.url"""
        main_content = get_rss_main_content(self.rss_object)
        rss = self.rss_object
        paths = self.rss_path_object
        main_fields = self.main_fields

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
    def __init__(self, rss_object, episode_model:Model):
        self.rss_object = rss_object
        self.episode_model = episode_model
        self.episode_paths = rss_object.episode_attributes_path


    def create_new_episode(self, new_episode_item:dict):

        episode = self.episode_model(rss=self.rss_object)

        for field in self.episode_paths._meta.fields:
            try:
                if attr:=getattr(self.episode_paths, field.name):
                    route:list = attr.split(" ")
                else:
                    continue
            except (TypeError,AttributeError):
                continue
            obj = new_episode_item
            while route:
                obj = obj[route.pop(0)]

            setattr(episode, field.name, obj)
        return episode

    def parse_all_episodes(self):
        episode_items = get_rss_episodes(self.rss_object)
        episode_objects = []
        for item in episode_items:
            episode = self.create_new_episode(item)
            episode_objects.append(episode)
        self.episode_model.objects.bulk_create(episode_objects)
