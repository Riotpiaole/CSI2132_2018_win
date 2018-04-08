from flask import Flask, jsonify, request, render_template, redirect, url_for
from flask_restless import APIManager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func 
from sqlalchemy import desc

import os 
from model import *

# random string generator
import random  
import string
def random_generator( size=10 ,chars = string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size) )


template_dir = os.path.abspath( "../template/" )
static_dir = os.path.abspath( "../static/" )

app = Flask( "Server" , template_folder = template_dir , static_folder = static_dir)
# Connecting to the database
app.config.from_pyfile ( 'config.py' )
db = SQLAlchemy( app ) # database object


############################ SHOW BLABLA IN JSON ################ 

# Show restaurants in JSON 
@app.route( "/restaurants/JSON" )
def restaurantsJSON():
    restaurants = Restaurant.query.limit(10).all()
    restaurants = restaurants_schema.dump( restaurants )
    return jsonify( restaurants.data )
    
# Show locations in JSON
@app.route( "/locations/JSON" )
def locationsJSON():
    locations = Location.query.limit(10).all()
    locations = locations_schema.dump( locations )
    return jsonify( locations.data )

# Show raters in JSON
@app.route( "/raters/JSON" )
def ratersJSON():
    raters = Rater.query.limit(10).all()
    raters = raters_schema.dump( raters )
    return jsonify( raters.data )

# Show ratings in JSON
@app.route( "/ratings/JSON" )
def ratingsJSON():
    ratings = Rating.query.limit(10).all()
    ratings = ratings_schema.dump( ratings )
    return jsonify( ratings.data )



######### Create Read Update Delete ###########################

######### RESTAURANT ######### 

# show all restaurants
@app.route('/')
@app.route('/restaurant/')
def showRestaurants():
    restaurants = db.session.query(Restaurant).limit(12).all()
    for rest in restaurants:
        rest.location= Location.query.filter(
            Location.business_id == rest.business_id).first()
    cates = db.session.query(Restaurant.food_type.distinct().label("food_type"))
    all_cate = [ row.food_type for row in cates.all()]
    os.system("clear")
    filters = list ( set([ y for x in all_cate for y in x ] ))
    random.shuffle( filters )
    return render_template('restaurants.html', restaurants = restaurants ,
                                               categories=filters[:10],
                                               cated=True)

@app.route('/restaurant/<catergories>')
def cateRestaurants(catergories):
    restaurant_ = Restaurant.query.filter(
        Restaurant.food_type.any(catergories)).all()
    
    # cated as false for skipping the category display
    return render_template('restaurants.html' , restaurants = restaurant_ , 
                                                catergories=catergories ,
                                                cated = False )

# create a new restaurant
@app.route('/restaurant/new/', methods=['GET','POST'])
def newRestaurant():
    if request.method == 'POST':
        location= Location( address = request.form['address'],
                            city = request.form['city'],
                            state = request.form['state'],
                            postal_code=request.form['post_code'])
        newRestaurant = Restaurant(name=request.form['name'],
                                    b_id=random_generator(),
                                    review_count=0,
                                    is_open = 0,
                                    stars=0,
                                    food_type=request.form['food_type'],
                                    location=location)
        db.session.add( location )
        db.session.add(newRestaurant)
        db.session.commit()
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('newRestaurant.html')

# update a restaurant
@app.route('/restaurant/<string:business_id>/edit/',methods=['GET','POST'])
def editRestaurant(business_id):
    editedRestaurant = db.session.query(
        Restaurant).filter_by(business_id=business_id).one()
    if request.method == 'POST':
            if request.form['name']:
                editedRestaurant.name = request.form['name']
                return redirect(url_for('showRestaurants'))
    else:
            return render_template(
                'editRestaurant.html', restaurant = editedRestaurant)
    

# Delete the restaurant
@app.route('/restaurant/<string:business_id>/delete/', methods=['GET', 'POST'])
def deleteRestaurant(business_id):
    restaurantToDelete = db.session.query(
        Restaurant).filter_by(business_id=business_id).one()
    if request.method == 'POST':
        db.session.delete(restaurantToDelete)
        db.session.commit()
        return redirect(
            url_for('showRestaurants', business_id=business_id))
    else:
        return render_template(
            'deleteRestaurant.html', restaurant=restaurantToDelete)


############# MenuItem #########
# Show Menu
@app.route('/restaurant/<string:business_id>')
@app.route('/restaurant/<string:business_id>/menu')
def showMenu(business_id):
    location = Location.query.filter( Location.business_id == business_id ).all()
    restaurant = Restaurant.query.filter( Restaurant.business_id == business_id ).first()
    items = db.session.query(MenuItem).filter_by(
        business_id=business_id).limit(8)
    all_cate_avg =dict(db.session.query(
        MenuItem.category,func.avg(MenuItem.price)).group_by( MenuItem.category ).all())
    for key ,value in  all_cate_avg.items():
        all_cate_avg[key] = format( float( value ) , '.2f')
    
    most_expensive = db.session.query(MenuItem).order_by(
        desc(MenuItem.price)
    ).limit(1).first()
    
    
    
    return render_template('showMenu.html', items=items, 
                                            hours=restaurant.hours,
                                            business_id=business_id,
                                            restaurant=restaurant, 
                                            location=location,
                                            avg = all_cate_avg ,
                                            exp=most_expensive)

# Create a new menu item
@app.route(
    '/restaurant/<string:business_id>/menu/new/', methods=['GET', 'POST'])
def newMenuItem(business_id):
    if request.method == 'POST':
        newItem = MenuItem(name=request.form['name'], description=request.form[
                           'description'], price=request.form['price'], item_type=request.form['category'], business_id=business_id)
        db.session.add(newItem)
        db.session.commit()

        return redirect(url_for('showMenu', business_id=business_id))
    else:
        return render_template('newmenuitem.html', business_id=business_id)


# Update a menu item
@app.route('/restaurant/<string:business_id>/menu/<int:item_id>/edit',
           methods=['GET', 'POST'])
def editMenuItem(business_id, item_id):
    editedItem = db.session.query(MenuItem).filter_by(item_id=item_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['name']
        if request.form['price']:
            editedItem.price = request.form['price']
        if request.form['course']:
            editedItem.category = request.form['course']
        db.session.add(editedItem)
        db.session.commit()
        return redirect(url_for('showMenu', business_id=business_id))
    else:

        return render_template(
            'editmenuitem.html', business_id=business_id, item_id=item_id, item=editedItem)

# Delete a menu item
@app.route('/restaurant/<string:business_id>/menu/<int:item_id>/delete',
           methods=['GET', 'POST'])
def deleteMenuItem(business_id, item_id):
    itemToDelete = db.session.query(MenuItem).filter_by(item_id=item_id).one()
    if request.method == 'POST':
        db.session.delete(itemToDelete)
        db.session.commit()
        return redirect(url_for('showMenu', business_id=business_id))
    else:
        return render_template('deleteMenuItem.html', item=itemToDelete, business_id=business_id,item_id=itemToDelete.item_id)

#############  Raters #########
# show answers for the last part in the same page
@app.route('/')
@app.route('/raters/')
def showRaters():
    counts = func.count(Rating.user_id).label("count_rating")
    rater = db.session.query( 
        Rater ,Restaurant, MenuItem ,Rating,
        MenuItem.item_id ,  Rater.user_id ,
        Rating.menu_id , Rating.business_id ,
        func.count(Rating.user_id).label("count_rating")).\
    filter(Rating.user_id == Rater.user_id).\
    filter(Restaurant.business_id == Rating.business_id).\
    filter(MenuItem.item_id == Rating.menu_id ).\
        group_by(Rater.name,Rater.user_id,
                 Restaurant.business_id  ,
                 MenuItem.item_id,
                 Rating.menu_id,
                 Rating.business_id,
                 Rating.id 
                 ).order_by( desc(counts)
    ).first()

    return render_template('raters.html', rater = rater[0], 
                                          restaurant=rater[1],
                                          item=rater[2],
                                          rating=rater[3])
    

# CRUD for raters
@app.route('/')
@app.route('/raterlist/')
def raterList():
    raterlist = db.session.query(Rater).limit(20).all()

    return render_template('raterlist.html',raterlist=raterlist)
 
# Create a new rater
@app.route(
    '/raterlist/new/', methods=['GET', 'POST'])
def newRater():
    if request.method == 'POST':
        newRater = Rater(name=request.form['name'],
                        join_date=request.form['join_date'],
                        user_id='00',
                        reputation='0',
                        rater_type='0'
                        )
        db.session.add(newRater)
        db.session.commit()
 
        return redirect(url_for('raterList'))
    else:
        return render_template('newRater.html')    

# Update a rater
@app.route('/raterlist/<string:user_id>/edit/',methods=['GET','POST'])
def editRater(user_id):
    e_rater = db.session.query(
        Rater).filter_by(user_id=user_id).one()
    if request.method == 'POST':
            if request.form['name']:
                e_rater.name = request.form['name']
                return redirect(url_for('raterList'))
    else:
            return render_template(
                'editRater.html',e_rater=e_rater, user_id=e_rater.user_id)

# Delete a rater
@app.route('/raterlist/<string:user_id>/delete/', methods=['GET', 'POST'])
def deleteRater(user_id):
    d_rater = db.session.query(
        Rater).filter_by(user_id=user_id).one()
    if request.method == 'POST':
        db.session.delete(d_rater)
        db.session.commit()
        return redirect(
            url_for('raterList'))
    else:
        return render_template(
            'deleteRater.html',d_rater=d_rater, user_id=d_rater.user_id)

    


#############  Ratings #########
@app.route('/ratings/<string:business_id>/')
@app.route('/ratings/<string:business_id>/ratings')
def showRatings(business_id):
    ratings=Rating.query.filter(Rating.business_id == business_id).limit(10)
    
    return render_template('ratings.html',ratings=ratings)



@app.route('/news/')
def news():
    return render_template('news.html')

if __name__ == "__main__":
    app.run( port=5000,debug=True )
