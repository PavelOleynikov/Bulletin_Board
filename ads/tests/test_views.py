import pytest
from django.urls import reverse

from django.contrib.auth import get_user_model
from ads.models import Ad

User = get_user_model()


@pytest.mark.django_db
class TestAdViews:
    """Тесты API объявлений"""

    def test_list_ads_unauthorized(self, api_client, ad):
        """Неавторизованный видит список объявлений"""

        url = reverse("ad-list")
        response = api_client.get(url)
        assert response.status_code == 200
        assert "results" in response.data

    def test_detail_ad(self, api_client, ad):
        """Просмотр деталей объявления"""

        url = reverse("ad-detail", args=[ad.id])
        response = api_client.get(url)
        assert response.status_code == 200
        assert response.data["title"] == ad.title

    def test_create_ad_unauthorized(self, api_client, category):
        """Неавторизованный не может создать объявление"""

        url = reverse("ad-list")
        data = {"title": "Новое", "description": "Описание", "price": 1000, "category": category.id}
        response = api_client.post(url, data)
        assert response.status_code == 401  # Unauthorized

    def test_create_ad_authorized(self, auth_client, category):
        """Авторизованный может создать объявление"""

        url = reverse("ad-list")
        data = {
            "title": "Мое объявление",
            "description": "Описание объявления",
            "price": 5000,
            "category": category.id,
        }
        response = auth_client.post(url, data)

        # Выводим ошибку для отладки
        if response.status_code != 201:
            print(f"\nСтатус: {response.status_code}")
            print(f"Ошибка: {response.data}")

        assert response.status_code == 201
        assert response.data["title"] == "Мое объявление"

    def test_update_own_ad(self, auth_client, ad):
        """Автор может обновить свое объявление"""

        url = reverse("ad-detail", args=[ad.id])
        data = {"title": "Обновленное название"}
        response = auth_client.patch(url, data)
        assert response.status_code == 200
        assert response.data["title"] == "Обновленное название"

    def test_update_others_ad(self, auth_client, category):
        """Нельзя обновить чужое объявление"""

        # Создаем другого пользователя
        other_user = User.objects.create(email="other@test.com")
        other_user.set_password("pass123")
        other_user.save()

        other_ad = Ad.objects.create(
            title="Чужое", description="desc", price=100, category=category, author=other_user
        )
        url = reverse("ad-detail", args=[other_ad.id])
        data = {"title": "Попытка взлома"}
        response = auth_client.patch(url, data)
        assert response.status_code == 403

    def test_delete_own_ad(self, auth_client, ad):
        """Автор может удалить свое объявление"""

        url = reverse("ad-detail", args=[ad.id])
        response = auth_client.delete(url)
        assert response.status_code == 204

    def test_search_ads(self, api_client, ad):
        """Поиск по заголовку работает"""

        url = reverse("ad-list")
        response = api_client.get(url, {"search": "квартиру"})
        assert response.status_code == 200
        assert len(response.data["results"]) >= 1

    def test_filter_by_category(self, api_client, ad, category):
        """Фильтрация по категории"""

        url = reverse("ad-list")
        response = api_client.get(url, {"category": category.id})
        assert response.status_code == 200

    def test_pagination_limit_4(self, auth_client, category):
        """Пагинация: не более 4 объявлений на странице"""

        # Получаем текущего пользователя из auth_client
        current_user = auth_client.handler._force_user

        # Создаем 10 объявлений от текущего пользователя
        for i in range(10):
            Ad.objects.create(
                title=f"Объявление {i}", description="desc", price=1000 + i, category=category, author=current_user
            )
        url = reverse("ad-list")
        response = auth_client.get(url)
        assert response.status_code == 200
        assert len(response.data["results"]) <= 4
