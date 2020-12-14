from django.contrib.gis.db import models

class School(models.Model):
    name = models.CharField(max_length=100)
    location = models.PointField()
    address = models.CharField(max_length=150)
    city = models.CharField(max_length=50)

class Donation(models.Model):
    donor= models.CharField(max_length=100)
    org=models.CharField(max_length=100)
    donation=models.CharField(max_length=100)
    date=models.DateField()
    verification=models.CharField(max_length=15)


# Create your models here.
