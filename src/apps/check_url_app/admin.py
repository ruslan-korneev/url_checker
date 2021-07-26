from django.contrib import admin
from .models import Url


@admin.register(Url)
class UrlAdmin(admin.ModelAdmin):
    list_display = ("url", "status_code", 'status_text', )
    list_filter = ("status_text", )
