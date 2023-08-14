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
        fields = ['email', 'text']

    def send_mail_reader(self, username):
        cd = self.cleaned_data
        subject = 'Save your comment'
        message = f'Hi {username}, your comment successfully save in my site'
        from_email = 'localhost:8000'
        recipient_list = [cd['email']]
        send_mail(subject, message, from_email, recipient_list)
    
    def send_mail_author(self, article, username):
        subject = f'comment for {article.title}'
        message = f'a comment by {username} for {article.title} saved'
        from_email = 'localhost:8000'
        recipient_list = [article.author.email]
        send_mail(subject, message, from_email, recipient_list)
