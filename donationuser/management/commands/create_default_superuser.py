from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

class Command(BaseCommand):
    help = 'Creates a default superuser from environment variables if it does not exist.'

    def handle(self, *args, **options):
        User = get_user_model()
        username = os.environ.get('ADMIN_USERNAME')
        email = os.environ.get('ADMIN_EMAIL')
        password = os.environ.get('ADMIN_PASSWORD')

        if not all([username, email, password]):
            self.stdout.write(self.style.WARNING(
                'Skipping superuser creation: ADMIN_USERNAME, ADMIN_EMAIL, and ADMIN_PASSWORD environment variables must be set.'
            ))
            return

        if not User.objects.filter(username=username).exists():
            self.stdout.write(self.style.SUCCESS(f'Creating superuser {username}...'))
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f'Superuser {username} created successfully!'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Superuser {username} already exists.')) 