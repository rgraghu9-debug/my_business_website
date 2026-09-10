"""
Management command to create a default superuser for development.
Run: python manage.py create_admin
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Create a default admin superuser for development"

    def handle(self, *args, **options):
        User = get_user_model()
        username = "admin"
        password = "admin123"
        email = "admin@weddingcards.local"

        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(f'User "{username}" already exists.')
            )
        else:
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(
                self.style.SUCCESS(
                    f'Superuser "{username}" created successfully.\n'
                    f"  Username: {username}\n"
                    f"  Password: {password}\n"
                    f"  Login at: http://127.0.0.1:8000/admin/"
                )
            )
