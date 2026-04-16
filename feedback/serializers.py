from rest_framework import serializers
from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор отзыва"""

    author_email = serializers.ReadOnlyField(source="author.email")
    ad_title = serializers.ReadOnlyField(source="ad.title")

    class Meta:
        model = Review
        fields = ["id", "text", "author", "author_email", "ad", "ad_title", "created_at"]
        read_only_fields = ["author", "created_at"]

    def validate_text(self, value):
        """Валидация текста"""

        if len(value) < 5:
            raise serializers.ValidationError("Текст отзыва должен содержать минимум 5 символов")
        if len(value) > 500:
            raise serializers.ValidationError("Текст отзыва не должен превышать 500 символов")
        return value
