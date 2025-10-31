from django.contrib import admin
from .models import Hotel, User, Booking, Ferry, ThemeParkTicket, Event, FerryBooking, ThemeParkBooking, EventBooking


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'price', 'available_rooms')
    list_filter = ('location',)
    search_fields = ('name', 'location')


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'created_at')
    search_fields = ('username', 'email')


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('booking_reference', 'user', 'hotel', 'check_in_date', 'check_out_date', 'is_confirmed')
    list_filter = ('is_confirmed', 'check_in_date', 'hotel')
    search_fields = ('booking_reference', 'user__username', 'hotel__name')


@admin.register(Ferry)
class FerryAdmin(admin.ModelAdmin):
    list_display = ('name', 'departure_location', 'arrival_location', 'departure_time', 'price')
    list_filter = ('departure_location', 'arrival_location')


@admin.register(ThemeParkTicket)
class ThemeParkTicketAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'valid_from', 'valid_until')
    list_filter = ('valid_from', 'valid_until')


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_date', 'event_time', 'location', 'price')
    list_filter = ('event_date', 'location')


@admin.register(FerryBooking)
class FerryBookingAdmin(admin.ModelAdmin):
    list_display = ('booking', 'ferry', 'departure_date', 'number_of_passengers')
    list_filter = ('departure_date', 'ferry')


@admin.register(ThemeParkBooking)
class ThemeParkBookingAdmin(admin.ModelAdmin):
    list_display = ('booking', 'ticket', 'booking_date', 'number_of_tickets')
    list_filter = ('booking_date', 'ticket')


@admin.register(EventBooking)
class EventBookingAdmin(admin.ModelAdmin):
    list_display = ('booking', 'event', 'booking_date', 'number_of_tickets')
    list_filter = ('booking_date', 'event')