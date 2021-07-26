from django.db import models
import requests as req

class Url(models.Model):
    url = models.URLField(max_length=255)
    status_code = models.IntegerField(blank=True, null=True)
