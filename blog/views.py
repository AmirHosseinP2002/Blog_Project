from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.urls import reverse_lazy
from django.db.models import Q

from .models import Article, Category
from .forms import ArticleCreateForm, CommentForm


class ArticleListView(generic.ListView):
    queryset = Article.objects.published()
    template_name = 'blog/article_list.html'
    context_object_name = 'articles'


class CategoryListView(generic.ListView):
    template_name = 'blog/category_list.html'
    context_object_name = 'articles'

    def get_queryset(self):
        global category
        slug = self.kwargs.get('slug')
        category = get_object_or_404(
            Category.objects.active_category(), slug=slug,)
        return category.articles.published()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = category
        return context


class ArticleDetailView(generic.DetailView):
    template_name = 'blog/article_detail.html'
    context_object_name = 'article'

    def get_object(self):
        global article
        pk = self.kwargs.get('pk')
        article = get_object_or_404(Article.objects.published(), id=pk)
        return article

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = article.comments.active_comments()
        context['comment_form'] = CommentForm()
        return context


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q')
        return context


class CommentCreate(generic.CreateView):
    form_class = CommentForm

    def form_valid(self, form):
        article_id = self.kwargs.get('article_id')
        article = get_object_or_404(Article, id=article_id)
        form.instance.article = article
        form.instance.author = self.request.user

        if self.request.user != article.author:
            form.send_mail_reader(self.request.user)
            form.send_mail_author(article, self.request.user)

        return super().form_valid(form)
