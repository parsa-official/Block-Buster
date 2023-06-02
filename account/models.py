from django.core.validators import RegexValidator
from django.db import models
from cinema.models import Movie
from television.models import TVShow
from django.utils import timezone
from django.contrib.auth.models import User

class Profile(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    country = models.CharField(max_length=50)
    profile_picture = models.ImageField(upload_to='profile_pictures', blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    phone_regex = RegexValidator(
        regex=r'^\+?[\d\s-]+$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=15, blank=True)
    bio = models.TextField(blank=True)
    vip_status = models.BooleanField(default=False)
    vip_expiration = models.DateField(blank=True, null=True)

    def get_vip_status_display(self):
        if self.vip_status:
            return "Active"
        else:
            return "Not Active"

    def is_vip(self):
        return self.vip_status and self.vip_expiration and self.vip_expiration > timezone.now()

class FavoriteMovie(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_mfavs')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='mfavs')

    def __str__(self):
        return f"{self.user.username} - {self.movie.title}" 

class FavoriteTVShow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_tvfavs')
    tvshow = models.ForeignKey(TVShow, on_delete=models.CASCADE, related_name='tvfavs')

    def __str__(self):
        return f"{self.user.username} - {self.tvshow.title}"     