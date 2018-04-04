from sqlalchemy import create_engine
import os , sys , json , glob , itertools 
from random import randint

from sqlalchemy.orm import sessionmaker 
from timeit import timeit

import pandas as pd 
from pandas.io import sql 

try:
    from config import * 
except ModuleNotFoundError :
    print ( '''Please provide config.py for database connection:
                in which include:
                        host_name : ip addr for host
                        port      : port num for db
                        database  : name of db 
                        password  : password of dbadminstrator
                        user      : name pf dbadminstrator
                And 
                import os 
                basedir = os.path.abspath( os.path.dirname( __file__ ) )
                SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://{}:{}@{}:{}/{}".format( 
                        user, password , host_name , port , database )
            ''')
    sys.exit( -1 )

FOOD_description = [ "Amazing food and make with fish and salad.", 
                     "Baked with beef and mushroom and fish" ,
                     "Wrap with ham and baked with caskate iron chesse",
                     "Blend with mushroom and nuts and folded with meat in bake", 
                     "Reversed sears steak and alfredio sources", 
                     "Pastry baked steak in beef wellington" ]


# Importing model 
from model import *
from app import db  
from base64 import encodestring  , b64encode

sess = db.session() 
# db.create_all() 
# db.session.commit() 

gen_int = lambda x : randint ( 0 , x - 1)

def parse_restaurant( bucket , line , restaurant_id = None ,genre_type = None  ):
    item = json.loads( line ) 
    bucket.append(
        Restaurant( item['business_id'], item['name']   , item['review_count'],
                    item['is_open' ]   , item[ 'stars' ],
                    item[ 'hours' ]    , food_type= item['categories'] ) )
    
    restaurant_id.append ( item[ 'business_id' ] )
    for genre in item['categories']:
        genre_type.append ( genre ) 

def parse_review( bucket  , line , user_id , rest_id , menu_id):
    item = json.loads( line )
    bucket.append ( Rating( user_id[ gen_int( len ( user_id ) ) ],
                                rest_id[ gen_int( len ( rest_id ) ) ],
                                item['date']   ,item['text'] , 
                                gen_int( 30 ) ,gen_int( 5 ) , menu_id[ gen_int (len( menu_id )) ]) )


def parse_user ( bucket , line , user_id ):
    item = json.loads ( line )
    bucket.append( Rater( item[ 'user_id' ]      ,item[ 'name' ],
                          item[ 'yelping_since' ],item[ 'average_stars' ]))
    user_id.append ( item['user_id']) 
    
def insert_data ( file_path , insert_threshhold , func , bucket , num_data , *args , insert=False ):
    with open ( file_path , "r" , buffering = 1000 ) as files:
        for count , line in enumerate( files ): 
            if count  == num_data : break 
            func( *args )
            if  len ( bucket ) == insert_threshhold and insert : 
                sess.add_all ( bucket ) 
                bucket = [] 
                sess.commit() 

# parsing the location 
def parse_location ( bucket , line ):
    item = json.loads( line )
    bucket.append( Location(  item['neighborhood'], item['address'],
                              item['city']        , item['state'],
                              item['postal_code'] , item['latitude'],
                              item['longitude']   , item['business_id'] ) )  

# read the csv file and insertting the data to the database
def read_csv_file ( file_folder    = "../dataset/" , 
                    file_name      = None  , 
                    category_id    = None  , 
                    restaurant_id  = None  , save = True ): 
    drop_columns = [ "menus_appeared" , "times_appeared" , 
                     "times_appeared" , "last_appeared"  ,
                     "first_appeared" ]
    menu_id =[]   
    
    if file_name and file_folder:
        file = os.path.join( file_folder , file_name )
        data = pd.read_csv( file )
        if not save: return list (data["item_id"])
        data.dropna( axis = 1 , how = 'any' , inplace = True )
        data.drop( columns = drop_columns , axis = 1 , inplace=True)
        data[ 'category' ]    = data.item_id.apply( lambda x : category_id[ gen_int( len( category_id ) ) ] )
        data[ 'business_id' ] = data.item_id.apply( lambda x : restaurant_id[ gen_int( len ( restaurant_id ) ) ] )
        data[ 'price' ] = data.item_id.apply ( lambda x : gen_int ( 30 ) )
        data[ 'description' ] = data.item_id.apply ( lambda x : gen_int (6 ) )
        return list(data['item_id '])
        if save :data.to_sql( "menuitem" , db.engine , if_exists='append' , index=False )
        
    else: raise ValueError("Invalid directory NONE filename")
    

# Initializes the database 

def init_db( num_data = 300 , insert_threshhold = 100 , inserting=True):
    bus_bucket , location_bucket , user_bucket  = [] , [] , [] 
    user_id ,rating_bucket , rest_id  , category= [], [] , [], []

    print ( "Inserting data ......")
    os.system ( "clear")
    print ( "Adding locations and busiensses ...... ")  
    
    
    with open("../dataset/business.json","r", buffering = insert_threshhold ) as businesses :        
        for count , business in enumerate( businesses.readlines() ):
            if count > num_data : break
            parse_restaurant( bus_bucket , business  ,  
                restaurant_id= rest_id , 
                genre_type= category )
            parse_location ( location_bucket , business )  
            if len( bus_bucket ) == insert_threshhold : 
                sess.add_all( bus_bucket )
                sess.add_all( location_bucket )
                location_bucket , bus_bucket = [] , [] 
                sess.commit() 
        
        category = list (set( category )) # all of category food 
    
    # inserting menu_item 
    print ( "Adding menus........")
    menu_id = read_csv_file( file_name= "Dish.csv" , category_id= category , restaurant_id= rest_id) 
    
    # inserting user 
    print ( "Adding users ...... ")
    with open("../dataset/user.json" , "r", buffering = insert_threshhold ) as rater:
        for count , rater in enumerate ( rater ):
            if count > num_data : break 
            parse_user( user_bucket , rater , user_id )
            if len( user_bucket ) == insert_threshhold :
                sess.add_all( user_bucket )
                user_bucket = [] 
                sess.commit() 
    
    user_id.remove( 'aRBFKDKgIfqtn83ZI4oNSQ' ) # avoid adding review issues 
    
    print ( "Adding reviews ...... ")
    with open("../dataset/review.json" , "r", buffering = 1000 ) as rating:
        for count , rater in enumerate (rating):
            if count  == num_data * 10 : break  
            parse_review ( rating_bucket , rater , user_id , rest_id ,menu_id )
            if  len(rating_bucket ) == insert_threshhold and inserting: # if the size of value reaches thresh hold 
                sess.add_all( rating_bucket )
                rating_bucket = []
                sess.commit() 
    


if __name__ == "__main__":
    db.create_all()
    db.session.commit() 
    init_db() 