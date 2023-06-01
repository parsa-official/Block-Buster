from django.shortcuts import render,redirect
from django.views import View
from django.views.generic import ListView, DetailView
from .models import Person
from cinema.models import Movie
from television.models import TVShow
from django.db.models import Count
from django_countries import countries

class CelebListView(ListView):
    model = Person
    context_object_name = 'celebs'
    template_name = 'people/celebs_list.html'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['celebs_count'] = Person.objects.aggregate(total=Count('id'))['total']
        return context

class CelebGridView(ListView):
    model = Person
    context_object_name = 'celebs'
    template_name = 'people/celebs_grid.html'
    paginate_by = 12

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['celebs_count'] = Person.objects.aggregate(total=Count('id'))['total']
        
        return context    

class CelebDetailView(DetailView):
    model = Person
    template_name = 'people/celeb_detail.html'
    context_object_name = 'celeb'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        celeb = self.get_object()
        movies_directed = Movie.objects.filter(directors=celeb)
        movies_written = Movie.objects.filter(writers=celeb)
        movies_cast = Movie.objects.filter(casts__person=celeb)
        movies = set(list(movies_directed) + list(movies_written) + list(movies_cast))
        
        series_written = TVShow.objects.filter(writers=celeb)
        series_cast = TVShow.objects.filter(casts__person=celeb)
        series = set(list(series_written) + list(series_cast))

        context['movies'] = movies
        context['series'] = series
        context['countries'] = [celeb.country.name] 
        return context