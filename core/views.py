# pylint: disable=no-member
# pylint: disable=not-an-iterable
from django.shortcuts import render
from core.forms import UserForm
from .models import UserProfileInfo, Genre, Book, Author
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from rest_framework.response import Response
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from neomodel import db as neodb
import random

# Create your views here.

#Creates user for a user node
@receiver(post_save, sender=UserProfileInfo, dispatch_uid='create_user_node')
def create_user_node(sender, instance, created, **kwargs):
    if created:
        user = User.objects.create_user(instance.username)
        user.set_password(instance.password)
        user.save()

#Deletes user from db when user node is deleted
@receiver(post_delete, sender=UserProfileInfo, dispatch_uid='delete_user_node')
def delete_user_node(sender, instance, **kwargs):
    User.objects.filter(username=instance.username).delete()

def user_login(request):
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)
        if user:
            if user.is_active:
                login(request,user)
                print("successful")
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("ACCOUNT NOT ACTIVE")
        else:
            print("someone tried to login and failed")
            print("Username:{} and password {}".format(username,password))
            return HttpResponse("invalid login details")
    else:
        return render(request,'core/login.html',{})

@login_required
def user_logout(request):
    logout(request)
    return message(request, 'Logout successful')

def register(request):

    if request.method=='POST':
        userform = UserForm(data=request.POST)
        genresList = request.POST.getlist('genres')
        if userform.is_valid():
            newUser = userform.save(commit=False)
            newUser.latitude = request.POST.get('latitude')
            newUser.longitude = request.POST.get('longitude')
            newUser.save()
            for g in genresList:
                #print(g)
                newUser.favGenres.connect(Genre.nodes.get(name=g))
            return message(request,'Registered successfully! You can login to proceed.')
        else:
            print(userform.errors)
            return message(request,'Error in registering. Please try again.')
    else:

        #createGenreNodes(request)
        user = request.user
        if user.is_authenticated:
            return message(request, 'You are already logged in.')
        else:
            userform = UserForm()
            genreNodes = Genre.nodes
            return render(request,'core/register.html',{'userform':userform,'genreNodes':genreNodes})


def explore(request):
    booksToBePassed = []
    user = request.user
    if user.is_authenticated:
        userNode = UserProfileInfo.nodes.get(username=user.username)
        userGenres = userNode.favGenres.all()
        #adding 5 books from user's genres
        for g in userGenres:
            count = 5
            for b in g.bookGenre.all():
                booksToBePassed.append([b.Title, b.wrote.all(),b.img_url, b.genre.all()])
                count = count - 1
                if count == 0:
                    break
    else:
        #adding 5 books from each genre
        genres = Genre.nodes.all()
        for g in genres:
            count = 5
            for b in g.bookGenre.all():
                booksToBePassed.append([b.Title, b.wrote.all(),b.img_url, b.genre.all()])
                count = count - 1
                if count == 0:
                    break

    return render(request, 'core/explore.html', {'books': booksToBePassed})

def profile(request):
    userNode = UserProfileInfo.nodes.get(username=request.user.username)
    booksToBePassed = []
    for b in userNode.favBooks.all():
        booksToBePassed.append([b.Title, b.wrote.all(), b.genre.all()])
    userGenres = userNode.favGenres.all()
    otherGenres = []
    for g in Genre.nodes.all():
        if g not in userGenres:
            otherGenres.append(g)
    return render(request,'core/profile.html',{'books':booksToBePassed,'userNode':userNode,'userGenres':userGenres,'otherGenres':otherGenres})

def removeFavorites(request):
    userNode = UserProfileInfo.nodes.get(username=request.user.username)

    selectedBooks = request.POST.getlist('selectedBooks')
    for b in selectedBooks:
        neodb.cypher_query("MATCH (user:UserProfileInfo {username:$username})-[rel:FAVORITEBOOK]->(:Book{Title:$Title}) DELETE rel", {"username": userNode.username,"Title":b})

    return profile(request)

def addGenres(request):
    userNode = UserProfileInfo.nodes.get(username=request.user.username)
    addGenresSelected = request.POST.getlist('addGenresSelected')
    for g in addGenresSelected:
        userNode.favGenres.connect(Genre.nodes.get(name=g))
    return profile(request)

def removeGenres(request):
    userNode = UserProfileInfo.nodes.get(username=request.user.username)

    removeGenresSelected = request.POST.getlist('removeGenresSelected')
    for b in removeGenresSelected:
        neodb.cypher_query("MATCH (user:UserProfileInfo {username:$username})-[rel:FAVORITEGENRE]->(:Genre{name:$name}) DELETE rel", {"username": userNode.username,"name":b})

    return profile(request)

# Shows users what other users are reading who have common genres
def collab(request):
    booksToBePassed = []
    user = request.user
    if user.is_authenticated:
        userNode = UserProfileInfo.nodes.get(username=user.username)
        userGenres = userNode.favGenres.all()
        #adding books belonging to common genres vale users
        commonUsers = []
        for g in userGenres:
            for curruser in g.favGenre.all():
                if curruser not in commonUsers and curruser != userNode:
                    commonUsers.append(curruser)
        for u in commonUsers:
            booksList = u.favBooks.all()
            for b in booksList:
                booksToBePassed.append([b.Title, b.wrote.all(), b.img_url, b.genre.all()])
            if len(booksToBePassed) >= 50:
                break

        return render(request, 'core/explore.html', { 'books': booksToBePassed})
    else:
        #adding 5 books from each genre
        genres = Genre.nodes.all()
        for g in genres:
            booksList = g.bookGenre.all()
            random_items = random.sample(booksList, 5)
            for b in random_items:
                booksToBePassed.append([b.Title, b.wrote.all(), b.img_url, b.genre.all()])

    return render(request, 'core/explore.html', { 'books': booksToBePassed })


def genresPage(request):

    genres = Genre.nodes
    if request.method == "POST":
        booksToBePassed = {}
        genresList = request.POST.getlist('genres')
        #adding 50 random books belonging to each selected genres
        for g in genresList:
            genreNode = Genre.nodes.get(name=g)
            books = []
            booksList = genreNode.bookGenre.all()
            random_items = random.sample(booksList, 50)
            for b in random_items:
                books.append([b.Title, b.wrote.all(), b.img_url, b.genre.all()])
            booksToBePassed[str(genreNode.name)] = books

        return render(request, 'core/genresPage.html', {'books': booksToBePassed, 'genreNodes': genres})

    else:
        return render(request, 'core/genresPage.html', {'genreNodes': genres})


def authorsPage(request):
    authors = Author.nodes
    authorNodes = sorted(authors, key=lambda x: x.name)
    random_authors = random.sample(authorNodes, 50)
    if request.method == "POST":
        booksToBePassed = []
        authorSelected = request.POST.get('authorSelected')
        #adding 20 books belonging to selected author
        #random_items = random.sample(booksList, 50)
        booksList = Author.nodes.get(name=authorSelected).wrote.all()
        for b in booksList:
            booksToBePassed.append([b.Title, b.wrote.all(), b.img_url, b.genre.all()])
        return render(request, 'core/authorsPage.html', {'books': booksToBePassed, 'authorNodes': random_authors})

    else:
        return render(request, 'core/authorsPage.html', {'authorNodes': random_authors})

def message(request, message):
    return render(request,'core/message.html',{'message':message})

def gettingStarted(request):
    return render(request, 'core/gettingStarted.html')

def addRatings(request):
    if request.user.is_authenticated == False:
        return register(request)

    else:
        userNode = UserProfileInfo.nodes.get(username=request.user.username)

        if request.method=="GET":
            booksToBePassed = {}
            userGenres = userNode.favGenres
            for g in userGenres:
                books = []
                booksList = g.bookGenre.all()
                booksList = sorted(booksList, key=lambda x: x.id)
                random_items = random.sample(booksList, 50)
                for b in random_items:
                    if userNode not in b.user.all():
                        books.append([b.Title, b.wrote.all(), b.img_url, b.genre.all()])
                booksToBePassed[str(g.name)] = books

            return render(request, 'core/addRatings.html', {'booksToBePassed': booksToBePassed})

        else:
            selectedBooks = request.POST.getlist('selectedBooks')
            print(selectedBooks)
            # for b in favBooksList:
            #     userNode.favBooks.connect(Book.nodes.get(Title=b))
            return message(request,'Books added to favorites')

# Displays random 50 books from each of user's genres and adding selected books as user's favorite ones
def addFavorites(request):
    if request.user.is_authenticated == False:
        return register(request)

    else:
        userNode = UserProfileInfo.nodes.get(username=request.user.username)

        if request.method=="GET":
            booksToBePassed = {}
            userGenres = userNode.favGenres
            for g in userGenres:
                books = []
                booksList = g.bookGenre.all()
                booksList = sorted(booksList, key=lambda x: x.id)
                random_items = random.sample(booksList, 50)
                for b in random_items:
                    if userNode not in b.user.all():
                        books.append([b.Title, b.wrote.all(), b.img_url, b.genre.all()])
                booksToBePassed[str(g.name)] = books

            return render(request, 'core/addFavorites.html', {'booksToBePassed': booksToBePassed})

        else:
            favBooksList = request.POST.getlist('selectedBooks')
            for b in favBooksList:
                userNode.favBooks.connect(Book.nodes.get(Title=b))
            return message(request,'Books added to favorites')

#Creates genre nodes. Call each time before adding the first user.
def createGenreNodes(request):
    genre = Genre(genre_id=0,name="Arts & Photography")
    genre.save()
    genre = Genre(genre_id = 1,name="Biographies & Memoirs")
    genre.save()
    genre = Genre(genre_id = 2,name="Business & Money")
    genre.save()
    genre = Genre(genre_id = 3,name="Calendars")
    genre.save()
    genre = Genre(genre_id = 4,name="Children's Books")
    genre.save()
    genre = Genre(genre_id = 5,name="Comics & Graphic Novels")
    genre.save()
    genre = Genre(genre_id = 6,name="Computers & Technology")
    genre.save()
    genre = Genre(genre_id = 7,name="Cookbooks, Food & Wine")
    genre.save()
    genre = Genre(genre_id = 8,name="Crafts, Hobbies & Home")
    genre.save()
    genre = Genre(genre_id = 9,name="Christian Books & Bibles")
    genre.save()
    genre = Genre(genre_id = 10,name="Engineering & Transportationry")
    genre.save()
    genre = Genre(genre_id = 11,name="Health, Fitness & Dieting")
    genre.save()
    genre = Genre(genre_id = 12,name="History")
    genre.save()
    genre = Genre(genre_id = 13,name="Humor & Entertainment")
    genre.save()
    genre = Genre(genre_id = 14,name="Law")
    genre.save()
    genre = Genre(genre_id = 15,name="Literature & Fiction")
    genre.save()
    genre = Genre(genre_id = 16,name="Medical Books")
    genre.save()
    genre = Genre(genre_id = 17,name="Mystery, Thriller & Suspense")
    genre.save()
    genre = Genre(genre_id = 18,name="Parenting & Relationships")
    genre.save()
    genre = Genre(genre_id = 19,name="Politics & Social Sciences")
    genre.save()
    genre = Genre(genre_id = 20,name="Reference")
    genre.save()
    genre = Genre(genre_id = 21,name="Religion & Spirituality")
    genre.save()
    genre = Genre(genre_id = 22,name="Romance")
    genre.save()
    genre = Genre(genre_id = 23,name="Science & Math")
    genre.save()
    genre = Genre(genre_id = 24,name="Science Fiction & Fantasy")
    genre.save()
    genre = Genre(genre_id = 25,name="Self-Help")
    genre.save()
    genre = Genre(genre_id = 26,name="Sports & Outdoors")
    genre.save()
    genre = Genre(genre_id = 27,name="Teen & Young Adult")
    genre.save()
    genre = Genre(genre_id = 28,name="Test Preparation")
    genre.save()
    genre = Genre(genre_id = 29,name="Travel")
    genre.save()
    genre = Genre(genre_id = 30,name="Gay & Lesbian")
    genre.save()
    genre = Genre(genre_id = 31,name="Education & Teaching")
    genre.save()


def index(request):
    return render(request,'core/index.html')

def aboutus(request):
    return render(request,'core/aboutus.html')

def contactus(request):
    return render(request,'core/contactus.html')
