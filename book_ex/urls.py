from django.contrib import admin
from django.urls import path
from book_ex import views


app_name='book_ex'

urlpatterns = [
     #path('', views.index, name='index'),
     path('near_book/', views.near_book, name='near_book'),
     path('map_near_book/', views.map_near_book, name='map_near_book'),
     path('bookex_form/', views.bookex_form, name='bookex_form'),
     path('genre/', views.genre, name='genre'),
]
