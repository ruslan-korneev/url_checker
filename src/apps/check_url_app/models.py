from django.db import models
import requests as req

class Url(models.Model):
    url = models.URLField(max_length=255)
    status_code = models.IntegerField(blank=True, default=0, editable=False)
    status_text = models.CharField(max_length=64, blank=True, default='Not checked', editable=False)
