from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from .models import Book_ex

@admin.register(Book_ex)
class Book_exAdmin(OSMGeoAdmin):
    list_display = ('name', 'location')
# Register your models here.
