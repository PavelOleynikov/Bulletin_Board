from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Пользователь может редактировать только свои комментарии"""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class IsAdminOrAuthor(permissions.BasePermission):
    """Админ может всё, пользователь только свои комментарии"""

    def has_object_permission(self, request, view, obj):
        # Админ может всё
        if request.user and request.user.is_staff:
            return True

        # Чтение разрешено всем
        if request.method in permissions.SAFE_METHODS:
            return True

        # Пользователь может редактировать только свои комментарии
        return obj.author == request.user
