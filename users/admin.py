from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdminModel(admin.ModelAdmin):
    list_display = ("id", "email", "first_name", "last_name", "city", "phone", "role")
    list_filter = ("role", "city")
    search_fields = ("email", "first_name", "last_name", "phone")
