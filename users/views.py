from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User
from users.serializers import (
    UserCreateSerializer,
    UserDetailViewSerializer,
    UserViewSerializer,
    PasswordResetSerializer,
    PasswordResetConfirmSerializer,
)


class UserCreateAPIView(CreateAPIView):
    """Создание пользователя"""

    serializer_class = UserCreateSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)


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


class PasswordResetView(APIView):
    """POST /users/reset_password/ - запрос сброса пароля"""

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Ссылка для сброса отправлена на почту"})
        return Response(serializer.errors, status=400)


class PasswordResetConfirmView(APIView):
    """POST /users/reset_password_confirm/ - установка нового пароля"""

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Пароль успешно изменен"})
        return Response(serializer.errors, status=400)
