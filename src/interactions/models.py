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



class Notification(BaseModel):
    name = models.CharField(max_length=75)
    data = models.TextField()
    is_sent = models.BooleanField(default=False)

    def add_user(self, users:list[User]):
        user_notifications = [UserNotification(user=user, notification=self) for user in users]
        UserNotification.objects.bulk_create(user_notifications)


class UserNotification(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notification = models.ForeignKey(Notification, on_delete=models.PROTECT)
    # is_received = models.BooleanField(default=False)
    # is_read = models.BooleanField(default=False)
