from rest_framework import serializers
from .models import Category, Ad
from .validators import title_validator, price_validator, description_validator


class CategorySerializer(serializers.ModelSerializer):
    """ "Сериализатор для категорий"""

    class Meta:
        model = Category
        fields = ["id", "name"]


class AdSerializer(serializers.ModelSerializer):
    """Сериализатор для объявлений со встроенной валидацией"""

    class Meta:
        model = Ad
        fields = [
            "id",
            "title",
            "description",
            "price",
            "category",
            "author",
            "image",
            "created_at",
            "updated_at",
            "is_active",
        ]
        read_only_fields = ["author", "created_at", "updated_at"]

    def validate_title(self, value):
        """Валидация заголовка"""

        title_validator(value)
        return value

    def validate_description(self, value):
        """Валидация описания"""

        description_validator(value)
        return value

    def validate_price(self, value):
        """Валидация цены"""

        price_validator(value)
        return value
