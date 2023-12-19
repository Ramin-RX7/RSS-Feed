from accounts.models import User
from podcasts.models import PodcastRSS
from lib.notification.email import EmailNotification



class PodcastUpdateNotificaiton(EmailNotification):
    def get_message(self, user: User):
        data = self.get_notification_data()
        podcast_title = PodcastRSS.objects.get(id=data["podcast_id"]).main_fields.title
        episodes_count = len(data["new_episodes"])
        return f"""Hey {user.username}, {podcast_title} has received {episodes_count} new episodes"""
