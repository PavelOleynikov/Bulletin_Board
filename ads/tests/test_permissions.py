import pytest
from ads.permissions import IsAuthorOrAdmin


@pytest.mark.django_db
class TestPermissions:
    """Тесты прав доступа"""

    def test_author_can_edit(self, user, ad):
        """Автор может редактировать"""

        permission = IsAuthorOrAdmin()
        request = type("Request", (), {"user": user, "method": "PUT"})()
        assert permission.has_object_permission(request, None, ad) == True

    def test_admin_can_edit(self, admin_user, ad):
        """Админ может редактировать"""

        permission = IsAuthorOrAdmin()
        request = type("Request", (), {"user": admin_user, "method": "DELETE"})()
        assert permission.has_object_permission(request, None, ad) == True

    def test_other_user_cannot_edit(self, user, ad):
        """Другой пользователь не может редактировать"""

        from django.contrib.auth import get_user_model

        User = get_user_model()
        other_user = User.objects.create(email="other@test.com", password="pass")
        permission = IsAuthorOrAdmin()
        request = type("Request", (), {"user": other_user, "method": "PUT"})()
        assert permission.has_object_permission(request, None, ad) == False

    def test_anyone_can_read(self, user, ad):
        """Чтение доступно всем (без авторизации)"""

        permission = IsAuthorOrAdmin()
        request = type("Request", (), {"user": None, "method": "GET"})()
        assert permission.has_object_permission(request, None, ad) == True
