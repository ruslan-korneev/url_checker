from django.contrib import admin

from .models import Url


@admin.register(Url)
class UrlAdmin(admin.ModelAdmin):
    """
        This class, Admin Model, for the visibility
        of the Url model in the admin panel
    """

    # I show a link on the display, status code, status text
    list_display = (
        "url",
        "status_code",
        'status_text',
    )

    # I also give the ability to filter objects by "status text"
    list_filter = ("status_text", )
