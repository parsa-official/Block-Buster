from django.contrib import admin
from .models import Profile,FavoriteMovie,FavoriteTVShow
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.contrib import messages

class ProfileInline(admin.StackedInline):
	model = Profile
	can_delete = False


class ExtendedUserAdmin(UserAdmin):
	inlines = (ProfileInline,)

@admin.register(FavoriteMovie)
class FavoriteMovieAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        existing_favorites = FavoriteMovie.objects.filter(user=obj.user, movie=obj.movie)
        
        if existing_favorites.exists():
            self.message_user(request, "existed", level=messages.ERROR)
            return  # Do not save the model if the movie already exists in the user's favorites
        
        super().save_model(request, obj, form, change)


@admin.register(FavoriteTVShow)
class FavoriteTVShowAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        existing_favorites = FavoriteTVShow.objects.filter(user=obj.user, tvshow=obj.tvshow)
        
        if existing_favorites.exists():
            self.message_user(request, "This TVShow/Serie already existed in User favorites", level=messages.ERROR)
            return  # Do not save the model if the movie already exists in the user's favorites
        
        super().save_model(request, obj, form, change)


admin.site.unregister(User)
admin.site.register(User, ExtendedUserAdmin)


