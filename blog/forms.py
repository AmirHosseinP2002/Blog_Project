from django import forms
from django.core.mail import send_mail

from .models import Article, Comment


class ArticleCreateForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'description', 'cover', 'publish', 'status', 'category']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['email', 'text', 'rate']
        