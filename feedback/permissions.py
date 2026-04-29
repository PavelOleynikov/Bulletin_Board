from rest_framework import permissions


class IsAdminOrAuthor(permissions.BasePermission):
    """Админ может всё, пользователь только свои комментарии"""

    def has_object_permission(self, request, view, obj):
        # Админ может всё
        if request.user.is_authenticated and request.user.role == "admin":
            return True

        # Чтение разрешено всем
        if request.method in permissions.SAFE_METHODS:
            return True

        # Пользователь может редактировать только свои комментарии
        return obj.author == request.user
