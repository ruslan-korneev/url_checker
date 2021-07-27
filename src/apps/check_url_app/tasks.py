from celery import shared_task

import requests as req

from .models import Url


@shared_task
def check_urls():
    """
        This function check all url with status code 0
        And Changes the status code to real,
        thereby indicating the availability of the website
    """
    # Collect all sites with status code 0 from the db
    urls = Url.objects.filter(status_code=0)

    # We will send a request to each site to receive the status code
    for url in urls:
        url.status_code = req.get(url.url).status_code
        if url.status_code >= 100 and url.status_code < 200:
            url.status_text = 'Processing'
        elif url.status_code >= 200 and url.status_code < 300:
            url.status_text = 'OK'
        elif url.status_code >= 300 and url.status_code < 400:
            url.status_text = 'Redirection'
        elif url.status_code >= 400 and url.status_code < 500:
            url.status_text = 'Client Error'
        elif url.status_code >= 500 and url.status_code < 600:
            url.status_text = 'Server Error'
        else:
            url.status_text = 'Something was wrong'

        # Updating the data in the database,
        # Status code and Status Text
        #   - For clarification, the status of the code
        url.save(update_fields=['status_code', 'status_text'])
    return urls
