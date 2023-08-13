import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.urls import reverse


class CommentManager(models.Manager):
    def active_comments(self):
        return self.filter(active=True)


class CategoryManager(models.Manager):
    def active_category(self):
        return self.filter(status=True)


class ArticleManager(models.Manager):
    def published(self):
        return self.filter(status='p')


class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_updated = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)

    objects = CategoryManager()

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'


class Article(models.Model):
    STATUS_CHOICES = (
        ('p', 'Published'),
        ('d', 'Draft'),
    )

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, db_index=True
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    cover = models.ImageField(upload_to='article/covers/')
    publish = models.DateTimeField(default=timezone.now)
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_updated = models.DateTimeField(auto_now=True)
    category = models.ManyToManyField(Category, related_name='articles')
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)

    objects = ArticleManager()

    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['id'], name='id_index'),
            models.Index(fields=['publish'])
        ]
        verbose_name = 'مقاله'
        verbose_name_plural = 'مقالات'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:article_detail', args=[str(self.id)])

    def get_category(self):
        return ', '.join(category.title for category in self.category.active_category())

    def category_active(self):
        return self.category.filter(status=True)


class Comment(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name='comments')
    email = models.EmailField()
    text = models.TextField()
    active = models.BooleanField(default=True)
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_updated = models.DateTimeField(auto_now=True)

    objects = CommentManager()

    def __str__(self) -> str:
        return f'{self.author} for {self.article}'

    class Meta:
        verbose_name = 'نظر '
        verbose_name_plural = 'نظرات'

    def get_absolute_url(self):
        return reverse('blog:article_detail', args=[str(self.article.id)])
