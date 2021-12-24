import logging
import random, string

from django.db import models, IntegrityError

from heyurl.managers import ClickQueryset

log = logging.getLogger(__name__)


class Url(models.Model):
    SHORT_URL_SIZE = 5

    short_url = models.URLField(unique=True)
    original_url = models.URLField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def to_dict(self):
        url_json_response = {
            "type": "urls",
            "id": self.id,
            "attributes": {
                "created-at": str(self.created_at),
                "original-url": str(self.original_url),
                "url": str(self.short_url),
                "clicks": self.clicks_count
            },
            "relationships": {
                "metrics": {
                    "data": []
                }
            }
        }
        for click in self.clicks.all():
            click_json_response = {
                "id": click.id,
                "type": "click"
            }
            url_json_response['relationships']['metrics']['data'].append(click_json_response)

        return url_json_response

    @classmethod
    def create(cls, original_url):
        success = False
        while not success:
            try:
                url = Url.objects.create(
                    short_url=cls.create_short_url(),
                    original_url=original_url,
                )
                success = True
                return url
            except IntegrityError:
                logging.warning('Could not create URL for short_url {}, it already exists in the database')

    @classmethod
    def create_short_url(cls):
        return ''.join(random.choice(string.ascii_letters) for _ in range(cls.SHORT_URL_SIZE))

    @property
    def clicks_count(self):
        return self.clicks.count()


class Click(models.Model):
    url = models.ForeignKey(Url, on_delete=models.CASCADE, related_name='clicks')
    browser = models.CharField(max_length=255)
    platform = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ClickQueryset.as_manager()

    @classmethod
    def create(cls, url, request):
        Click.objects.create(
            url=url,
            browser=cls.get_browser_from_request(request),
            platform=cls.get_platform_from_request(request),
        )

    @classmethod
    def get_browser_from_request(cls, request):
        if request.user_agent:
            return request.user_agent.browser.family

    @classmethod
    def get_platform_from_request(cls, request):
        if request.user_agent:
            return request.user_agent.os.family
