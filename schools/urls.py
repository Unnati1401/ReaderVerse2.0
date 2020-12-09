from django.contrib import admin
from django.urls import path
from schools import views


app_name='schools'

urlpatterns = [
     #path('', views.index, name='index'),
     path('nearby/', views.nearby, name='nearby'),
     path('map_near_school/', views.map_near_school, name='map_near_school'),
     path('ngo_form/', views.ngo_form, name='ngo_form'),
]
