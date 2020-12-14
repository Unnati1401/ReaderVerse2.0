from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from .models import School,Donation

@admin.register(School)
class SchoolAdmin(OSMGeoAdmin):
    list_display = ('name', 'location')

@admin.register(Donation)
class DonationAdmin(OSMGeoAdmin):
    list_display = ('donor', 'org')
# Register your models here.
