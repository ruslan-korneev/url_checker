from celery import shared_task
from .models import Url
import requests as req


@shared_task
def check_urls():
    urls = Url.objects.filter(status_code=0)
    for url in urls:
        url.status_code = req.get(url.url).status_code
        if url.status_code >=100 and url.status_code < 200:
            url.status_text = 'Processing'
        elif url.status_code >=200 and url.status_code < 300:
            url.status_text = 'OK'
        elif url.status_code >=300 and url.status_code < 400:
            url.status_text = 'Redirection'
        elif url.status_code >=400 and url.status_code < 500:
            url.status_text = 'Client Error'
        elif url.status_code >=500 and url.status_code < 600:
            url.status_text = 'Server Error'
        else:
            url.status_text = 'Something was wrong'
        url.save(update_fields=['status_code', 'status_text'])
    return urls
