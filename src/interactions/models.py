from django.db import models

from core.models import BaseModel
from accounts.models import User
from podcasts.models import PodcastRSS,PodcastEpisode




class Subscribe(BaseModel):
    user = models.ForeignKey(User)
    rss = models.ForeignKey(PodcastRSS)



class Like(models.Model):
    user = models.ForeignKey(User)
    episode = models.ForeignKey(PodcastEpisode)


class Comment(BaseModel):
    user = models.ForeignKey(User)
    episode = models.ForeignKey(PodcastEpisode)
    content = models.CharField(max_length=150)
