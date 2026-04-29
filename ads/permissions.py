from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Права доступа:
    - Чтение доступно всем
    - Изменение только автору объявления
    """

    def has_object_permission(self, request, view, obj):
        # Чтение доступно всем
        if request.method in permissions.SAFE_METHODS:
            return True

        # Изменение только автору объявления
        return obj.author == request.user


class IsAuthorOrAdmin(permissions.BasePermission):
    """
    Права доступа:
    - Чтение доступно всем
    - Изменение автору или администратору
    """

    def has_object_permission(self, request, view, obj):
        # Чтение доступно всем
        if request.method in permissions.SAFE_METHODS:
            return True

        # Проверка через role
        if request.user.is_authenticated and request.user.role == "admin":
            return True

        return obj.author == request.user


class IsActiveUser(permissions.BasePermission):
    """Проверка, что пользователь активен"""

    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            return request.user.is_active
        return True
