from django.contrib import admin
from .models import Movie
from .models import Profile


# Register your models here.

class MovieAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

admin.site.register(Movie, MovieAdmin)

admin.site.register(Profile)