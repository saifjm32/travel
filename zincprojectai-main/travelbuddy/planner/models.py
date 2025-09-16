from django.db import models


class TripRequest(models.Model):
    PLAN_FREE = 'FREE'
    PLAN_PAID = 'PAID'
    PLAN_CHOICES = [
        (PLAN_FREE, 'Free'),
        (PLAN_PAID, 'Paid'),
    ]

    plan_type = models.CharField(max_length=8, choices=PLAN_CHOICES)
    origin = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()

    budget_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    budget_currency = models.CharField(max_length=8, null=True, blank=True)
    transport_prefs = models.CharField(max_length=255, blank=True)
    taxi_airport_to_hotel = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.plan_type} trip {self.origin} → {self.destination} ({self.start_date} to {self.end_date})"


class Traveler(models.Model):
    GENDER_MALE = 'Male'
    GENDER_FEMALE = 'Female'
    GENDER_OTHER = 'Other'
    GENDER_CHOICES = [
        (GENDER_MALE, 'Male'),
        (GENDER_FEMALE, 'Female'),
        (GENDER_OTHER, 'Other'),
    ]

    trip = models.ForeignKey(TripRequest, on_delete=models.CASCADE, related_name='travelers')
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=16, choices=GENDER_CHOICES)
    interests = models.TextField(blank=True)
    disabilities_allergies = models.TextField(blank=True)

    def __str__(self) -> str:
        return f"Traveler {self.age} {self.gender}"


class Itinerary(models.Model):
    trip = models.OneToOneField(TripRequest, on_delete=models.CASCADE, related_name='itinerary')
    content = models.JSONField()

    def __str__(self) -> str:
        return f"Itinerary for trip {self.trip_id}"

# Create your models here.
