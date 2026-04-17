from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    help = "Создание тестовых пользователей"

    def handle(self, *args, **options):

        # Создание администратора
        self.create_user(
            email="admin@admin.com",
            first_name="Admin",
            last_name="User",
            phone="4321",
            password="1234",
            role="admin",
        )

        # Создание обычного пользователя
        self.create_user(
            email="user@admin.com",
            first_name="Ivan",
            last_name="Ivanov",
            phone="5678",
            password="1234",
            role="user",
        )

    def create_user(self, email, first_name, last_name, phone, password, role):
        if not User.objects.filter(email=email).exists():
            user = User.objects.create(
                email=email,
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                role=role,
            )
            user.set_password(password)
            user.save()
            self.stdout.write(self.style.SUCCESS(f"Пользователь {email} (роль: {role}) успешно создан."))
        else:
            self.stdout.write(self.style.WARNING(f"Пользователь с email {email} уже существует."))
