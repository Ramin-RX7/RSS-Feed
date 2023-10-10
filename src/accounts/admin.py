from django.contrib import admin

from .models import User,UserTracking
from .forms import ChangeForm,UserAddForm



admin.site.register(UserTracking)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["username", "created_at"]

    def get_form(self, request, obj=None, **kwargs):
        if obj is not None:
            return ChangeForm
        return UserAddForm
