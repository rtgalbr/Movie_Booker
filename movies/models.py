from django.db import models
from django.contrib.auth.models import User

class Movie(models.Model):
    Title = models.CharField(max_length=255)
    image = models.ImageField(upload_to="movies/files/covers")
    description = models.TextField(max_length=2000)
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    avatar = models.ImageField(default='default.png', upload_to='movies/profiles/profile_images')
    bio = models.TextField()

    def __str__(self):
        return self.user.username