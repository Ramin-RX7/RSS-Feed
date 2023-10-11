from django.contrib import admin

from .models import Notification,UserNotification

admin.site.register(Notification)
admin.site.register(UserNotification)
