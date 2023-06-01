from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('about/', views.AboutUsView.as_view(), name='about'),
    path('blogs/', views.BlogListView.as_view(), name='blog_list'),
    path('blogs/<int:pk>/', views.BlogDetailView.as_view(), name='blog_detail'),
]    

