from flask import Flask, jsonify, abort, request
from flask_restless import APIManager
from flask_sqlalchemy import SQLAlchemy
import os 
from model import * 

template_dir = os.path.abspath( "../template/" )

app = Flask( "Server" , template_folder = template_dir )
app.config.from_pyfile ( 'config.py' )
db = SQLAlchemy( app )

# Adding routes over here 

@app.route( "/" )
@app.route( "/main" )
def main():
    user = {'username': 'Miguel'}
    return render_template( 'index.html' 
        , user=user )

@app.route( "/restaurant" , methods=["GET"] )
def get_restaurant():
    all_restaurants = Restaurant.query.limit(10).all()
    all_restaurants = restaurants_schema.dump( all_restaurants )
    return jsonify( all_restaurants.data )


if __name__ == "__main__":
    app.run( debug=True )
    