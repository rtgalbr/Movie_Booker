from django.urls import path
from movies.views import ChangePasswordView
from movies.views import home, landing, login_view, signup_view, profile, browse, browse_detail


urlpatterns = [
    path('', landing, name='landing'),  # Landing page (accessible without login)
    path('home/', home, name='home'),   # Home page (requires login)
    path('userlogin/', login_view, name='userlogin'),
    path('usersignup/', signup_view, name='usersignup'),
    path('home/profile/', profile, name='user_profile'),
    path('browse/', browse, name='browse'),
    path('browse/<int:movie_id>/', browse_detail, name='browse_id'),
    path('password-change/', ChangePasswordView.as_view(), name='password_change'),
    
   
]