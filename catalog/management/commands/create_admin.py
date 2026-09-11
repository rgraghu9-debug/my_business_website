"""
Management command to create or update the superuser account.
Run: python manage.py create_admin
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Create or update admin superuser credentials"

    def handle(self, *args, **options):
        User = get_user_model()
        username = "gangothri"
        password = "8585"
        email = "gangothri@siddhivinayakcards.com"

        user, created = User.objects.get_or_create(
            username=username,
            defaults={"email": email, "is_staff": True, "is_superuser": True}
        )
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save()

        action = "Created" if created else "Updated"
        self.stdout.write(
            self.style.SUCCESS(
                f'Superuser "{username}" {action} successfully.\n'
                f"  Username: {username}\n"
                f"  Password: {password}\n"
                f"  Staff: {user.is_staff}, Superuser: {user.is_superuser}"
            )
        )
