import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.urls import reverse


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
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)

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


class Comment(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    active = models.BooleanField(default=True)
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.author} for {self.article}'
