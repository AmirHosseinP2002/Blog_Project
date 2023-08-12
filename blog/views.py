from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy

from .models import Article
from .forms import ArticleCreateForm


class ArticleListView(generic.ListView):
    queryset = Article.objects.filter(status='p')
    template_name = 'blog/article_list.html'
    context_object_name = 'articles'


class ArticleDetailView(generic.DetailView):
    model = Article
    template_name = 'blog/article_detail.html'
    context_object_name = 'article'


class ArticleCreateView(generic.CreateView):
    form_class = ArticleCreateForm
    template_name = 'blog/article_create_update.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ArticleUpdateView(generic.UpdateView):
    model = Article
    form_class = ArticleCreateForm
    template_name = 'blog/article_create_update.html'

class ArticleDeleteView(generic.DeleteView):
    model = Article
    template_name = 'blog/article_delete.html'
    success_url = reverse_lazy('blog:article_list')
