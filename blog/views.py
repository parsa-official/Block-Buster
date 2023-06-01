from django.shortcuts import render,redirect
from django.views import View
from django.views.generic import ListView, DetailView
from .models import Trailer,BlogArticle
from django.views.generic import ListView
from cinema.models import Movie


# class SlideShowView(ListView):
#     model = Movie
#     context_object_name = 'movies'
#     template_name = 'blog/home.html'


class Home(ListView):
    model = Trailer
    template_name = 'blog/home.html'
    context_object_name = 'trailers'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['movies'] = Movie.objects.all()
        context['blogs'] = BlogArticle.objects.all()
        return context

class AboutUsView(View):
    def get(self, request):
        return render(request, 'about.html')

class BlogListView(ListView):
    model = BlogArticle
    template_name = 'blog/blog_list.html'
    context_object_name = 'blogs'
    paginate_by = 5

class BlogDetailView(DetailView):
    model = BlogArticle
    template_name = 'blog/blog_detail.html'
    context_object_name = 'blog'

# def custom_404_view(request, exception):
#     return render(request, '404.html', status=404)    