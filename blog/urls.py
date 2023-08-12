from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.ArticleListView.as_view(), name='article_list'),
    path('<uuid:pk>/', views.ArticleDetailView.as_view(), name='article_detail'),
    path('create/', views.ArticleCreateView.as_view(), name='article_create'),
    path('<uuid:pk>/update/', views.ArticleUpdateView.as_view(), name='article_update'),
    path('<uuid:pk>/delete/', views.ArticleDeleteView.as_view(), name='article_delete'),
    path('search/', views.ArticlesearchListView.as_view(), name='article_search'),
]
