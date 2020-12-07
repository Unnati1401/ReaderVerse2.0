from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import School
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.contrib.gis.geos import fromstr
from django.contrib.gis.db.models.functions import Distance
# Create your views here.
def nearby(request):
    details=False
    lat=0.0
    long=0.0
    dist=""
    near=[]
    dirn=[]
    count=0

    if request.method == 'POST' and details==False:
        details=True
        lat=request.POST.get('lat')
        long=request.POST.get('long')
        location = fromstr(f'POINT({long} {lat})', srid=4326)
        dist=request.POST.get('dist')

        if dist=="lt5":
            near = School.objects.annotate(distance=Distance("location", location)/1000).filter(distance__lte=5).order_by("distance")
        elif dist=="lt10":
            near= School.objects.annotate(distance=Distance("location", location)/1000).filter(distance__lte=10).order_by("distance")
        else:
            near= School.objects.annotate(distance=Distance("location", location)/1000).filter(distance__lte=15).order_by("distance")

        if len(near)>0:
            for it in near:
                org=it.name.replace(' ','+')
                org_address=it.address.replace(' ','+')
                link="https://www.google.com/maps/dir/?api=1&destination=" + org + "+"+org_address
                dirn.append(link)





    return render(request,'schools/nearby_schools.html',{'near':near, 'details':details,'dist':dist,'dirn':dirn,'zi':zip(near,dirn)})

def ngo_form(request):
    name=""
    address=""
    city=""
    lat=0.0
    long=0.0
    details=False

    if request.method == 'POST' and details==False:
        details=True
        name = request.POST.get('name')
        address= request.POST.get('address')
        city= request.POST.get('city')
        lat=request.POST.get('lat')
        long=request.POST.get('long')
        location = fromstr(f'POINT({long} {lat})', srid=4326)

        s=School(name=name, city=city, address=address, location=location)
        s.save()
        return HttpResponse("Thank you for submitting your details")

    return render(request,'schools/ngo_form.html',{'details':details})
