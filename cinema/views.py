from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView
from django.views import View
from .models import Movie,Comment
from django.contrib import messages
from television.models import TVShow
from people.models import Person
from account.models import FavoriteMovie
from django.db.models import Count
from django_countries import countries
from django.urls import reverse_lazy
from .forms import CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class MovieListView(ListView):
    model = Movie
    context_object_name = 'movies'
    template_name = 'cinema/movies_list.html'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['movies_count'] = Movie.objects.aggregate(total=Count('id'))['total']
        return context

class MovieGridView(ListView):
    model = Movie
    context_object_name = 'movies'
    template_name = 'cinema/movies_grid.html'
    paginate_by = 8

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['movies_count'] = Movie.objects.aggregate(total=Count('id'))['total']
        return context

class MovieDetailView(DetailView):
    model = Movie
    template_name = 'cinema/movie_detail.html'
    slug_url_kwarg = 'slug'
    paginate_by = 20
    form_class = CommentForm

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        slug = self.kwargs.get('slug')
        if pk is not None:
            return get_object_or_404(Movie, pk=pk)
        elif slug is not None:
            return get_object_or_404(Movie, slug=slug)
        else:
            return None

    def get(self, request, *args, **kwargs):
        object = self.get_object()
        if object is None:
            return super().get(request, *args, **kwargs)
        else:
            canonical_url = reverse('cinema:movie_detail', kwargs={
                'pk': object.pk,
                'slug': object.slug,
            })
            requested_url = request.path_info

            if requested_url != canonical_url:
                return redirect(canonical_url)

            comments = Comment.objects.filter(movie=object, is_reply=False).order_by('-created')
            comment_count = comments.count()
            is_favorite = False
            if request.user.is_authenticated:
                favorite_movies = FavoriteMovie.objects.filter(user=request.user, movie=object)
                is_favorite = favorite_movies.exists()
                

            paginator = Paginator(comments, self.paginate_by)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

            context = {
                'movie': object,
                'genres': object.genres.all(),
                'cast': object.casts.all(),
                'directors': object.directors.all(),
                'writers': object.writers.all(),
                'plotkeys': object.plot_keywords.all(),
                'countries': [countries.name(code) for code in object.country],
                'comments': page_obj,  # Pass the paginated comments to the template
                'comment_count': comment_count,
                'comment_form': CommentForm(),  # Add the comment form to the context
                'is_favorite': is_favorite,
            }

            return render(request, self.template_name, context)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        object = self.get_object()
        form = self.form_class(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.movie = object
            new_comment.save()
            messages.success(request, 'Your comment was submitted successfully.', 'success')
        else:
            messages.error(request, 'There was an error submitting your comment.', 'error')
        return redirect('cinema:movie_detail', pk=object.pk, slug=object.slug)


        
class SearchMoviesView(View):

    def get(self, request):
        return render(request, 'cinema/search_results.html')
    
    def post(self, request):
        searched = request.POST.get('searched', '')
        movies = Movie.objects.filter(title__icontains=searched)
        series = TVShow.objects.filter(title__icontains=searched)
        celebs = Person.objects.filter(name__icontains=searched)
        context = {'searched': searched, 'movies': movies, 'series': series, 'celebs': celebs}
        return render(request, 'cinema/search_results.html', context)


class FavoriteMovieCreateView(LoginRequiredMixin, View):
    def get(self, request):
        movie_id = request.GET.get('movie_id')
        movie = Movie.objects.get(id=movie_id)
        movie_in_favorites = FavoriteMovie.objects.filter(user=request.user, movie=movie).exists()

        if movie_in_favorites:
            return redirect('cinema:movie_detail', pk=movie.pk, slug=movie.slug)  # Redirect back to the movie detail page

        favorite_movie = FavoriteMovie(user=request.user, movie=movie)
        favorite_movie.save()
        return redirect('cinema:movie_detail', pk=movie.pk, slug=movie.slug)


