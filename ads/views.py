from django.core.cache import cache
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from ads.models import Ad, Category
from ads.pagination import AdPagination
from ads.serializers import AdSerializer, CategorySerializer
from ads.permissions import IsAuthorOrAdmin, IsActiveUser


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet для категорий с кэшированием(только чтение)
    Доступно всем пользователям
    """

    def get_queryset(self):
        # Кэшируем категории на 1 час (3600 секунд)
        cache_key = "categories_list"
        cached_data = cache.get(cache_key)

        if cached_data is not None:
            # Возвращаем закэшированные данные
            return cached_data

        # Если кэша нет, получаем из БД
        queryset = Category.objects.all()
        # Сохраняем в кэш на 1 час
        cache.set(cache_key, queryset, 3600)
        return queryset

    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class AdViewSet(viewsets.ModelViewSet):
    """
    ViewSet для объявлений:
    - GET /ads/ - список всех активных объявлений
    - GET /ads/{id}/ - детальное просмотр объявления
    - POST /ads/ - создание объявления (только авторизованные)
    - PUT/PATCH /ads/{id}/ - обновление (только автор или админ)
    - DELETE /ads/{id}/ - удаление (только автор или админ)
    """

    queryset = Ad.objects.filter(is_active=True)  # Только активные объявления
    serializer_class = AdSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrAdmin, IsActiveUser]
    pagination_class = AdPagination

    # Настройка фильтрации, поиска и сортировки
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["category", "is_active"]  # Точное совпадение
    search_fields = ["title", "description"]  # Поиск по тексту
    ordering_fields = ["price", "created_at"]  # Сортировка
    ordering = ["-created_at"]  # По умолчанию: новые первые

    def perform_create(self, serializer):
        """При создании объявления автоматически подставляем автора"""

        serializer.save(author=self.request.user)
