from django.urls import path
from . import views

app_name = 'television'

urlpatterns = [
    path('', views.SerieListView.as_view(), name='series_list'),
    path('grid/', views.SerieGridView.as_view(), name='series_grid'),
    path('<int:pk>/<slug:slug>/', views.SerieDetailView.as_view(), name='serie_detail'),
    path('<int:pk>/', views.SerieDetailView.as_view(), name='serie_detail_by_id'),
    path('favorite_series/add/', views.FavoriteTVShowCreateView.as_view(), name='favorite_serie_create')
]