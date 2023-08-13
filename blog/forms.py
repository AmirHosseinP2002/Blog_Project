from django import forms

from .models import Article, Comment


class ArticleCreateForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'description', 'cover', 'publish', 'status']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['email', 'text']
