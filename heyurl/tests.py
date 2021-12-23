from django.test import TestCase
from django.urls import reverse
from .models import Url


class IndexTests(TestCase):
    def test_no_urls(self):
        """
        If no URLs exist, an appropriate message is displayed
        """
        response = self.client.get(reverse('index'))
        response_content = response.content.decode()
        self.assertIn('There are no URLs in the system yet!', response_content)

    def test_submitting_new_url_failure(self):
        """
        When submitting an invalid URL, an error is returned to the user
        """
        response = self.client.post(reverse('store'), data={'original_url': 'http://google'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode(), 'Request is not valid, missing proper data')

    def test_submitting_new_url_success(self):
        """
        When submitting a valid URL, a success message is displayed
        """
        response = self.client.post(reverse('store'), data={'original_url': 'http://google.com'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), 'Storing a new URL object into storage')

    def test_visiting_short_url_missing(self):
        """
        If short URL does not exist, custom 404 page is displayed
        """
        test_url = f"{reverse('short_url', args=('dne',))}"
        response = self.client.get(test_url)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content.decode(), f"Short URL dne not found")

    def test_visiting_short_url(self):
        """
        If short URL exists, stats logged and redirected to original URL
        """
        url = Url.create(original_url='http://google.com')
        test_url = f"{reverse('short_url', args=(url.short_url,))}"
        response = self.client.get(test_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), f"You're looking at url {url.short_url}")
