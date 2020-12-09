from django.db import models
from django_neomodel import DjangoNode
from neomodel import StructuredNode, RelationshipTo, RelationshipFrom, Relationship, StructuredRel
from neomodel.properties import EmailProperty, DateProperty, StringProperty, FloatProperty, IntegerProperty
from neomodel.cardinality import OneOrMore, One, ZeroOrMore

class RatingRel(StructuredRel):
    rating = FloatProperty()
    
class UserProfileInfo(DjangoNode):
    first_name = StringProperty(max_length=30,required = True)
    last_name = StringProperty(max_length=150, required = True)
    email = EmailProperty(unique=True,required = True)
    username = StringProperty(max_length=150, unique=True, required = True)
    password = StringProperty(max_length=10,unique=True, required = True)
    address = StringProperty(max_length=200)
    pincode = StringProperty(max_length=6)
    phone = StringProperty(max_length=10, required = True)
    latitude = FloatProperty()
    longitude = FloatProperty()
    favGenres = RelationshipTo('Genre', 'FAVORITEGENRE', cardinality=ZeroOrMore)
    favBooks = RelationshipTo('Book', 'FAVORITEBOOK', cardinality=ZeroOrMore)
    bookRating = RelationshipTo('Book', 'RATING', model = RatingRel, cardinality=ZeroOrMore)
    class Meta:
        app_label = 'core'

class Book(DjangoNode):
    Title = StringProperty()
    img_url = StringProperty()
    user = RelationshipFrom('UserProfileInfo','FAVORITEBOOK',cardinality=ZeroOrMore)
    wrote = RelationshipFrom('Author','WROTE',cardinality=OneOrMore)
    genre = RelationshipFrom('Genre', 'GENRE', cardinality=OneOrMore)
    bookRating = RelationshipFrom('Book', 'RATING', model = RatingRel, cardinality=ZeroOrMore)

class Author(DjangoNode):
    name = StringProperty()
    wrote = RelationshipTo('Book','WROTE',cardinality=ZeroOrMore)

class Genre(DjangoNode):
    name = StringProperty()
    genre_id = IntegerProperty()
    bookGenre = RelationshipTo('Book','GENRE',cardinality=ZeroOrMore)
    favGenre = RelationshipFrom('UserProfileInfo','FAVORITEGENRE',cardinality=ZeroOrMore)

class SeekDonation(DjangoNode):
    relSeek= RelationshipTo('Institute','SEEKFROM',cardinality=ZeroOrMore)


class Institute(DjangoNode):
    #print("in institute")
    name=StringProperty(max_length=100,required = True)
    email=EmailProperty(unique=True,required = True)
    contact=StringProperty(max_length=10, required = True)
    address = StringProperty(max_length=200)
    select = StringProperty(max_length=12, required = True)
    Date = StringProperty(required = True)

    seek = RelationshipFrom('SeekDonation', 'SEEKFROM', cardinality=ZeroOrMore)

    class Meta:
        app_label = 'core'
