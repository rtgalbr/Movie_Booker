from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from allauth.account.forms import LoginForm, SignupForm
from django.contrib import messages


def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)  # Bind data from the request
        if form.is_valid():
            form.save(request)  # Save the user
            messages.success(request, 'Your account has been created successfully!')
            return redirect('userlogin')  # Redirect to the login page or any other page
    else:
        form = SignupForm()  # Create a new instance of the form

    return render(request, 'signup.html', {'form': form})  # Render the form in the template

def login_view(request):
    form = LoginForm()
    return render(request, 'login.html', {'form': form})  


def landing(request):
    return render(request, 'landing.html')

@login_required
def home(request):
    return render(request, 'home.html', {'user': request.user})