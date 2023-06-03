from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, FormView
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, PasswordChangeView
from .forms import UserRegistrationForm,UserLoginForm,EditProfileForm, ChangeProfilePictureForm
from .models import Profile,FavoriteMovie,FavoriteTVShow
from django.shortcuts import redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist

class UserRegisterView(View):
	form_class = UserRegistrationForm
	template_name = 'blog/home.html'

	def dispatch(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			return redirect('blog:home')
		return super().dispatch(request, *args, **kwargs)

	def get(self, request):
		form = self.form_class()
		return render(request, self.template_name, {'form':form})

	def post(self, request):
		form = self.form_class(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			User.objects.create_user(cd['username'], cd['email'], cd['password1'])
			messages.success(request, 'you registered successfully , Welcome', 'success')
			logged_in = authenticate(request,username=cd['username'], email=cd['email'], password=cd['password1']) 
			login(request,logged_in)      
			return redirect('blog:home')
		messages.error(request, 'Invalid Informationm , try again please.', 'warning')
		return render(request, self.template_name, {'form':form})

class UserLoginView(View):
	form_class = UserLoginForm
	template_name = 'blog/home.html'

	def setup(self, request, *args, **kwargs):
		self.next = request.GET.get('next')
		return super().setup(request, *args, **kwargs)

	def dispatch(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			return redirect('blog:home')
		return super().dispatch(request, *args, **kwargs)

	def get(self, request):
		form = self.form_class
		return render(request, self.template_name, {'form':form})

	def post(self, request):
		form = self.form_class(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			user = authenticate(request, username=cd['username'], password=cd['password'])
			if user is not None:
				login(request, user)
				messages.success(request, 'you logged in successfully', 'success')
				if self.next:
					return redirect(self.next)
				return redirect('blog:home')
			messages.error(request, 'username or password is wrong', 'warning')
		return render(request, self.template_name, {'form':form})


class UserLogoutView(LoginRequiredMixin, View):
	def get(self, request):
		logout(request)
		messages.success(request, 'you logged out successfully', 'success')
		return redirect('blog:home')

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'account/userprofile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context
    
    
class EditProfileView(LoginRequiredMixin, FormView):
    template_name = 'account/edit_profile.html'
    form_class = EditProfileForm
    success_url = '/user/'

    def form_valid(self, form):
        try:
            profile = self.request.user.profile
            user = profile.user
        except ObjectDoesNotExist:
            # If the profile does not exist, create a new one
            profile = Profile(user=self.request.user)
            user = self.request.user


        # Validate username uniqueness
        new_username = form.cleaned_data['username']
        if user.username != new_username and User.objects.filter(username=new_username).exists():
            form.add_error('username', 'Username already exists')

        # Validate email uniqueness and format
        new_email = form.cleaned_data['email']
        if user.email != new_email and User.objects.filter(email=new_email).exists():
            form.add_error('email', 'Email already exists')

        # Validate phone number format
        new_phone_number = form.cleaned_data['phone_number']
        if not form.fields['phone_number'].clean(new_phone_number):
            form.add_error('phone_number', 'Invalid phone number format')

        # Update profile and user information
        user.username = new_username
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.email = new_email
        profile.country = form.cleaned_data['country']
        profile.phone_number = new_phone_number

        # Save changes
        user.save()
        profile.save()

        return super().form_valid(form)

#Movies FAVORITE
class FavoriteMovieListView(LoginRequiredMixin, View):
    def get(self, request):
        favorite_movies = FavoriteMovie.objects.filter(user=request.user)
        return render(request, 'account/user_favorite_movies.html', {'favorite_movies': favorite_movies})

class FavoriteMovieEditView(LoginRequiredMixin, View):
    def get(self, request):
        favorite_movies = FavoriteMovie.objects.filter(user=request.user)
        return render(request, 'account/user_favorite_movies_edit.html', {'favorite_movies': favorite_movies})

class FavoriteMovieDeleteView(LoginRequiredMixin, View):
    def get(self, request, movie_id):
        favorite_movie = get_object_or_404(FavoriteMovie, id=movie_id, user=request.user)
        favorite_movie.delete()
        return redirect('account:favorite_movies_edit')


#Series FAVORITE
class FavoriteTVShowListView(LoginRequiredMixin, View):
    def get(self, request):
        favorite_series = FavoriteTVShow.objects.filter(user=request.user)
        return render(request, 'account/user_favorite_series.html', {'favorite_series': favorite_series})
    
class FavoriteTVShowEditView(LoginRequiredMixin, View):
    def get(self, request):
        favorite_series = FavoriteTVShow.objects.filter(user=request.user)
        return render(request, 'account/user_favorite_series_edit.html', {'favorite_series': favorite_series})    

class FavoriteTVShowDeleteView(LoginRequiredMixin, View):
    def get(self, request, tvshow_id):
        favorite_serie = get_object_or_404(FavoriteTVShow, id=tvshow_id, user=request.user)
        favorite_serie.delete()
        return redirect('account:favorite_series_edit')


class ChangeProfilePictureView(LoginRequiredMixin, View):
    form_class = ChangeProfilePictureForm
    template_name = 'account/change_profile_picture.html'
    success_url = '/user/'  # Update with the desired success URL

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            user = request.user

            # Check if the user has a profile
            if hasattr(user, 'profile'):
                profile = user.profile
            else:
                # Create a new profile for the user
                profile = Profile(user=user)

            # Delete previous profile picture if exists
            if profile.profile_picture:
                profile.profile_picture.delete()

            # Save the new profile picture
            profile.profile_picture = form.cleaned_data['profile_picture']
            profile.save()

            return redirect(self.success_url)

        return render(request, self.template_name, {'form': form})


class ChangePasswordView(LoginRequiredMixin, PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = 'account/change_password.html'
    success_url = reverse_lazy('account:profile')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Password has been changed Successfully.', 'success')
        return response

    def form_invalid(self, form):
        messages.error(self.request, 'Something is Invalid. Please try again.', 'warning')
        return super().form_invalid(form)
    
class UserPasswordResetView(PasswordResetView):
    template_name = 'account/password_reset_form.html'
    success_url = reverse_lazy('blog:home')
    email_template_name = 'account/password_reset_email.html'

    def form_valid(self, form):
        email = form.cleaned_data.get('email')

        if not User.objects.filter(email=email).exists():
            messages.error(
                self.request,
                'Email address is not registered. Please enter a valid email.'
            )
            return self.form_invalid(form)

        response = super().form_valid(form)
        messages.success(
            self.request,
            'Please check your Email.Password reset email has been sent.'
        )
        return redirect(self.success_url)


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'account/password_reset_confirm.html'
    success_url = reverse_lazy('blog:home')

    def form_invalid(self, form):
        messages.error(self.request, 'Passwords do Not Match or are Not Valid.')
        return super().form_invalid(form)

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Password has been successfully reset.')
        return redirect(self.success_url)
