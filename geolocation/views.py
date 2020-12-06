from django.shortcuts import render
from .models import RestaurantModel
from django.views.generic import ListView
from geopy.geocoders import Nominatim
import folium
from .forms import RestaurantModelForm
from django.contrib.gis.geoip2 import GeoIP2
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from geopy.distance import geodesic


# Create your views here.

def get_user_ip(ip):
    g = GeoIP2()
    lat, lon = g.lat_lon(ip)
    return lat, lon


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class Restaurant(ListView):
    template_name = 'restaurant_list.html'
    query_set = RestaurantModel.objects.defer('address', 'city', 'location')
    paginate_by = 12
    model = RestaurantModel
    context_object_name = "restaurants"


def restaurant_detail(request, **kwargs):
    product = kwargs['restaurant_id']
    restaurant = RestaurantModel.objects.get(id=product)
    geolocator = Nominatim(user_agent="geolocation")
    location = geolocator.reverse(f'{restaurant.latitude}, {restaurant.longitude}')
    r_location = (restaurant.latitude, restaurant.longitude)
    address = location.address
    m = folium.Map(width=800, height=400, location=r_location, zoom_start=13)
    folium.Circle(location=r_location, color='red', fill=True, weight=0,
                  radius=restaurant.service).add_to(m)
    folium.Marker(icon=folium.Icon(color='red'), location=r_location, tooltip='click',
                  popup=f"{restaurant.name}").add_to(m)
    m = m._repr_html_()
    context = {
        "restaurant": restaurant,
        'map': m,
        'address': address
    }
    return render(request, 'restaurant_detail.html', context)


def show_nearby_restaurant(request):
    form = RestaurantModelForm(request.POST or None)
    geolocator = Nominatim(user_agent="geolocation")
    ip = '178.169.27.223'  # change content with get_client_ip(request) in deploying stage.
    l_lat, l_lon = get_user_ip(ip)
    user_location = (l_lat, l_lon)
    point = Point(l_lat, l_lon, srid=4326)
    m = folium.Map(width=800, height=400, zoom_start=12, location=user_location, no_touch=False)
    folium.Marker(location=user_location, tooltip='Click', popup='Your Position', icon=folium.Icon(color='red')).add_to(
        m)
    nearby_restaurant = RestaurantModel.objects.all()
    for res in nearby_restaurant:
        distance = int(geodesic((res.latitude, res.longitude), user_location).meters)
        if res.service >= distance:
            folium.Circle(location=(res.latitude, res.longitude), color='red', fill=True, weight=0,
                          radius=res.service, popup=res.name).add_to(m)
    if form.is_valid():
        form_location = form.cleaned_data.get('location')
        user_location = geolocator.geocode(form_location)
        lat, lon = user_location.latitude, user_location.longitude
        lat_lon = (lat, lon)
        m = folium.Map(width=800, height=400, zoom_start=10, location=lat_lon)
        folium.ClickForMarker().add_to(m)
    m = m._repr_html_()
    context = {
        'form': form,
        'map': m
    }
    return render(request, 'nearby_restaurant.html', context)
