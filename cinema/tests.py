from django.test import TestCase
from imdb import Cinemagoer
from cinema.models import Genre

# Create your tests here.
imdb_id = '1375666'  # Example IMDb ID for "Inception"
ia = Cinemagoer()
movie = ia.get_movie(imdb_id)

# Fetch the genre names from the Genre model
genre_names = Genre.objects.values_list('name', flat=True)

for genre in movie['genres']:
    if genre in genre_names:
        genre_obj = Genre.objects.get(name=genre)
        print(genre_obj)