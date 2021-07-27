from apps.check_url_app.models import Url
from apps.check_url_app.tasks import check_urls

from django.test import TestCase


class TestDefinitionStatusCode(TestCase):

    def setUp(self):
        self.url = 'https://google.com'
        Url.objects.create(url=self.url)

    def test_status_code_before_after_task(self):
        """ Check status code of url before task and after """
        url_object = Url.objects.get(url=self.url)

        # Check before task
        self.assertEquals(url_object.status_code, 0)
        self.assertEquals(url_object.status_text, 'Not checked')

        # Do task
        check_urls()
        url_object.refresh_from_db()

        # After task
        self.assertEquals(url_object.status_code, 200)
        self.assertEquals(url_object.status_text, 'OK')
