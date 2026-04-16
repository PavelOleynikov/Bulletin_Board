from rest_framework import viewsets, permissions
from .models import Review
from .serializers import ReviewSerializer


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Только автор может редактировать свой отзыв"""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class ReviewViewSet(viewsets.ModelViewSet):
    """ViewSet для отзывов"""

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        """Автоматически подставляем автора"""

        serializer.save(author=self.request.user)
