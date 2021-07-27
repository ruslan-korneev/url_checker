from ssl import SSLCertVerificationError
from urllib.error import HTTPError, URLError
from urllib.request import socket

from OpenSSL.SSL import WantReadError

from celery import shared_task

from django.conf import settings

import requests as req
from requests.exceptions import (
    ReadTimeout,
    SSLError,
)

from urllib3.exceptions import MaxRetryError

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
    timeout = settings.TIMEOUT_FOR_REQUEST

    # We will send a request to each site to receive the status code
    for url in urls:
        try:
            url.status_code = req.get(
                url.url,
                allow_redirects=True,
                timeout=timeout).status_code
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
        except (socket.timeout, ReadTimeout, WantReadError):
            # The request takes a very long time
            url.status_text = 'Timed Out'
        except URLError:
            # If url was set incorrectly
            url.status_text = 'Wrong Url'
        except HTTPError:
            url.status_text = 'HTTP Error'
        except UnicodeError:
            url.status_text = 'Unicode Error'
        except (SSLError, SSLCertVerificationError, MaxRetryError):
            # If SSL cirtificate is invalid
            url.status_code = req.get(
                url.url,
                allow_redirects=True,
                timeout=timeout, verify=False).status_code
            if url.status_code >= 100 and url.status_code < 200:
                url.status_text = 'Processing, Please Update SSL'
            elif url.status_code >= 200 and url.status_code < 300:
                url.status_text = 'OK, Please Update SSL'
            elif url.status_code >= 300 and url.status_code < 400:
                url.status_text = 'Redirection, Please Update SSL'
            elif url.status_code >= 400 and url.status_code < 500:
                url.status_text = 'Client Error, Please Update SSL'
            elif url.status_code >= 500 and url.status_code < 600:
                url.status_text = 'Server Error, Please Update SSL'
            else:
                url.status_text = 'Something was wrong, Please Update SSL'
        except ConnectionError:
            url.status_text = 'Connection Error'

        # Updating the data in the database,
        # Status code and Status Text
        #   - For clarification, the status of the code
        url.save(update_fields=['status_code', 'status_text'])
    return
