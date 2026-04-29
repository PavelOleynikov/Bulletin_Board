from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Кастомная модель пользователя с email в качестве логина."""

    username = None

    ROLE_CHOICES = [
        ("user", "Пользователь"),
        ("admin", "Администратор"),
    ]

    first_name = models.CharField(
        verbose_name="имя пользователя", max_length=30, blank=True, null=True, help_text="введите ваше имя"
    )
    last_name = models.CharField(
        verbose_name="фамилия пользователя", max_length=30, blank=True, null=True, help_text="введите вашу фамилию"
    )
    email = models.EmailField(verbose_name="почта", unique=True, help_text="введите вашу электронную почту")
    phone = models.CharField(
        verbose_name="номер телефона", max_length=15, blank=True, null=True, help_text="введите номер телефона"
    )
    image = models.ImageField(
        verbose_name="аватар", upload_to="users/avatar", blank=True, null=True, help_text="загрузите аватарку"
    )
    role = models.CharField(
        verbose_name="роль", max_length=20, choices=ROLE_CHOICES, default="user", help_text="выберете роль"
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
