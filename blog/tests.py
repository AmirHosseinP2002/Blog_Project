from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model
import tempfile

from .models import Article
from .forms import ArticleCreateForm
from . import views


class ArticleTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.cover = tempfile.NamedTemporaryFile(suffix='.jpg').name
        cls.author = get_user_model().objects.create(
            username='testuser',
        )
        cls.article1 = Article.objects.create(
            title='test title 1',
            description='test description 1',
            author=cls.author,
            cover=cls.cover,
            status='p',
        )
        cls.article2 = Article.objects.create(
            title='test title 2',
            description='test description 2',
            author=cls.author,
            cover=cls.cover,
            status='d',
        )

    # List View
    def test_article_list_url(self):
        url = reverse('blog:article_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_article_list_template(self):
        url = reverse('blog:article_list')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'blog/article_list.html')
        self.assertContains(response, 'Article List')
        self.assertContains(response, 'test title 1')
        self.assertNotContains(response, 'Hi, Article List')
        self.assertNotContains(response, 'test title 2')

    def test_article_list_view(self):
        view = resolve('/blog/')
        self.assertEqual(
            view.func.__name__, views.ArticleListView.as_view().__name__
        )

    # Detail View
    def test_article_detail_url(self):
        url_1 = reverse('blog:article_detail', args=[self.article1.id])
        response = self.client.get(url_1)
        url_2 = reverse('blog:article_detail', args=[self.article2.id])
        self.not_response = self.client.get(url_2)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.not_response.status_code, 404)

    def test_article_detail_template(self):
        url_1 = reverse('blog:article_detail', args=[self.article1.id])
        response = self.client.get(url_1)
        self.assertTemplateUsed(response, 'blog/article_detail.html')
        self.assertContains(response, 'Article Detail')
        self.assertContains(response, 'test title 1')
        self.assertNotContains(response, 'Hi, Article List')
        self.assertNotContains(response, 'test title 2')

    def test_article_detail_view(self):
        view = resolve(f'/blog/{self.article1.id}/')
        self.assertEqual(
            view.func.__name__, views.ArticleDetailView.as_view().__name__
        )
    
    # Create View
    def test_article_create_url(self):
        url = reverse('blog:article_create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    def test_article_create_template(self):
        url = reverse('blog:article_create')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'blog/article_create_update.html')
        self.assertContains(response, 'Article Create')
        self.assertNotContains(response, 'Hi, Article Create')
    
    def test_article_create_form(self):
        url = reverse('blog:article_create')
        response = self.client.get(url)
        form = response.context.get('form')
        self.assertIsInstance(form, ArticleCreateForm)
        self.assertContains(response, 'csrfmiddleware')

    def test_article_create_view(self):
        view = resolve(f'/blog/create/')
        self.assertEqual(
            view.func.__name__, views.ArticleCreateView.as_view().__name__
        )
    
    # def test_article_create_in_create_article(self):
    #     response = self.client.post(reverse('blog:article_create'), {
    #         'title': 'Some Title',
    #         'description': 'Some Text',
    #         'author': self.author.id,
    #         'cover': self.cover,
    #         'status': 'p'
    #     })
    #     self.assertEqual(response.status_code, 302)
    #     self.assertEqual(Article.objects.last().title, 'Some Title')
    #     self.assertEqual(Article.objects.last().description, 'Some Text')
    #     self.assertEqual(Article.objects.last().author, self.author)
    #     self.assertEqual(Article.objects.last().status, 'p')

    # Update View
    # def test_post_update_view(self):
    #     response = self.client.post(reverse('blog:article_update', args=[self.article2.id]), {
    #         'title': 'Update Title',
    #         'text': 'Update Text',
    #         'author': self.author.id,
    #         'cover': self.cover,
    #         'status': 'p'
    #     })
    #     # self.assertEqual(response.status_code, 302)
    #     self.assertEqual(Article.objects.last().title, 'Update Title')
    #     self.assertEqual(Article.objects.last().description, 'Update Text')
    #     self.assertEqual(Article.objects.last().author, self.author)
    #     self.assertEqual(Article.objects.last().status, 'p')

    def test_article_delete_view(self):
        response = self.client.post(reverse('blog:article_delete', args=[self.article2.id]))
        self.assertEqual(response.status_code, 302)
