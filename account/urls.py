from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('', views.ProfileView.as_view(), name='profile'),
    path('edit_profile/', views.EditProfileView.as_view(), name='edit_profile'),
    path('change_avatar/', views.ChangeProfilePictureView.as_view(), name='change_profile_picture'),
    path('favorites/movies/', views.FavoriteMovieListView.as_view(), name='favorite_movies'),
    path('favorites/movies/edit/', views.FavoriteMovieEditView.as_view(), name='favorite_movies_edit'),
    path('favorite/movies/delete/<int:movie_id>/', views.FavoriteMovieDeleteView.as_view(), name='delete_favorite_movie'),
    path('favorites/series/', views.FavoriteTVShowListView.as_view(), name='favorite_series'),
    path('favorites/series/edit/', views.FavoriteTVShowEditView.as_view(), name='favorite_series_edit'),
    path('favorite/series/delete/<int:tvshow_id>/', views.FavoriteTVShowDeleteView.as_view(), name='delete_favorite_serie'),
    path('change_password/', views.ChangePasswordView.as_view(), name='change_password'),
    path('reset_password/', views.UserPasswordResetView.as_view(), name='reset_password'),
	path('reset_password/confirm/<uidb64>/<token>/', views.UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('signup/', views.UserRegisterView.as_view(), name='signup'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
]