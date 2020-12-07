from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from .models import School

@admin.register(School)
class SchoolAdmin(OSMGeoAdmin):
    list_display = ('name', 'location')
# Register your models here.
