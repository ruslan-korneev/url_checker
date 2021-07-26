from celery import shared_task
from .models import Url
import requests as req


@shared_task
def get_url():
    urls = Url.objects.values()
    urls = [url for url in urls]
    codes = []
    for url in urls:
        if url['status_code'] == 0:
            status_code = req.get(url['url']).status_code
        codes.append({url['url']: status_code})
    return codes
