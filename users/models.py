from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Кастомная модель пользователя с email в качестве логина."""

    username = None

    email = models.EmailField(verbose_name="почта", unique=True, help_text="введите вашу почту")
    phone_number = models.CharField(
        verbose_name="номер телефона", max_length=15, blank=True, null=True, help_text="введите номер телефона"
    )
    avatar = models.ImageField(
        verbose_name="аватар", upload_to="users/avatar", blank=True, null=True, help_text="загрузите аватар"
    )
    city = models.CharField(verbose_name="город", max_length=50, blank=True, null=True, help_text="введите ваш город")
    rating = models.DecimalField(verbose_name="рейтинг", max_digits=3, decimal_places=2, default=0.00)
    total_ads = models.IntegerField(verbose_name="всего объявлений", default=0)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email
