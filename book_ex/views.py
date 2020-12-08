from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from core.models import UserProfileInfo
from .models import Book_ex
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.contrib.gis.geos import fromstr
from django.contrib.gis.db.models.functions import Distance
# Create your views here.

def message(request, message):
    return render(request,'core/message.html',{'message':message})

def near_book(request):
    user = request.user
    if user.is_authenticated:
        userNode = UserProfileInfo.nodes.get(username=user.username)
        lat=userNode.latitude
        long=userNode.longitude
        dist=""
        near=[]
        dirn=[]
        location = fromstr(f'POINT({long} {lat})', srid=4326)

        if request.method == 'POST':
            book=request.POST.get('exchange')
            near = Book_ex.objects.annotate(distance=Distance("location", location)/1000).filter(distance__lte=25,book=book).order_by("distance")
            if len(near)>0:
                for it in near:
                    org_address=it.address.replace(' ','+')
                    link="https://www.google.com/maps/dir/?api=1&destination=" +org_address
                    dirn.append(link)
        return render(request,'book_ex/near_book.html',{'near':near, 'dirn':dirn,'zi':zip(near,dirn),'book':book})
    else:
        return message(request, 'Register/Login to use this feature!')



def bookex_form(request):
    name=""
    address=""
    city=""
    lat=0.0
    long=0.0
    book=""
    author=""
    email=""
    contact=""
    details=False

    if request.method == 'POST' and details==False:
        details=True
        name = request.POST.get('name')
        address= request.POST.get('address')
        city= request.POST.get('city')
        lat=request.POST.get('lat')
        long=request.POST.get('long')
        book= request.POST.get('book')
        author=request.POST.get('author')
        email=request.POST.get('email')
        contact=request.POST.get('contact')
        genre=request.POST.get('genre')

        location = fromstr(f'POINT({long} {lat})', srid=4326)

        s=Book_ex(name=name, city=city, address=address, location=location,email=email,contact=contact,book=book,author=author,genre=genre)
        s.save()
        return message(request,'Thank you for submitting your details!')


    return render(request,'book_ex/bookex_form.html',{'details':details})



def genre(request):
    user = request.user
    if user.is_authenticated:
        items=Book_ex.objects.all().distinct('genre')
        userNode = UserProfileInfo.nodes.get(username=user.username)
        lat=userNode.latitude
        long=userNode.longitude
        location = fromstr(f'POINT({long} {lat})', srid=4326)
        item=[]
        dirn=[]
        details=False
        if request.method == 'POST' and details==False:
            details=True
            genre=request.POST.get('genre')
            if genre=="All":
                item=Book_ex.objects.annotate(distance=Distance("location", location)/1000).filter(distance__lte=25).order_by("distance")
            else:
                item=Book_ex.objects.annotate(distance=Distance("location", location)/1000).filter(distance__lte=25,genre=genre).order_by("distance")
            if len(item)>0:
                for it in item:
                    org_address=it.address.replace(' ','+')
                    link="https://www.google.com/maps/dir/?api=1&destination=" +org_address
                    dirn.append(link)
        return render(request,'book_ex/genre.html',{'details':details,'item':item, 'items':items,'dirn':dirn,'zi':zip(item,dirn)})

    else:
        return message(request, 'Register/Login to use this feature!')
