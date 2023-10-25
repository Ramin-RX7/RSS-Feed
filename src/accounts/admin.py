from django.contrib import admin,messages

from .models import User,UserTracking
from .forms import ChangeForm,UserAddForm



admin.site.register(UserTracking)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["username", "created_at"]
    actions = ["block_user","unblock_user"]

    def get_form(self, request, obj=None, **kwargs):
        if obj is not None:
            return ChangeForm
        return UserAddForm

    @admin.action(description="Blocks user login attempts to website")
    def block_user(self, request, queryset):
        for user in queryset:
            user.block()
        self.message_user(
            request,
            'User has been blocked successfully',
            level=messages.SUCCESS
        )

    @admin.action(description="Unblock user login attempts")
    def unblock_user(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(
            request,
            'User has been unblocked successfully',
            level=messages.SUCCESS
        )
