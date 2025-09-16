from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from .forms import FreePlanForm, PaidPlanForm, TravelerFormSet
from .models import TripRequest, Itinerary
from .services.ai import generate_itinerary


def home(request):
    return render(request, 'planner/home.html')


def choose_plan(request):
    return render(request, 'planner/choose_plan.html')


@require_http_methods(["GET", "POST"])
def free_plan(request):
    if request.method == 'POST':
        form = FreePlanForm(request.POST)
        if form.is_valid():
            trip: TripRequest = form.save(commit=False)
            trip.plan_type = TripRequest.PLAN_FREE
            trip.save()
            content = generate_itinerary(trip)
            Itinerary.objects.update_or_create(trip=trip, defaults={'content': content})
            return redirect('planner:itinerary_detail', trip_id=trip.id)
    else:
        form = FreePlanForm()
    return render(request, 'planner/free_plan.html', {'form': form})


@require_http_methods(["GET", "POST"])
def paid_plan(request):
    if request.method == 'POST':
        form = PaidPlanForm(request.POST)
        dummy_trip = TripRequest(plan_type=TripRequest.PLAN_PAID)  # for formset binding
        formset = TravelerFormSet(request.POST, instance=dummy_trip, prefix='trav')
        if form.is_valid() and formset.is_valid():
            trip: TripRequest = form.save(commit=False)
            trip.plan_type = TripRequest.PLAN_PAID
            trip.save()
            # save travelers against real trip
            formset.instance = trip
            formset.save()
            content = generate_itinerary(trip)
            Itinerary.objects.update_or_create(trip=trip, defaults={'content': content})
            return redirect('planner:itinerary_detail', trip_id=trip.id)
    else:
        form = PaidPlanForm()
        formset = TravelerFormSet(instance=TripRequest(plan_type=TripRequest.PLAN_PAID), prefix='trav')
    return render(request, 'planner/paid_plan.html', {'form': form, 'formset': formset})


@require_http_methods(["GET", "POST"])
def itinerary_detail(request, trip_id: int):
    trip = get_object_or_404(TripRequest, pk=trip_id)
    itinerary, _ = Itinerary.objects.get_or_create(trip=trip, defaults={'content': generate_itinerary(trip)})
    if request.method == 'POST':
        # Regenerate
        itinerary.content = generate_itinerary(trip)
        itinerary.save()
        return redirect('planner:itinerary_detail', trip_id=trip.id)
    return render(request, 'planner/itinerary_detail.html', {'trip': trip, 'itinerary': itinerary.content})


# Create your views here.
