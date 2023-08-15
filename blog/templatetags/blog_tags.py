from django import template
from django.db.models import Count, Avg

from ..models import Category, Article

register = template.Library()


@register.inclusion_tag('blog/partials/category_navbar.html')
def category_navbar():
    return {'category': Category.objects.active_category()}


@register.inclusion_tag('blog/partials/hot_article.html')
def hot_articles():
    return {
        'articles': Article.objects.published().annotate(comment=Count('comments'))
            .order_by('-comment', '-publish')[:4]
    }

@register.inclusion_tag('blog/partials/high_rate_articles.html')
def high_rating():
    return {
        'articles': Article.objects.published().annotate(high_rating=Avg('comments__rate'))
            .filter(high_rating__isnull=False).order_by('-high_rating')
    }
