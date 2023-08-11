from django.test import TestCase, SimpleTestCase
from django.urls import reverse, resolve

from . import views


class HomePageTest(SimpleTestCase):
    def setUp(self):
        url = reverse('pages:home')
        self.response = self.client.get(url)

    def test_homepage_by_url(self):
        self.assertEqual(self.response.status_code, 200)

    def test_homepage_template(self):
        self.assertTemplateUsed(self.response, 'home.html')

    def test_homepage_contains_correct_html(self):
        self.assertContains(self.response, 'This is our home page')

    def test_homepage_does_not_contains_inccorect_html(self):
        self.assertNotContains(self.response, 'Hi, This is our home page')

    def test_homepage_url_resolves_homepageview(self):
        view = resolve('/')
        self.assertEqual(
            view.func.__name__, views.HomePageView.as_view().__name__
        )
