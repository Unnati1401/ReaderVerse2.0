from django.conf.urls import url
from core import views

app_name = 'core'

urlpatterns = [
    url(r'^register/$', views.register, name='register'),
    url(r'^user_login/$', views.user_login, name='user_login'),
    url(r'^user_logout/$', views.user_logout, name='user_logout'),
    url(r'^aboutus/$', views.aboutus, name='aboutus'),
    url(r'^contactus/$', views.contactus, name='contactus'),
    url(r'^explore/$', views.explore, name='explore'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^collab/$', views.collab, name='collab'),
    url(r'^genresPage/$', views.genresPage, name='genresPage'),
    url(r'^authorsPage/$', views.authorsPage, name='authorsPage'),
    url(r'^message/$', views.message, name='message'),
    url(r'^gettingStarted/$', views.gettingStarted, name='gettingStarted'),
    url(r'^addRatings/$', views.addRatings, name='addRatings'),
    url(r'^addFavorites/$', views.addFavorites, name='addFavorites'),
    url(r'^addGenres/$', views.addGenres, name='addGenres'),
    url(r'^removeFavorites/$', views.removeFavorites, name='removeFavorites'),
    url(r'^removeGenres/$', views.removeGenres, name='removeGenres')
]
