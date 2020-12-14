from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import School,Donation
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.contrib.gis.geos import fromstr
from django.contrib.gis.db.models.functions import Distance
import folium
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

        m=folium.Map(location=[lat,long],zoom_start=12)

        folium.Marker([lat,long],
        popup='',
        tooltip='Your Location!',
        icon=folium.Icon(color='red')).add_to(m),

        if dist=="lt5":
            near = School.objects.annotate(distance=Distance("location", location)/1000).filter(distance__lte=5).order_by("distance")
        elif dist=="lt1":
            near= School.objects.annotate(distance=Distance("location", location)/1000).filter(distance__lte=1).order_by("distance")
        elif dist=="lt10":
            near= School.objects.annotate(distance=Distance("location", location)/1000).filter(distance__lte=10).order_by("distance")
        else:
            near= School.objects.annotate(distance=Distance("location", location)/1000).filter(distance__lte=15).order_by("distance")
        #print(near)

        if len(near)>0:
            for it in near:
                org=it.name.replace(' ','+')
                org_address=it.address.replace(' ','+')
                link="https://www.google.com/maps/dir/?api=1&destination=" + org + "+"+org_address
                dirn.append(link)
                tooltip="Name:"+it.name
                folium.Marker([it.location.y,it.location.x],
                               popup='<a href="' + link + '">GetDirection</a>',
                               tooltip=tooltip).add_to(m)


        m.save('templates/schools/map_near_school.html')




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
        return message(request,"Thank you for submitting your details")

    return render(request,'schools/ngo_form.html',{'details':details})

def map_near_school(request):
    return render(request,'schools/map_near_school.html')

def message(request, message):
    return render(request,'core/message.html',{'message':message})


def donor_form(request):
    donor=''
    org=''
    date=''
    verification=''
    donation=''
    details=False

    if request.method == 'POST' and details==False:
        details=True
        donor = request.POST.get('donor')
        org= request.POST.get('org')
        verification=request.POST.get('verification')
        date=request.POST.get('date')
        donation=request.POST.get('donation')

        d=Donation(donor=donor,org=org,verification=verification,date=date,donation=donation)
        d.save()
        return message(request, 'Thank you for filling your donation details!')

    return render(request,'schools/donor_form.html',{details:details})

def show_donation(request):
    item=[]
    item=Donation.objects.all().order_by('date')
    #print(item)
    return render(request,'schools/show_donation.html',{'item':item})
