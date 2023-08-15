from django.contrib import admin

from .models import Article, Comment, Category


class InlineComment(admin.TabularInline):
    model = Comment
    extra = 4


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'publish', 'get_category', 'status']
    list_filter = ['publish', 'status']
    raw_id_fields = ['author']
    ordering = ['-status', '-publish']
    list_editable = ['status']
    inlines = [
        InlineComment,
    ]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'datetime_created', 'status']
    prepopulated_fields = {'slug': ('title', )}
    ordering = ['-datetime_updated']
    list_editable = ['status']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['article', 'author', 'text', 'rate', 'active']
    list_filter = ['datetime_updated', 'active']
    raw_id_fields = ['author']
    ordering = ['-active', '-datetime_updated']
