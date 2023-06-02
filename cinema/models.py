from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from people.models import Person
from django.contrib.auth.models import User
from datetime import datetime
from django_countries.fields import CountryField


MPAA_CHOICES = [
    ('G', 'General Audiences'),
    ('PG', 'Parental Guidance Suggested'),
    ('PG-13', 'Parents Strongly Cautioned'),
    ('R', 'Restricted'),
    ('NC-17', 'No One 17 and Under Admitted')
]

class Genre(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class PlotKeyword(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Movie(models.Model):
    imdb_id = models.CharField(max_length=9, unique=True, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    release_year = models.IntegerField(
        validators=[
            MinValueValidator(1900),
            MaxValueValidator(datetime.now().year)
        ],
        blank=True,
        null=True
    )
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1, validators=[MinValueValidator(1.0), MaxValueValidator(10.0)], blank=True, null=True)
    mpaa_rating = models.CharField(max_length=5, choices=MPAA_CHOICES, blank=True)
    image = models.ImageField(upload_to='movie_images', blank=True, null=True)
    runtime = models.PositiveIntegerField(blank=True, null=True)
    synopsis = models.TextField(blank=True, null=True)
    is_on_slideshow = models.BooleanField(default=False)
    genres = models.ManyToManyField(Genre, blank=True)
    country = CountryField(multiple=True , blank=True)
    cast = models.ManyToManyField('Cast', related_name='movies', blank=True)
    directors = models.ManyToManyField(Person, related_name='directed_movies', blank=True)
    writers = models.ManyToManyField(Person, related_name='written_movies', blank=True)
    plot_keywords = models.ManyToManyField(PlotKeyword, blank=True)
    youtube_trailer_code = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return f'{self.title} - {self.release_year}'
    
    def get_absolute_url(self):
        return reverse('cinema:movie_detail', args=[self.pk, self.slug])
    
    
class Cast(models.Model):
    movie = models.ForeignKey(Movie, related_name='casts', on_delete=models.CASCADE)
    person = models.ForeignKey(Person, related_name='cinema_casts', on_delete=models.CASCADE)
    character_name = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.person} as {self.character_name} in {self.movie.title}'


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ucomments')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='mcomments')
    body = models.TextField(max_length=400)
    created = models.DateTimeField(auto_now_add=True)
    liked_users = models.ManyToManyField(User, related_name='liked_comments', blank=True)

    def __str__(self):
        return f'{self.user} - {self.body[:30]}'

