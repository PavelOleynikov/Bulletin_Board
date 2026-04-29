from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """Класс для проверки является ли пользователь владельцем объекта."""

    def has_object_permission(self, request, view, obj):

        owner = getattr(obj, "user", None) or getattr(obj, "owner", None)
        return owner == request.user


class IsPublic(permissions.BasePermission):
    """Класс для проверки является ли объект публичным."""

    def has_object_permission(self, request, view, obj):
        # Если объект публичный - доступ разрешен
        if getattr(obj, "is_public", False):
            return True

        # Если объект не публичный, проверяем владельца
        owner = getattr(obj, "user", None) or getattr(obj, "owner", None)
        return owner == request.user
