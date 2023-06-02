from django.urls import path
from . import views

app_name = 'cinema'

urlpatterns = [
    path('', views.MovieListView.as_view(), name='movies_list'),
    path('grid/', views.MovieGridView.as_view(), name='movies_grid'),
    path('<int:pk>/<slug:slug>/', views.MovieDetailView.as_view(), name='movie_detail'),
    path('<int:pk>/', views.MovieDetailView.as_view(), name='movie_detail_by_id'),
    path('search_results/', views.SearchMoviesView.as_view(), name='search_results'),
    path('favorite_movies/add/', views.FavoriteMovieCreateView.as_view(), name='favorite_movie_create'),
]