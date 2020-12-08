from django.contrib.gis.db import models

class Book_ex(models.Model):
    name = models.CharField(max_length=100)
    location = models.PointField()
    address = models.CharField(max_length=150)
    city = models.CharField(max_length=50)
    book= models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    email= models.EmailField(max_length = 254)
    contact= models.CharField(max_length=20)
    genre= models.CharField(max_length=120)



# Create your models here.
