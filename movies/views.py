from django.http import Http404
from django.shortcuts import  render, redirect
from django.contrib.auth.decorators import login_required
from allauth.account.forms import LoginForm, SignupForm
from django.contrib import messages
from movies.models import Movie

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
    return render(request, 'user/profile.html')