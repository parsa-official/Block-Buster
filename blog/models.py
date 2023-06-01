from django.db import models
from django.urls import reverse
from ckeditor.fields import RichTextField
from cinema.models import PlotKeyword

class Trailer(models.Model):
    title = models.CharField(max_length=255)
    youtube_code = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class BlogCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class BlogArticle(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    image = models.ImageField(upload_to='news_images')
    pub_date = models.DateTimeField()
    content = RichTextField()
    plot_keywords = models.ManyToManyField(PlotKeyword)
    category = models.ForeignKey(BlogCategory, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('blog:blog_detail', args=[self.pk])