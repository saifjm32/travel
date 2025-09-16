from django.urls import path
from . import views


app_name = 'planner'

urlpatterns = [
    path('', views.home, name='home'),
    path('choose-plan/', views.choose_plan, name='choose_plan'),
    path('plan/free/', views.free_plan, name='free_plan'),
    path('plan/paid/', views.paid_plan, name='paid_plan'),
    path('plan/<int:trip_id>/itinerary/', views.itinerary_detail, name='itinerary_detail'),
]


