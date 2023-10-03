from django.db import models

from core.models import BaseModel
from accounts.models import User
from podcasts.models import PodcastRSS,PodcastEpisode




class Subscribe(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rss = models.ForeignKey(PodcastRSS, on_delete=models.CASCADE)
    notification = models.BooleanField(default=False)
    class Meta:
        unique_together = ('user', 'rss',)



class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    episode = models.ForeignKey(PodcastEpisode, on_delete=models.CASCADE)
    class Meta:
        unique_together = ('user', 'episode',)



class Comment(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    episode = models.ForeignKey(PodcastEpisode, on_delete=models.CASCADE)
    content = models.CharField(max_length=150)
