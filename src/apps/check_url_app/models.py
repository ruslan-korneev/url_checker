from django.db import models


class Url(models.Model):
    """
        Url model for saving link,
        code status and text status
        to the database
    """
    # This field will be for saving links
    url = models.URLField(max_length=255)

    # This field is for saving the status code,
    # it cannot be changed in the admin panel, when creating an Url object,
    # the status code is set to zero,
    # so the celery task understands that it is necessary
    # to send a request for a link of this object
    status_code = models.IntegerField(blank=True, default=0, editable=False)

    # This field is for Text Status,
    # which is needed to understand the meaning of the status code,
    # since when creating an object, the status code is unknown,
    # the status text is set to "Not Checked"
    status_text = models.CharField(
        max_length=64,
        blank=True,
        default='Not checked',
        editable=False)
