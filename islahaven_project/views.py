from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from booking_app.models import Hotel, Booking, Ferry, ThemeParkTicket, Event, User, FerryBooking, ThemeParkBooking, EventBooking
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from django.utils import timezone


def index(request):
    # Get featured content for the home page
    featured_hotels = Hotel.objects.all()[:3]
    featured_tickets = ThemeParkTicket.objects.all()[:3]
    featured_events = Event.objects.all().order_by('event_date')[:3]
    
    context = {
        'featured_hotels': featured_hotels,
        'featured_tickets': featured_tickets,
        'featured_events': featured_events
    }
    return render(request, 'index.html', context)


def rooms(request):
    hotels = Hotel.objects.all()
    context = {'hotels': hotels}
    return render(request, 'rooms.html', context)


def ferry(request):
    ferries = Ferry.objects.all()
    context = {'ferries': ferries}
    return render(request, 'ferry.html', context)


def tickets(request):
    # Get bookings with related ferry and park bookings
    # For demo purposes, using all bookings
    bookings = Booking.objects.prefetch_related('ferrybooking_set', 'themeparkbooking_set').all()
    context = {'bookings': bookings}
    return render(request, 'tickets.html', context)


def events(request):
    events = Event.objects.all().order_by('event_date')
    context = {'events': events}
    return render(request, 'events.html', context)


def login(request):
    return render(request, 'login.html')


def booking_view(request):
    bookings = Booking.objects.prefetch_related(
        'ferrybooking_set',
        'eventbooking_set',
        'themeparkbooking_set',
        'hotel',
        'user'
    ).all()
    context = {'bookings': bookings}
    return render(request, 'booking-view.html', context)


def booking_detail(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    context = {
        'booking': booking
    }
    return render(request, 'booking_detail.html', context)


def dashboard(request):
    # Get all bookings
    bookings = Booking.objects.select_related('hotel').all()
    upcoming_stays_count = bookings.filter(check_in_date__gte=timezone.now().date()).count()
    
    # Get data for dashboard stats
    ferry_rides_count = FerryBooking.objects.count()
    events_count = EventBooking.objects.count()
    
    # Get upcoming items
    upcoming_hotels = bookings.filter(check_in_date__gte=timezone.now().date()).order_by('check_in_date')[:5]
    upcoming_ferry = FerryBooking.objects.select_related('ferry', 'booking__user').filter(
        departure_date__gte=timezone.now().date()
    ).order_by('departure_date')[:5]
    upcoming_events = EventBooking.objects.select_related('event', 'booking__user').filter(
        event__event_date__gte=timezone.now().date()
    ).order_by('event__event_date')[:5]
    
    # Get recent activity
    recent_bookings = bookings.order_by('-booking_date')[:3]
    recent_ferry = FerryBooking.objects.select_related('ferry', 'booking__user').order_by('-id')[:3]
    recent_events = EventBooking.objects.select_related('event', 'booking__user').order_by('-id')[:3]
    
    context = {
        'upcoming_stays_count': upcoming_stays_count,
        'ferry_rides_count': ferry_rides_count,
        'events_count': events_count,
        'upcoming_hotels': upcoming_hotels,
        'upcoming_ferry': upcoming_ferry,
        'upcoming_events': upcoming_events,
        'recent_bookings': recent_bookings,
        'recent_ferry': recent_ferry,
        'recent_events': recent_events,
    }
    return render(request, 'dashboard.html', context)


def book_ferry(request):
    if request.method == 'POST':
        booking_id = request.POST.get('booking_id')
        ferry_id = request.POST.get('ferry_id')
        departure_date = request.POST.get('departure_date')
        number_of_passengers = request.POST.get('number_of_passengers', 1)
        
        try:
            booking = Booking.objects.get(id=booking_id)
            ferry = Ferry.objects.get(id=ferry_id)
            
            # Calculate total price
            total_price = ferry.price * int(number_of_passengers)
            
            # Create ferry booking
            ferry_booking = FerryBooking.objects.create(
                booking=booking,
                ferry=ferry,
                departure_date=departure_date,
                number_of_passengers=number_of_passengers,
                total_price=total_price
            )
            
            messages.success(request, 'Ferry ticket booked successfully!')
            return redirect('booking-view')
        except (Booking.DoesNotExist, Ferry.DoesNotExist):
            messages.error(request, 'Invalid booking or ferry selected.')
            return redirect('ferry')
    
    # GET request - show booking form
    ferries = Ferry.objects.all()
    confirmed_bookings = Booking.objects.filter(is_confirmed=True)  # Show only confirmed hotel bookings
    
    context = {
        'ferries': ferries,
        'confirmed_bookings': confirmed_bookings
    }
    return render(request, 'book_ferry.html', context)