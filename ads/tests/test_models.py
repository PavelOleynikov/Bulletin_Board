import pytest
from ads.models import Ad


@pytest.mark.django_db  # Создает временную тестовую БД
class TestCategoryModel:
    """Тесты категорий"""

    def test_create_category(self, category):
        assert category.name == "Недвижимость"

    def test_category_str(self, category):
        assert str(category) == "Недвижимость"


@pytest.mark.django_db
class TestAdModel:
    """Тесты объявлений"""

    def test_create_ad(self, ad, user, category):
        assert ad.title == "Продам квартиру"
        assert ad.price == 15000000
        assert ad.author == user
        assert ad.category == category
        assert ad.is_active == True

    def test_ad_str(self, ad):
        assert "Продам квартиру" in str(ad)

    def test_ad_ordering(self, user, category):
        # Создаем два объявления
        Ad.objects.create(title="Старое", description="desc", price=100, category=category, author=user)

        Ad.objects.create(title="Новое", description="desc", price=200, category=category, author=user)

        # Проверяем, что новое объявление появляется первым
        first_ad = Ad.objects.filter(title__in=["Старое", "Новое"]).first()
        assert first_ad.title == "Новое"
