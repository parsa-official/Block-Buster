from django.contrib import admin
from .models import TVShow,Season,Cast,Network
from django import forms
from django.utils.text import slugify
from cinema.models import Movie, Genre
from people.models import Person
from imdb import Cinemagoer
from django_countries import countries
from django.contrib import messages

class CastInline(admin.TabularInline):
    model = Cast
    extra = 1
    sortable_field_name = 'order'

class TVShowAdminForm(forms.ModelForm):
    use_imdb = forms.BooleanField(label='Use IMDb Sync', required=False)

    class Meta:
        model = TVShow
        fields = '__all__'

class TVShowAdmin(admin.ModelAdmin):
    form = TVShowAdminForm
    list_display = ('title', 'release_year', 'rating', 'status')
    inlines = [CastInline]

    fieldsets = (
        ('General Information', {
            'fields': ('title','rating', 'slug','network' ),
        }),
        ('IMDb Information', {
            'fields': ('imdb_id', 'use_imdb'),
        }),
        ('Status Information', {
            'fields': ( 'status','release_year', 'finish_year', 'num_seasons',),
        }),
        ('Display Information', {
            'fields': ('image', 'is_on_slideshow'),
        }),
        ('Other Information', {
            'fields': ('synopsis', 'runtime','mpaa_rating', 'genres', 'country', 'plot_keywords'),
        }),
        ('Cast Information', {
            'fields': ('cast', 'writers'),
        }),
    )

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)

        if form.cleaned_data.get('use_imdb', False):
            # try:
                # Fetch additional movie information from IMDb using IMDbPY
                ia = Cinemagoer()
                imdb_id = form.cleaned_data['imdb_id']
                movie = ia.get_movie(imdb_id)

                # Update movie fields with IMDb information
                form.instance.title = movie.get('title', '')
                form.instance.rating = movie.get('rating', None)
                form.instance.num_seasons = movie.get('number of seasons')
                form.instance.synopsis = movie.get('plot outline', [''])
                form.instance.release_year = movie.get('year', None)

                # Update runtime
                runtime_list = movie.get('runtime', ['0'])
                form.instance.runtime = int(runtime_list[0])

                # Update genres
                genre_list = movie.get('genres', [])
                form.instance.genres.clear()
                for genre_name in genre_list:
                    genre, _ = Genre.objects.get_or_create(name=genre_name)
                    form.instance.genres.add(genre)
                
                # Update writers
                form.instance.writers.all().delete()
                writer_list = movie.get('writers', [])
                for writer in writer_list:
                    writer_name = writer.get('name')
                    if writer_name is not None:
                        writer_obj, _ = Person.objects.get_or_create(name=writer_name)
                        form.instance.writers.add(writer_obj)

                # Update country
                imdb_countries = movie.get('countries', [])
                selected_countries = []
                for country_code, country_name in countries:
                    if country_name in imdb_countries:
                        selected_countries.append(country_code)
                form.instance.country = selected_countries

                # Delete existing cast and add new cast members from IMDb
                form.instance.casts.all().delete()

                character_names = []
                for i, character in enumerate(movie.get('cast', [])):
                    if i >= 6:
                        break
                    try:
                        actor_name = character.get('name')
                        role_name = character.currentRole
                        if actor_name and role_name:
                            formatted_name = f"{actor_name} ({role_name})"
                            character_names.append(formatted_name)
                    except AttributeError:
                        # Skip cast members with missing role information
                        continue

                # Add the cast members with their character names
                for character_name in character_names:
                    actor_name, role_name = character_name.split(' (')
                    role_name = role_name.rstrip(')')
                    person_obj, _ = Person.objects.get_or_create(name=actor_name)
                    cast_member = Cast.objects.create(tvshow=form.instance, person=person_obj, character_name=role_name)
                    form.instance.casts.add(cast_member)

                # form.instance.save()
            # except Exception as e:
            #     # Error occurred while fetching data from IMDb API
            #     self.message_user(request, f"Failed to fetch IMDb data: {str(e)}", level=messages.ERROR)
            #     return

        # Generate slug if it doesn't exist
        if not form.instance.slug:
            base_slug = slugify(form.instance.title)
            release_year = form.instance.release_year
            if release_year:
                form.instance.slug = f"{base_slug}-{release_year}"
            else:
                form.instance.slug = base_slug
        form.instance.save()


admin.site.register(TVShow,TVShowAdmin)
admin.site.register(Season)
admin.site.register(Network)