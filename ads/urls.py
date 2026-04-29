from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AdViewSet, CategoryViewSet

# Создаем роутер для автоматической генерации URL-ов
router = DefaultRouter()
router.register(r"ads", AdViewSet, basename="ad")
router.register(r"categories", CategoryViewSet, basename="category")

urlpatterns = [
    path("", include(router.urls)),
]
