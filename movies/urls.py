from django.urls import path
from movies.views import ChangePasswordView
from movies.views import home, hub, landing, login_view, signup_view, profile, browse, browse_detail, movie_reviews, buy_tickets, payment_options, payment_verify, payment_fail, ticket_purchases, browse_choice, future_catalog, future_movie_detail


urlpatterns = [
    path('landing/', landing, name='landing'),  # Landing page (accessible without login)
    path('', home, name='home'), 
    path('hub/', hub, name='hub'),# Home page (requires login)
    path('userlogin/', login_view, name='userlogin'),
    path('usersignup/', signup_view, name='usersignup'),
    path('user/profile/', profile, name='user_profile'),
    path('browse/', browse, name='browse'),
    path('browse/<int:movie_id>/', browse_detail, name='browse_id'),
    path('movie/<int:movie_id>/reviews/', movie_reviews, name='movie_reviews'),
    path('password-change/', ChangePasswordView.as_view(), name='password_change'),
    path('showtime/<int:showtime_id>/buy/', buy_tickets, name='buy_tickets'),
    path('payment/<int:ticket_id>/', payment_options, name='payment_options'),
    path('payment/<int:ticket_id>/verify/', payment_verify, name='payment_verify'),
    path('payment/<int:ticket_id>/fail/', payment_fail, name='payment_fail'),
    path('ticket_purchases/', ticket_purchases, name='ticket_purchases'),
    path('browse/future/', future_catalog, name='future_catalog'),
    path('future/<int:pk>/', future_movie_detail, name='future_movie_detail'),
]