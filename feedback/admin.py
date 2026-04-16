from django.contrib import admin
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "ad", "created_at")
    list_filter = ("created_at",)
    search_fields = ("text", "author__email", "ad__title")
