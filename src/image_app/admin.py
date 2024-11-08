from django.contrib import admin

from .models import Image


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Image._meta.get_fields()]
    list_display_links = ("id",)
