from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from allauth.account.forms import LoginForm, SignupForm
from django.contrib import messages
from movies.forms import UpdateProfileForm, UpdateUserForm
from movies.models import Movie
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from . models import Review 
from . forms import ReviewForm
from movies.models import Seat
import uuid
from .models import FutureMovie
from .models import Movie, Showtime, Ticket, SeatSelection


def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)  # Bind data from the request
        if form.is_valid():
            form.save(request)  # Save the user
            messages.success(request, 'Your account has been created successfully!')
            return redirect('hub')  # Redirect to the login page or any other page
    else:
        form = SignupForm()  # Create a new instance of the form

    return render(request, 'authentication/landing.html', {'form': form})  # Render the form in the template

def login_view(request):
    form = LoginForm()
    return render(request, 'authentication/landing.html', {'form': form})  


def landing(request):
    return render(request, 'authentication/landing.html')


def home(request):
    return render(request, 'user/home.html')

@login_required
def hub(request):
    return render(request, 'user/hub.html', {'user': request.user})

def browse(request):
    query = request.GET.get('search')
    if query:
        movies = Movie.objects.filter(Title__icontains=query)
    else:
        movies = Movie.objects.all()
    return render(request, 'catalog/browse.html', {'movies': movies})

def browse_detail(request, movie_id):
    movie = Movie.objects.get (pk=movie_id)
    showtimes = Showtime.objects.filter(movie=movie).prefetch_related('seats')
    
    for st in showtimes:
        st.available_seats_count = st.seats.filter(is_taken=False).count()
    
    reviews = Review.objects.filter(movie=movie_id).order_by("-content")
    return render(request, 'catalog/movie_detail.html', {'movie': movie, 'showtimes':showtimes})

@login_required
def ticket_purchases(request):
    tickets = Ticket.objects.filter(user=request.user, purchased=True)
    return render(request, 'user/ticket_purchases.html', {'tickets': tickets})

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

@login_required   
def movie_reviews(request, movie_id):
    movie = Movie.objects.get(pk=movie_id)
    reviews = Review.objects.filter(movie=movie)

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('userlogin')
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.movie = movie
            review.user = request.user
            review.save()
            messages.success(request, 'Review submitted!')
            return redirect('movie_reviews', movie_id=movie_id)
    else:
        form = ReviewForm()

    return render(request, 'catalog/reviews.html', {
        'movie': movie,
        'reviews': reviews,
        'form': form
    })
    
@login_required
def buy_tickets(request, showtime_id):
    showtime = get_object_or_404(Showtime, pk=showtime_id)
    available_seats = showtime.seats.filter(is_taken=False)

    if request.method == 'POST':
        selected_seat_ids = request.POST.getlist('selected_seats')
        
        if not selected_seat_ids:
            messages.error(request, "Please select at least one seat.")
            return redirect('buy_tickets', showtime_id=showtime.id)

        
        ticket = Ticket.objects.create(user=request.user, showtime=showtime, purchased=False)

        for seat_id in selected_seat_ids:
            seat = Seat.objects.get(id=seat_id, showtime=showtime, is_taken=False)
            

            SeatSelection.objects.create(ticket=ticket, seat_number=seat.seat_number)

       
        messages.success(request, "Redirecting to payment options...")
        return redirect('payment_options', ticket_id=ticket.id)

    return render(request, 'catalog/buy_tickets.html', {
        'showtime': showtime,
        'available_seats': available_seats
    })    

@login_required
def payment_options(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id, user=request.user, purchased=False)
    num_seats = ticket.seat_selections.count()
    total_price = num_seats * 10  

    return render(request, 'payment/payment_options.html', {
        'ticket': ticket,
        'total_price': total_price
    })

@login_required
def payment_verify(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id, user=request.user, purchased=False)

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'verify':
           
            ticket.purchased = True
            ticket.ticket_code = str(uuid.uuid4()).split('-')[0]  
            ticket.save()

           
            for seat_selection in ticket.seat_selections.all():
                seat = Seat.objects.get(showtime=ticket.showtime, seat_number=seat_selection.seat_number)
                seat.is_taken = True
                seat.save()

            messages.success(request, "Payment verified! Your ticket has been booked.")
            return redirect('ticket_purchases')

        else:
            
            ticket.delete()
            messages.error(request, "Payment failed. Please try again.")
            return redirect('browse_id', movie_id=ticket.showtime.movie.id)

    return render(request, 'payment/verify_payment.html', {'ticket': ticket})

@login_required
def payment_fail(request, ticket_id):
    movie_id = Ticket.objects.get(id=ticket_id).showtime.movie.id
    return redirect('browse_id', movie_id=movie_id)

def browse_choice(request):
    return render(request, 'catalog/browse_choice.html')


def future_catalog(request):
    search_query = request.GET.get('search', '')
    qs = FutureMovie.objects.all()
    if search_query:
        qs = qs.filter(Title__icontains=search_query)
    return render(request, 'catalog/future_catalog.html', {'movies': qs})


def future_movie_detail(request, pk):
    future = get_object_or_404(FutureMovie, pk=pk)
    return render(request, 'catalog/future_movie_detail.html', {
        'movie': future
    })