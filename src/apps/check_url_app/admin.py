from django.contrib import admin
from .models import Url


@admin.register(Url)
class UrlAdmin(admin.ModelAdmin):
    list_display = ("url", "status_code", )
    list_filter = ("status_code", )
