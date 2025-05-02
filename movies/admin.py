from django.contrib import admin
from .models import Movie, Showtime, Ticket, FutureMovie, Profile, Review



@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('Title',)
    search_fields = ('Title',)
    readonly_fields = ('id',)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    pass

@admin.register(Showtime)
class ShowtimeAdmin(admin.ModelAdmin):
    list_display = ('movie','start_time', 'end_time', 'location')
    list_filter = ('location','start_time')
    search_fields = ('movie__Title',)

@admin.register(FutureMovie)
class FutureMovieAdmin(admin.ModelAdmin):
    list_display = ('Title', 'release_date')
    search_fields = ('Title',)
    fields = ('Title', 'release_date','description', 'image')

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'showtime', 'purchased', 'ticket_code','seat_list')
    list_filter = ('purchased', 'showtime')
    search_fields = ('ticket_code', 'user__username','showtime__movie__Title')
    readonly_fields = ('ticket_code',)
    actions = ['calculate_stats']
    
    def seat_list(self, obj):
        return ", ".join(seat.seat_number for seat in obj.seat_selections.all())
    seat_list.short_description = "Seats"

    @admin.action(description='Calculate Ticket Sales Stats')
    def calculate_stats(self, request, queryset):
        purchased_tickets = queryset.filter(purchased=True)
        total_seats = sum(ticket.seat_selections.count() for ticket in purchased_tickets)
        total_revenue = total_seats * 10

        self.message_user(request,f"Total Seats Sold: {total_seats} | Total Revenue: ${total_revenue}")
