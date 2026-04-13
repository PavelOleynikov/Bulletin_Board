from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    help = "Создание тестовых пользователей"

    def handle(self, *args, **options):
        self.create_user(
            email="admin@admin.com",
            phone_number="4321",
            password="1234",
            is_staff=True,
            is_superuser=True,
        )

        self.create_user(
            email="user@admin.com",
            phone_number="5678",
            password="1234",
            is_staff=False,
            is_superuser=False,
        )

    def create_user(self, email, phone_number, password, is_staff, is_superuser):
        user = User.objects.create(
            email=email, phone_number=phone_number, is_staff=is_staff, is_superuser=is_superuser
        )
        user.set_password(password)
        user.save()
        self.stdout.write(self.style.SUCCESS(f"Пользователь {email} успешно создан."))
