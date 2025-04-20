from django.urls import path
from movies.views import home, landing, login_view, signup_view, profile, browse, browse_detail


urlpatterns = [
    path('', landing, name='landing'),  # Landing page (accessible without login)
    path('home/', home, name='home'),   # Home page (requires login)
    path('userlogin/', login_view, name='userlogin'),
    path('usersignup/', signup_view, name='usersignup'),
    path('home/profile/', profile, name='user_profile'),
    path('home/browse/', browse, name='browse'),
    path('home/browse/<int:movie_id>/', browse_detail, name='browse_id'),
    
   
]