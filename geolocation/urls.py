from django.urls import path
from geolocation.views import Restaurant, restaurant_detail, show_nearby_restaurant

urlpatterns = [
    path('', Restaurant.as_view()),
    path('<restaurant_id>/<name>', restaurant_detail),
    path('nearby', show_nearby_restaurant)
]
