from django.contrib import admin

from .models import Article, Comment


class InlineComment(admin.TabularInline):
    model = Comment
    extra = 4


@admin.register(Article)
class ArticleAdmni(admin.ModelAdmin):
    list_display = ['title', 'author', 'publish', 'datetime_updated', 'status']
    list_filter = ['publish', 'status']
    raw_id_fields = ['author']
    ordering = ['-status', '-publish']
    inlines = [
        InlineComment,
    ]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['article', 'author', 'text', 'active']
    list_filter = ['datetime_updated', 'active']
    raw_id_fields = ['author']
    ordering = ['-active', '-datetime_updated']
