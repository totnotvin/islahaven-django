from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Hotel(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image_url = models.URLField(blank=True, null=True)
    rating = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],
        null=True,
        blank=True
    )
    available_rooms = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class User(models.Model):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # In production, use Django's built-in User model
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    number_of_guests = models.IntegerField(validators=[MinValueValidator(1)])
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    booking_date = models.DateTimeField(auto_now_add=True)
    booking_reference = models.CharField(max_length=20, unique=True)
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"Booking {self.booking_reference} - {self.user.username}"


class Ferry(models.Model):
    name = models.CharField(max_length=100)
    departure_location = models.CharField(max_length=100)
    arrival_location = models.CharField(max_length=100)
    departure_time = models.TimeField()
    arrival_time = models.TimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    capacity = models.IntegerField()

    def __str__(self):
        return f"{self.name} ({self.departure_location} to {self.arrival_location})"


class ThemeParkTicket(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    valid_from = models.DateField()
    valid_until = models.DateField()
    max_visitors = models.IntegerField()

    def __str__(self):
        return self.name


class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=100)
    event_date = models.DateField()
    event_time = models.TimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    max_attendees = models.IntegerField()

    def __str__(self):
        return self.title


class FerryBooking(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    ferry = models.ForeignKey(Ferry, on_delete=models.CASCADE)
    departure_date = models.DateField()
    number_of_passengers = models.IntegerField(validators=[MinValueValidator(1)])
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Ferry Booking - {self.booking.booking_reference}"


class ThemeParkBooking(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    ticket = models.ForeignKey(ThemeParkTicket, on_delete=models.CASCADE)
    booking_date = models.DateField()
    number_of_tickets = models.IntegerField(validators=[MinValueValidator(1)])
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Theme Park Booking - {self.booking.booking_reference}"


class EventBooking(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    booking_date = models.DateField()
    number_of_tickets = models.IntegerField(validators=[MinValueValidator(1)])
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Event Booking - {self.booking.booking_reference}"
