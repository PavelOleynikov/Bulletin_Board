from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from users.models import User
from users.serializers import UserCreateSerializer, UserDetailViewSerializer, UserViewSerializer


class UserCreateAPIView(CreateAPIView):
    """Создание пользователя"""

    serializer_class = UserCreateSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)  # хэширование пароля
        user.save()


class UserViewSet(viewsets.ModelViewSet):
    """Класс для просмотра деталей и списка пользователей"""

    queryset = User.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["city"]
    ordering_fields = ["email"]
    ordering = ["-email"]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return UserDetailViewSerializer
        return UserViewSerializer
