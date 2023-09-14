from django import forms
from django.db import models
from django.db.models.fields.related import RelatedField

from core.models import BaseModel
from .models import PodcastRSS,PodcastRSSPaths,PodcastEpisode,PodcastEpisodePaths



BASE_MODEL_FIELDS = [field.name for field in BaseModel._meta.fields]
DISSALLOWED_FIELDS = ["id", "name", "url"]
# ID_FIELD = 'id'


def is_field_allowed(field):
    if not isinstance(field, models.Field):
        return False
    if isinstance(field, RelatedField):
        return False
    if field.name in BASE_MODEL_FIELDS:
        return False
    if field.name in DISSALLOWED_FIELDS:
        return False
    return True



class XXXCreateRSSForm(forms.ModelForm):
    RSS_model = PodcastRSS
    fields = []

    class Meta:
        model = PodcastRSS
        fields = []


    def __init__(self, *args, **kwargs):
        self.get_main_fields(self.RSS_model)
        return super().__init__(*args,**kwargs)

    def get_main_fields(self, model=None):
        """get all needed main fields of the RSS model (This means any field defined in the model except name, url and relations)

        Args:
            model (_type_, optional): _description_. Defaults to None.
        """
        if model is None:
            model = self.RSS_model

        fields = []
        for field in model._meta.fields:
            if is_field_allowed(field):
                print(field)
                # setattr(self, f"{field.name}_path", forms.CharField(max_length=100))
                self.Meta.fields.append(f"{field.name}_path", forms.CharField(max_length=100))
                # self.fields.append(field)









class CreateRSSForm(forms.ModelForm):
    RSS_model = PodcastRSS
    # fields = []

    class Meta:
        model = PodcastRSS
        fields = ["name", "url", "main_fields_path", "episode_attributes_path"]


