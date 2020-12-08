from django.contrib import admin
from django.urls import path
from web_scrape import views


app_name='web_scrape'

urlpatterns = [
     #path('', views.index, name='index'),
     
     path('webscrape', views.webscrape, name='webscrape'),
]
