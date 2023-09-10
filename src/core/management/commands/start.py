from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Create required configs/models before first run'

    def handle(self, *args, **options):
        import os
        os.remove("./db.sqlite3")
        os.remove("./podcasts/migrations/0001_initial.py")
        os.system("python manage.py makemigrations podcasts")
        os.system("python manage.py migrate")
        user = User.objects.create_superuser(username="admin", email="admin@admin.admin", password="admin")
