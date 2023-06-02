from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView
from django.views import View
from .models import TVShow,Season,Comment
from account.models import FavoriteTVShow
from .forms import CommentForm
from django.db.models import Count
from django_countries import countries
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

class SerieListView(ListView):
    model = TVShow
    context_object_name = 'series'
    template_name = 'television/series_list.html'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['series_count'] = TVShow.objects.aggregate(total=Count('id'))['total']
        return context    

class SerieGridView(ListView):
    model = TVShow
    context_object_name = 'series'
    template_name = 'television/series_grid.html'
    paginate_by = 8
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['series_count'] = TVShow.objects.aggregate(total=Count('id'))['total']
        return context    
    
class SerieDetailView(DetailView):
    model = TVShow
    template_name = 'television/serie_detail.html'
    slug_url_kwarg = 'slug'
    paginate_by = 20
    form_class = CommentForm

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        slug = self.kwargs.get('slug')
        if pk is not None:
            return get_object_or_404(TVShow, pk=pk)
        elif slug is not None:
            return get_object_or_404(TVShow, slug=slug)
        else:
            return None

    def get(self, request, *args, **kwargs):
        
        object = self.get_object()

        if object is None:
            return super().get(request, *args, **kwargs)
        else:
            canonical_url = reverse('television:serie_detail', kwargs={
                'pk': object.pk,
                'slug': object.slug,
            })
            requested_url = request.path_info

            if requested_url != canonical_url:
                return redirect(canonical_url)

            comments = Comment.objects.filter(tvshow=object).order_by('-created')
            comment_count = comments.count()
            is_favorite = False
            if request.user.is_authenticated:
                favorite_series = FavoriteTVShow.objects.filter(user=request.user, tvshow=object)
                is_favorite = favorite_series.exists()

            paginator = Paginator(comments, self.paginate_by)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

            context = {
                'serie': object,
                'genres' : object.genres.all(),
                'seasons': Season.objects.filter(tv_show=object),
                'cast' : object.casts.all(),
                'writers' : object.writers.all(),
                'plotkeys' : object.plot_keywords.all(),
                'countries' : [countries.name(code) for code in object.country],
                'comments': page_obj,
                'comment_count': comment_count,
                'is_favorite' : is_favorite,
                }

            return render(request, self.template_name, context)
        
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        object = self.get_object()
        form = self.form_class(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.tvshow = object
            new_comment.save()
            messages.success(request, 'Your comment was submitted successfully.', 'success')
        else:
            messages.error(request, 'There was an error submitting your comment.', 'error')
        return redirect('television:serie_detail', pk=object.pk, slug=object.slug)    
    
class FavoriteTVShowCreateView(LoginRequiredMixin, View):
    def get(self, request):
        tvshow_id = request.GET.get('tvshow_id')
        tvshow = TVShow.objects.get(id=tvshow_id)
        tvshow_in_favorites = FavoriteTVShow.objects.filter(user=request.user, tvshow=tvshow).exists()

        if tvshow_in_favorites:
            return redirect('television:serie_detail', pk=tvshow.pk, slug=tvshow.slug)

        favorite_tvshow = FavoriteTVShow(user=request.user, tvshow=tvshow)
        favorite_tvshow.save()
        return redirect('television:serie_detail', pk=tvshow.pk, slug=tvshow.slug)
