import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from ads.models import Category, Ad
from feedback.models import Review

User = get_user_model()


@pytest.fixture
def api_client():
    """API клиент без авторизации"""

    return APIClient()


@pytest.fixture
def user():
    """Обычный пользователь (с паролем)"""

    user = User.objects.create(email="user@test.com", first_name="Test", last_name="User", role="user")
    user.set_password("testpass123")
    user.save()
    return user


@pytest.fixture
def admin_user():
    """Администратор"""

    admin = User.objects.create(email="admin@test.com", first_name="Admin", role="admin")
    admin.set_password("adminpass123")
    admin.is_staff = True
    admin.save()
    return admin


@pytest.fixture
def auth_client(api_client, user):
    """Авторизованный клиент"""

    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def admin_client(api_client, admin_user):
    """Авторизованный админ"""

    api_client.force_authenticate(user=admin_user)
    return api_client


@pytest.fixture
def category():
    """Категория"""

    return Category.objects.create(name="Недвижимость")


@pytest.fixture
def ad(user, category):
    """Объявление"""

    return Ad.objects.create(
        title="Продам квартиру",
        description="3-комнатная квартира",
        price=15000000,
        category=category,
        author=user,
        is_active=True,
    )


@pytest.fixture
def review(user, ad):
    """Отзыв"""

    return Review.objects.create(text="Отличное объявление!", rating=5, author=user, ad=ad)
