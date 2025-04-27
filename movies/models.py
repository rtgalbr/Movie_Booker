from django.utils import timezone
import uuid
from django.db import models
from django.contrib.auth.models import User



class Movie(models.Model):
    Title = models.CharField(max_length=255)
    image = models.ImageField(upload_to="movies/files/covers")
    description = models.TextField(max_length=2000)
    
class FutureMovie(models.Model):
    Title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='future_movies/', blank=True, null=True)
    release_date = models.CharField(
        max_length=100,
        blank=True,
        help_text="Expected Release Date"
    )
    description = models.TextField(
        blank=True,
        help_text="Description of movie"
    )

    def __str__(self):
        return f"{self.Title} ({self.release_date})"

    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    avatar = models.ImageField(default='default.png', upload_to='movies/profiles/profile_images')
    bio = models.TextField()

    def __str__(self):
        return self.user.username

class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    rating = models.IntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.movie.Title}"
    
class Showtime(models.Model):
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(default=timezone.now)
    location = models.CharField(max_length=100, default="Theater One")

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            self.generate_seats()

    def generate_seats(self):
        for i in range(1, 11):  # A1 to A10
            Seat.objects.get_or_create(showtime=self, seat_number=f"A{i}")

    def __str__(self):
        return f"{self.movie.Title} - {self.start_time} at {self.location}"
    
class Seat(models.Model):
    showtime = models.ForeignKey(Showtime, on_delete=models.CASCADE, related_name='seats')
    seat_number = models.CharField(max_length=10)
    is_taken = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.seat_number} - {'Taken' if self.is_taken else 'Available'}"
    
class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    showtime = models.ForeignKey(Showtime, on_delete=models.CASCADE, related_name="tickets")
    purchased = models.BooleanField(default=False)
    ticket_code = models.CharField(max_length=100, blank=True, null=True) 

    def generate_ticket_code(self):
        if not self.ticket_code:
            self.ticket_code = str(uuid.uuid4()).split('-')[0]
            self.save()

    def __str__(self):
        return f"{self.user.username} - {self.showtime.movie.Title} - {self.showtime.start_time}"
    
class SeatSelection(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='seat_selections')
    seat_number = models.CharField(max_length=10)

    def __str__(self):
        return f"Seat {self.seat_number} for {self.ticket.user.username}"
