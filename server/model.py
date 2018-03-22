from app import db , app
from sqlalchemy.types import ARRAY as Array
from flask import Flask, jsonify, abort, request
from flask_marshmallow import Marshmallow

ma = Marshmallow( app )

class Location(db.Model):
    __tablename__='location'
    neighborhood    = db.Column(db.String)
    address         = db.Column(db.String)
    city            = db.Column(db.String)
    state           = db.Column(db.String)
    postal_code     = db.Column(db.String)
    latitude        = db.Column(db.Float)
    longtitude      = db.Column(db.Float)

    location_id = db.Column(db.Integer , primary_key=True )
    first_open_date = db.Column(db.DateTime) 
    manager_name = db.Column(db.String)
    phone_number = db.Column(db.String(10))
    hour_open = db.Column( Array( db.String( 7)))
    hour_close = db.Column( Array( db.String( 7)))

    # restaurant id is a foreign key
    business_id  = db.Column(db.String (22), db.ForeignKey('restaurant.business_id'))

    def __init__(self, neighborhood, address, city, state, postal_code, latitude, longtitude, business_id):
        
        self.neighborhood = neighborhood
        self.address = address
        self.city = city
        self.state = state
        self.postal_code = postal_code
        self.latitude = latitude
        self.longtitude = longtitude
        self.business_id = business_id
    
class MenuItem(db.Model):
    __tablename__='menuitem'

    item_id  = db.Column(db.String (22), primary_key=True)
    name = db.Column(db.String) 

    # food or beverage 
    item_type = db.Column(db.String)

    # starter, main, desert 
    category = db.Column(db.String)
    description  = db.Column(db.String)
    price  = db.Column(db.String)

    # restaurant id is a foreign key
    business_id  = db.Column(db.String (22), db.ForeignKey('restaurant.business_id'))

    # M menu item  has N ratings
    ratings = db.relationship('Rating') 


class Rater(db.Model):
    __tablename__='rater'

    #mapper
    user_id = db.Column(db.String (22), primary_key=True)
    email = db.Column(db.String)

    # an alias such as SuperSizeMe
    name = db.Column(db.String)

    # show when this rater first joined the website
    join_date = db.Column(db.DateTime)

    # type of rater (blog, online, food critic)
    rater_type = db.Column(db.String) 

    # takes a value between 1 and 5
    # the value db.Modeld on the number of people who found 
    # this  rater’s opinion helpful, and the default value is 1 (lowest).
    reputation = db.Column(db.Integer) 

    # 1 rater writes N ratings
    ratings = db.relationship('Rating')

    def __init__(self, user_id, name, join_date, reputation):
        self.user_id = user_id
        self.name = name
        self.join_date = join_date
        self.reputation = reputation


class Rating(db.Model):
    __tablename__='rating'

    #mapper
    user_id = db.Column(db.String (22), db.ForeignKey('rater.user_id'))
    business_id  = db.Column(db.String (22), db.ForeignKey('restaurant.business_id'))
    item_id = db.Column(db.String (22), db.ForeignKey('menuitem.item_id'))
    
    date = db.Column(db.DateTime, primary_key=True)
    
    # price, food, mood, staff attributes may 
    # take a value between 1(low) to 5(high)
    price = db.Column(db.Integer)
    food = db.Column(db.Integer)
    mood = db.Column(db.Integer)
    staff= db.Column(db.Integer)


    comments =db.Column(db.String)

    def __init__(self, user_id, business_id, date, comments ):
        self.user_id = user_id
        self.business_id = business_id
        self.date = date
        self.comments = comments

class RatingItem(db.Model):
    __tablename__='ratingitem'

    user_id  = db.Column(db.String (22), primary_key=True)
    date = db.Column(db.DateTime, primary_key=True)
    item_id   = db.Column(db.String (22), primary_key=True)
    rating = db.Column(db.Integer)
    comment = db.Column(db.String)


class Restaurant(db.Model,object):
    __tablename__='restaurant'

    business_id = db.Column(db.String (22), primary_key=True)
    name = db.Column(db.String)

    stars = db.Column(db.Float) 
    review_count = db.Column(db.Integer)

    # 0 for closed, 1 for open
    is_open = db.Column(db.Integer)

    # type  attribute contains details about the cuisine, 
    # such as Italian, Indian, Middle Eastern, and so on.
    food_type = db.Column( Array( db.String))
    hours = db.Column( Array( db.String( 7))) # [ "Mon", "Tue" ... ]

    URL = db.Column(db.String)

    # 1 restaurant has N ratings
    ratings = db.relationship('Rating')

    # 1 restaurant has N locations
    locations = db.relationship('Location')

    # 1 restaurant serves M menu items
    items = db.relationship('MenuItem')

    def __init__(self,b_id,name,review_count,is_open):
        self.business_id=b_id
        self.name=name
        self.review_count=review_count
        self.is_open=is_open
    
class RestaurantSchmea( ma.Schema ):
    class Meta:
        fields = ( 'business_id' , 'name' )

# Formating the right models 
restaurants_schema = RestaurantSchmea( many=True )


