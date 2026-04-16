from django.db import models
from django.conf import settings
from ads.models import Ad


class Review(models.Model):
    """Модель отзыва на объявление"""

    text = models.TextField(verbose_name="текст отзыва", help_text="Ваш отзыв об объявлении или продавце")

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="автор отзыва",
        help_text="Пользователь, оставивший отзыв",
    )

    ad = models.ForeignKey(
        Ad,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="объявление",
        help_text="Объявление, под которым оставлен отзыв",
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="время и дата создания")

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ["-created_at"]
        # Пользователь может оставить только один отзыв на объявление
        unique_together = ["author", "ad"]

    def __str__(self):
        return f"Отзыв от {self.author.email} на {self.ad.title}"
