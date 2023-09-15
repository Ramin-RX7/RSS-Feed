from django.core.management.base import BaseCommand

from accounts.models import User


class Command(BaseCommand):
    help = 'Create required configs/models before first run'

    def handle(self, *args, **options):
        # User.objects.delete()
        user = User.objects.create_superuser(username="admin", email="admin@admin.admin", password="admin")
