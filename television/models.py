from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from cinema.models import Genre,PlotKeyword
from people.models import Person
from datetime import datetime
from django_countries.fields import CountryField
from django.contrib.auth.models import User


class Network(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


MPAA_CHOICES = [
    ('TV-Y', 'Suitable for all Children'),
    ('TV-Y7', 'Suitable for Children aged 7 and up'),
    ('TV-G', 'Suitable for all ages)'),
    ('TV-PG', 'Parental Guidance Suggested'),
    ('TV-14', 'Parents Strongly Cautioned'),
    ('TV-MA', 'Mature Audiences Only')
]


class TVShow(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField(max_length=255, blank=True, null=True)
    release_year = models.IntegerField(
        validators=[
            MinValueValidator(1900),
            MaxValueValidator(datetime.now().year)
        ],
        blank=True,
        null=True
    )
    finish_year = models.IntegerField(
        validators=[
            MinValueValidator(1900),
            MaxValueValidator(datetime.now().year)
        ],
        blank=True,
        null=True
    )    
    imdb_id = models.CharField(max_length=9, unique=True, blank=True, null=True)
    network = models.ForeignKey(Network, on_delete=models.CASCADE, null=True, blank=True)
    mpaa_rating = models.CharField(max_length=5, choices=MPAA_CHOICES, blank=True, null=True)
    image = models.ImageField(upload_to='tvshow_images', blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1, validators=[MinValueValidator(1.0), MaxValueValidator(10.0)], blank=True, null=True)
    runtime = models.PositiveIntegerField(blank=True, null=True)
    synopsis = models.TextField(blank=True, null=True)
    is_on_slideshow = models.BooleanField(default=False)
    num_seasons = models.PositiveIntegerField(blank=True, null=True)
    status = models.CharField(max_length=50, choices=[('now playing', 'Now Playing'), ('ended', 'Ended')],blank=True)
    country = CountryField(multiple=True , blank=True)
    genres = models.ManyToManyField(Genre,blank=True)
    plot_keywords = models.ManyToManyField(PlotKeyword,blank=True)
    cast = models.ManyToManyField('Cast', related_name='movies', blank=True)
    writers = models.ManyToManyField(Person, related_name='written_tvshow', blank=True)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('television:serie_detail', args=[self.pk, self.slug])
    
    
class Cast(models.Model):
    tvshow = models.ForeignKey(TVShow, related_name='casts', on_delete=models.CASCADE)
    person = models.ForeignKey(Person, related_name='television_casts', on_delete=models.CASCADE)
    character_name = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.person.name} ({self.character_name}) in {self.tvshow.title}'
    
class Season(models.Model):
    season_number = models.PositiveIntegerField()
    image = models.ImageField(upload_to='season_images')
    tv_show = models.ForeignKey(TVShow, on_delete=models.CASCADE, related_name='seasons')
    episode_number = models.PositiveIntegerField()

    class Meta:
        ordering = ['tv_show__title', 'season_number']
        
    def __str__(self):
        return f'Season {self.season_number} - {self.tv_show.title}'

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='series_ucomments')
    tvshow = models.ForeignKey(TVShow, on_delete=models.CASCADE, related_name='series_mcomments')
    body = models.TextField(max_length=400)
    created = models.DateTimeField(auto_now_add=True)
    liked_users = models.ManyToManyField(User, related_name='series_liked_comments', blank=True)

    def __str__(self):
        return f'{self.user} - {self.body[:30]}'