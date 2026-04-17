from rest_framework.serializers import ModelSerializer

from users.models import User


class UserCreateSerializer(ModelSerializer):
    """Сериализатор для создания пользователя"""

    class Meta:
        model = User
        fields = ["id", "email", "password", "first_name", "last_name", "role", "city", "phone", "image"]
        extra_kwargs = {"password": {"write_only": True}}  # Не показываем пароль, только для записи


class UserDetailViewSerializer(ModelSerializer):
    """Сериализатор для отображения деталей пользователя"""

    class Meta:
        model = User
        fields = "__all__"


class UserViewSerializer(ModelSerializer):
    """Сериализатор для отображения списка пользователей"""

    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "role", "city"]
