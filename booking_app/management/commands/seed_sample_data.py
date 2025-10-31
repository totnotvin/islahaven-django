from django.core.management.base import BaseCommand
from booking_app.models import Hotel, Ferry, ThemeParkTicket, Event, User, Booking
from django.utils import timezone
from datetime import datetime, timedelta, time
import random


class Command(BaseCommand):
    help = 'Seeds the database with sample data'

    def handle(self, *args, **options):
        # Create sample hotels
        hotels_data = [
            {
                'name': 'Ocean Pearl Resort',
                'location': 'Main Island',
                'price': 120.00,
                'description': 'King bed, sea view, includes breakfast.',
                'image_url': 'https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=1200&q=60',
                'rating': 4.5,
                'available_rooms': 10
            },
            {
                'name': 'Coral Reef Suites',
                'location': 'South Island',
                'price': 200.00,
                'description': 'Private balcony, king bed, premium amenities.',
                'image_url': 'https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?auto=format&fit=crop&w=1200&q=60',
                'rating': 4.8,
                'available_rooms': 5
            },
            {
                'name': 'Lagoon Breeze Inn',
                'location': 'North Island',
                'price': 80.00,
                'description': 'Budget-friendly option near the market.',
                'image_url': 'https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=1200&q=60',
                'rating': 4.0,
                'available_rooms': 15
            }
        ]
        
        for hotel_data in hotels_data:
            hotel, created = Hotel.objects.get_or_create(
                name=hotel_data['name'],
                defaults=hotel_data
            )
            if created:
                self.stdout.write(f'Created hotel: {hotel.name}')
            else:
                self.stdout.write(f'Hotel already exists: {hotel.name}')

        # Create sample ferries
        ferries_data = [
            {
                'name': 'Morning Express',
                'departure_location': 'Main Island',
                'arrival_location': 'Theme Park Island',
                'departure_time': time(7, 0),  # Using time object directly
                'arrival_time': time(7, 20),
                'price': 10.00,
                'capacity': 50
            },
            {
                'name': 'Midday Shuttle',
                'departure_location': 'Main Island',
                'arrival_location': 'Theme Park Island',
                'departure_time': time(10, 0),
                'arrival_time': time(10, 20),
                'price': 12.00,
                'capacity': 50
            },
            {
                'name': 'Evening Return',
                'departure_location': 'Theme Park Island',
                'arrival_location': 'Main Island',
                'departure_time': time(16, 0),
                'arrival_time': time(16, 20),
                'price': 10.00,
                'capacity': 50
            }
        ]
        
        for ferry_data in ferries_data:
            ferry, created = Ferry.objects.get_or_create(
                name=ferry_data['name'],
                departure_location=ferry_data['departure_location'],
                arrival_location=ferry_data['arrival_location'],
                departure_time=ferry_data['departure_time'],
                arrival_time=ferry_data['arrival_time'],
                defaults=ferry_data
            )
            if created:
                self.stdout.write(f'Created ferry: {ferry.name}')
            else:
                self.stdout.write(f'Ferry already exists: {ferry.name}')

        # Create sample theme park tickets
        tickets_data = [
            {
                'name': 'Space Coaster — FastPass',
                'description': 'Skip the lines with a FastPass add-on for the Space Exploration Coaster.',
                'price': 15.00,
                'valid_from': timezone.now().date(),
                'valid_until': timezone.now().date() + timedelta(days=365),
                'max_visitors': 100
            },
            {
                'name': 'Coral Reef Suites — 20% Off',
                'description': 'Limited time: stay 3 nights get breakfast included. Use code: ISLA20',
                'price': 25.00,
                'valid_from': timezone.now().date(),
                'valid_until': timezone.now().date() + timedelta(days=30),
                'max_visitors': 200
            }
        ]
        
        for ticket_data in tickets_data:
            ticket, created = ThemeParkTicket.objects.get_or_create(
                name=ticket_data['name'],
                defaults=ticket_data
            )
            if created:
                self.stdout.write(f'Created ticket: {ticket.name}')
            else:
                self.stdout.write(f'Ticket already exists: {ticket.name}')

        # Create sample events
        events_data = [
            {
                'title': 'Jet Ski Challenge',
                'description': 'Race course, prizes for top speeds. Limited slots.',
                'location': 'Main Beach',
                'event_date': timezone.now().date() + timedelta(days=7),
                'event_time': time(14, 0),  # Using time object directly
                'price': 30.00,
                'max_attendees': 20
            },
            {
                'title': 'Sunset Volleyball',
                'description': 'Team-based tournament at golden hour.',
                'location': 'Sunset Bay',
                'event_date': timezone.now().date() + timedelta(days=2),
                'event_time': time(17, 30),
                'price': 10.00,
                'max_attendees': 50
            },
            {
                'title': 'Island Music Fest',
                'description': 'Live bands, food stalls, and late-night vibes.',
                'location': 'Central Park',
                'event_date': timezone.now().date() + timedelta(days=14),
                'event_time': time(19, 0),
                'price': 25.00,
                'max_attendees': 200
            }
        ]
        
        for event_data in events_data:
            event, created = Event.objects.get_or_create(
                title=event_data['title'],
                event_date=event_data['event_date'],
                defaults=event_data
            )
            if created:
                self.stdout.write(f'Created event: {event.title}')
            else:
                self.stdout.write(f'Event already exists: {event.title}')

        # Create a sample user if one doesn't exist
        user, created = User.objects.get_or_create(
            username='demo_user',
            defaults={
                'email': 'demo@example.com',
                'password': 'demopassword123',  # In production, use proper password hashing
                'first_name': 'Demo',
                'last_name': 'User',
                'phone_number': '+960123456789'
            }
        )
        if created:
            self.stdout.write(f'Created user: {user.username}')
        else:
            self.stdout.write(f'User already exists: {user.username}')

        # Create a sample booking if one doesn't exist
        if not Booking.objects.filter(user=user).exists():
            sample_hotel = Hotel.objects.first()
            booking = Booking.objects.create(
                user=user,
                hotel=sample_hotel,
                check_in_date=timezone.now().date() + timedelta(days=10),
                check_out_date=timezone.now().date() + timedelta(days=13),
                number_of_guests=2,
                total_price=float(sample_hotel.price) * 3,  # 3 nights
                booking_reference='ISLA-2025-001',
                is_confirmed=True
            )
            self.stdout.write(f'Created booking: {booking.booking_reference}')
        else:
            self.stdout.write('Sample booking already exists')

        self.stdout.write(
            self.style.SUCCESS('Successfully seeded the database with sample data')
        )