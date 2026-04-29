from rest_framework import viewsets, permissions
from feedback.models import Review
from feedback.serializers import ReviewSerializer
from feedback.permissions import IsAdminOrAuthor


class ReviewViewSet(viewsets.ModelViewSet):
    """ViewSet для отзывов"""

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAdminOrAuthor]

    def perform_create(self, serializer):
        """Автоматически подставляем автора"""

        serializer.save(author=self.request.user)
