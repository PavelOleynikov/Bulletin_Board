from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from .models import Ad, Category
from .serializers import AdSerializer, CategorySerializer
from .permissions import IsAuthorOrReadOnly


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet для категорий (только чтение)
    Доступно всем пользователям
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class AdViewSet(viewsets.ModelViewSet):
    """
    ViewSet для объявлений:
    - GET /ads/ - список всех активных объявлений
    - GET /ads/{id}/ - детальное просмотр объявления
    - POST /ads/ - создание объявления (только авторизованные)
    - PUT/PATCH /ads/{id}/ - обновление (только автор)
    - DELETE /ads/{id}/ - удаление (только автор)
    """

    queryset = Ad.objects.filter(is_active=True)  # Только активные объявления
    serializer_class = AdSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    # Настройка фильтрации, поиска и сортировки
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["category", "is_active"]  # Точное совпадение
    search_fields = ["title", "description"]  # Поиск по тексту
    ordering_fields = ["price", "created_at"]  # Сортировка
    ordering = ["-created_at"]  # По умолчанию: новые первые

    def perform_create(self, serializer):
        """При создании объявления автоматически подставляем автора"""

        serializer.save(author=self.request.user)
