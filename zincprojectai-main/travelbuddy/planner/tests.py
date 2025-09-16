from django.test import TestCase, Client
from django.urls import reverse
from datetime import date
from .models import TripRequest, Itinerary, Traveler


class PlannerSmokeTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_get_pages(self):
        for url in [
            reverse('planner:home'),
            reverse('planner:choose_plan'),
            reverse('planner:free_plan'),
            reverse('planner:paid_plan'),
        ]:
            resp = self.client.get(url)
            self.assertEqual(resp.status_code, 200)

    def test_post_free_creates_trip_and_itinerary(self):
        resp = self.client.post(reverse('planner:free_plan'), data={
            'origin': 'Amman', 'destination': 'Paris',
            'start_date': '2025-10-01', 'end_date': '2025-10-03',
        })
        self.assertEqual(resp.status_code, 302)
        trip = TripRequest.objects.latest('id')
        self.assertEqual(trip.plan_type, 'FREE')
        self.assertTrue(Itinerary.objects.filter(trip=trip).exists())

    def test_post_paid_creates_trip_travelers_itinerary(self):
        data = {
            'origin': 'Amman', 'destination': 'Rome',
            'start_date': '2025-10-01', 'end_date': '2025-10-02',
            'budget_amount': '1000.00', 'budget_currency': 'USD',
            'transport_prefs': ['Walk', 'Public transit'],
            'taxi_airport_to_hotel': 'on',
            'trav-TOTAL_FORMS': '2', 'trav-INITIAL_FORMS': '0', 'trav-MIN_NUM_FORMS': '0', 'trav-MAX_NUM_FORMS': '1000',
            'trav-0-age': '30', 'trav-0-gender': 'Male', 'trav-0-interests': 'Food', 'trav-0-disabilities_allergies': '',
            'trav-1-age': '28', 'trav-1-gender': 'Female', 'trav-1-interests': 'Art', 'trav-1-disabilities_allergies': '',
        }
        resp = self.client.post(reverse('planner:paid_plan'), data=data)
        self.assertEqual(resp.status_code, 302)
        trip = TripRequest.objects.latest('id')
        self.assertEqual(trip.plan_type, 'PAID')
        self.assertEqual(trip.travelers.count(), 2)
        self.assertTrue(Itinerary.objects.filter(trip=trip).exists())


# Create your tests here.
