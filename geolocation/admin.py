from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from .models import RestaurantModel


# Register your models here.

@admin.register(RestaurantModel)
class RestaurantAdmin(OSMGeoAdmin):
    list_display = ['name', 'location']
