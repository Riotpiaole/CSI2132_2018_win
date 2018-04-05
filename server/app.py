from flask import Flask, jsonify, request, render_template, redirect, url_for
from flask_restless import APIManager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
import os 

template_dir = os.path.abspath( "../template/" )
static_dir = os.path.abspath( "../static/" )

app = Flask( "Server" , template_folder = template_dir , static_folder = static_dir)
# Connecting to the database
app.config.from_pyfile ( 'config.py' )
db = SQLAlchemy( app ) # database object

from model import * 
# Adding routes over here 

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

# Show rating items in JSON
@app.route( "/ratingitems/JSON")
def ratingitemsJSON():
    ratingitems = RatingItem.query.limit(10).all()
    ratingitems = ratingitems_schema.dump( ratingitems )
    return jsonify( ratingitems.data )


######### Create Read Update Delete ###########################

######### RESTAURANT ######### 

# show all restaurants
@app.route('/')
@app.route('/restaurant/')
def showRestaurants():
    restaurants = db.session.query(Restaurant).limit(5).all()
    return render_template('restaurants.html', restaurants = restaurants)

# create a new restaurant
@app.route('/restaurant/new/', methods=['GET','POST'])
def newRestaurant():
    if request.method == 'POST':
        newRestaurant = Restaurant(name=request.form['name'],
                                    b_id='111',
                                    review_count=0,
                                    is_open = 0)
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
    restaurant = db.session.query(Restaurant).filter_by(business_id).one()
    items = db.session.query(MenuItem).filter_by(
        business_id=business_id).all()
    
    return render_template('showMenu.html', items=items, restaurant=restaurant)

# Create a new menu item
@app.route(
    '/restaurant/<string:business_id>/menu/new/', methods=['GET', 'POST'])
def newMenuItem(business_id):
    if request.method == 'POST':
        newItem = MenuItem(name=request.form['name'], description=request.form[
                           'description'], price=request.form['price'], category=request.form['category'], business_id=business_id)
        db.session.add(newItem)
        db.session.commit()

        return redirect(url_for('showMenu', business_id=business_id))
    else:
        return render_template('newmenuitem.html', business_id=business_id)

    return render_template('newMenuItem.html', restaurant=restaurant)

# Update a menu item
@app.route('/restaurant/<string:business_id>/menu/<string:item_id>/edit',
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
@app.route('/restaurant/<string:business_id>/menu/<string:item_id>/delete',
           methods=['GET', 'POST'])
def deleteMenuItem(business_id, item_id):
    itemToDelete = db.session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        db.session.delete(itemToDelete)
        db.session.commit()
        return redirect(url_for('showMenu', business_id=business_id))
    else:
        return render_template('deleteMenuItem.html', item=itemToDelete)

#############  Rater #########

#############  Rating #########

#############  Rating Item #########



if __name__ == "__main__":
    app.run( debug=True )
    