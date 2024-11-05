import os

from django.contrib.auth.models import User
from django.core.management import BaseCommand
from dotenv import load_dotenv

load_dotenv()


class Command(BaseCommand):
    """Команда для создания администратора."""

    def handle(self, *args, **options):
        username = os.environ.get("APP_USERNAME")
        user = User.objects.filter(username=username)

        if not user:
            User.objects.create_superuser(
                username=username, password=os.environ.get("APP_PASSWORD")
            )
