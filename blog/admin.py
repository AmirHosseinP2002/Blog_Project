from django.contrib import admin

from .models import Article


@admin.register(Article)
class ArticleAdmni(admin.ModelAdmin):
    list_display = ['title', 'author', 'publish', 'datetime_updated', 'status']
    list_filter = ['publish', 'status']
    raw_id_fields = ['author']
    ordering = ['-status', '-publish']
