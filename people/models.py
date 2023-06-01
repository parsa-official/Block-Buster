from django.db import models
from django.urls import reverse
from time import timezone
from django_countries.fields import CountryField

JOB_CHOICES = [
    ('actor', 'Actor'),
    ('writer', 'Writer'),
    ('director', 'Director'),
]

class Person(models.Model):
    name = models.CharField(max_length=255)
    full_name = models.CharField(max_length=255, blank=True,null=True)
    job = models.CharField(max_length=10, choices=JOB_CHOICES, blank=True,null=True)
    country = CountryField(blank=True)
    birthday = models.DateField(blank=True,null=True)
    bio = models.TextField(blank=True,null=True)
    photo = models.ImageField(upload_to='people/photos', blank=True,null=True)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('people:celeb_detail', args=[self.pk])

