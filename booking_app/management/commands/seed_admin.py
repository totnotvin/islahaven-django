from django.core.management.base import BaseCommand
from django.contrib.auth.models import User as DjangoUser
from booking_app.models import User as AppUser


class Command(BaseCommand):
    help = 'Seeds the database with an admin user'

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            type=str,
            default='admin',
            help='Admin username (default: admin)'
        )
        parser.add_argument(
            '--email',
            type=str,
            default='admin@islahaven.com',
            help='Admin email (default: admin@islahaven.com)'
        )
        parser.add_argument(
            '--password',
            type=str,
            default='admin123',
            help='Admin password (default: admin123)'
        )

    def handle(self, *args, **options):
        username = options['username']
        email = options['email']
        password = options['password']

        # Create Django superuser
        if not DjangoUser.objects.filter(username=username).exists():
            django_user = DjangoUser.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created Django superuser: {username}')
            )
        else:
            self.stdout.write(
                self.style.WARNING(f'Django superuser {username} already exists')
            )

        # Create app user (if needed for the application's custom User model)
        if not AppUser.objects.filter(username=username).exists():
            app_user = AppUser.objects.create(
                username=username,
                email=email,
                password=password,  # In a real app, this should be hashed
                first_name='Admin',
                last_name='User',
                phone_number='+960123456789'
            )
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created app user: {username}')
            )
        else:
            self.stdout.write(
                self.style.WARNING(f'App user {username} already exists')
            )