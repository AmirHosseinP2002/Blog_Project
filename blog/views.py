from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import generic
from django.urls import reverse_lazy
from django.db.models import Q

from .models import Article
from .forms import ArticleCreateForm


class ArticleListView(generic.ListView):
    queryset = Article.objects.filter(status='p')
    template_name = 'blog/article_list.html'
    context_object_name = 'articles'


class ArticleDetailView(generic.DetailView):
    template_name = 'blog/article_detail.html'
    context_object_name = 'article'

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        article = get_object_or_404(Article, id=pk, status='p')
        return article


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


class ArticleSearchListView(generic.ListView):
    template_name = 'blog/article_search.html'
    context_object_name = 'articles'

    def get_queryset(self):
        q = self.request.GET.get('q')
        return Article.objects.filter(Q(title__icontains=q) | Q(description__icontains=q))
