from django.urls import path
from . import views

app_name = 'people'

urlpatterns = [
    path('', views.CelebListView.as_view(), name='celeb_list'),
    path('<int:pk>/', views.CelebDetailView.as_view(), name='celeb_detail'),
    path('grid/', views.CelebGridView.as_view(), name='celeb_grid'),
]