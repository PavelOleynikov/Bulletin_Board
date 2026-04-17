from rest_framework import serializers
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from users.models import User


class UserCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания пользователя"""

    class Meta:
        model = User
        fields = ["id", "email", "password", "first_name", "last_name", "role", "city", "phone", "image"]
        extra_kwargs = {"password": {"write_only": True}}  # Не показываем пароль, только для записи

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserDetailViewSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения деталей пользователя"""

    class Meta:
        model = User
        fields = "__all__"


class UserViewSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения списка пользователей"""

    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "role", "city"]


class PasswordResetSerializer(serializers.Serializer):
    """Запрос на сброс пароля"""

    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Пользователь не найден")
        return value

    def save(self):
        email = self.validated_data["email"]
        user = User.objects.get(email=email)

        # Генерируем токен
        token = default_token_generator.make_token(user)
        uid = user.pk

        # Ссылка для сброса
        reset_link = f"/users/reset_password_confirm/{uid}/{token}/"

        # Отправляем письмо
        send_mail(
            subject="Сброс пароля",
            message=f"Для сброса пароля перейдите по ссылке: {reset_link}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
        )


class PasswordResetConfirmSerializer(serializers.Serializer):
    """Подтверждение сброса пароля"""

    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(min_length=4)

    def validate(self, data):
        try:
            user = User.objects.get(pk=data["uid"])
        except User.DoesNotExist:
            raise serializers.ValidationError("Неверный пользователь")

        if not default_token_generator.check_token(user, data["token"]):
            raise serializers.ValidationError("Неверный или просроченный токен")

        data["user"] = user
        return data

    def save(self):
        user = self.validated_data["user"]
        user.set_password(self.validated_data["new_password"])
        user.save()
