from django.contrib import admin

from .models import Notification, UserNotification, Like, Subscribe

admin.site.register(Notification)
admin.site.register(UserNotification)
admin.site.register(Like)
admin.site.register(Subscribe)
