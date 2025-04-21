from django.http import Http404
from django.shortcuts import  render, redirect
from django.contrib.auth.decorators import login_required
from allauth.account.forms import LoginForm, SignupForm
from django.contrib import messages
from movies.forms import UpdateProfileForm, UpdateUserForm
from movies.models import Movie
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin


def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)  # Bind data from the request
        if form.is_valid():
            form.save(request)  # Save the user
            messages.success(request, 'Your account has been created successfully!')
            return redirect('userlogin')  # Redirect to the login page or any other page
    else:
        form = SignupForm()  # Create a new instance of the form

    return render(request, 'authentication/signup.html', {'form': form})  # Render the form in the template

def login_view(request):
    form = LoginForm()
    return render(request, 'authentication/login.html', {'form': form})  


def landing(request):
    return render(request, 'authentication/landing.html')

@login_required
def home(request):
    return render(request, 'user/home.html', {'user': request.user})

def browse(request):
    query = request.GET.get('search')
    if query:
        movies = Movie.objects.filter(Title__icontains=query)
    else:
        movies = Movie.objects.all()
    return render(request, 'catalog/browse.html', {'movies': movies})

def browse_detail(request, movie_id):
    movie = Movie.objects.get (pk=movie_id)
    return render(request, 'catalog/movie_detail.html', {'movie': movie})

@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='user_profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'user/profile.html', {'user_form': user_form, 'profile_form': profile_form})

class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'user/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('users-home')