from django import template
from ..models import Category

register = template.Library()


@register.inclusion_tag('blog/partials/category_navbar.html')
def category_navbar():
    return {'category': Category.objects.active_category()}
