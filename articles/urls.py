from django.urls import path
from articles import views

app_name = 'articles'

urlpatterns = [
    path('', views.article_list_view, name='article_list'),
    path('detail/<slug:slug>/', views.article_detail_view, name='article_detail'),
    path('search/', views.article_search_view, name='article_search'),
    path('create/', views.article_create_view, name='article_create'),
    path('update/<int:pk>/', views.article_update_view, name='article_update'),
    path('delete/<int:pk>/', views.article_delete_view, name='article_delete'),
]
