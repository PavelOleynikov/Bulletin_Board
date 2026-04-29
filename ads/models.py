from django.db import models
from django.conf import settings


class Category(models.Model):
    """Категория объявления."""

    name = models.CharField(
        max_length=100, unique=True, verbose_name="Название категории", help_text="Укажите название категории"
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Ad(models.Model):
    """Объявление."""

    title = models.CharField(
        max_length=200,
        verbose_name="Заголовок",
        help_text="Укажите заголовок (не более 200 символов)",
    )

    description = models.TextField(verbose_name="описание", help_text="подробное описание товара или услуги")

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="цена",
        help_text="цена в рублях (не может быть отрицательной)",
    )

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="ads", verbose_name="категория")

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="ads", verbose_name="автор"
    )

    image = models.ImageField(upload_to="ads/image", blank=True, null=True, verbose_name="изображение")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="создано")

    updated_at = models.DateTimeField(auto_now=True, verbose_name="обновлено")

    is_active = models.BooleanField(default=True, verbose_name="активно")

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} - {self.price} руб."
