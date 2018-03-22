from sqlalchemy import create_engine
import os , sys , json , glob , itertools 
from sqlalchemy.orm import sessionmaker 
from timeit import timeit
from time import time

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
            ''')
    sys.exit( -1 )

# Importing model 
from model import Restaurant , Rater , Location , Base , Rating

def parse_restaurant( bucket , line ):
    item = json.loads( line )
    bucket.append(Restaurant( item['business_id'], 
                                item['name'],
                                item['review_count'],
                                item['is_open'] ) )

def parse_review( bucket , line , sess ):
    item = json.loads( line )
    has_user = sess.query ( sess.query( Rater ).
                filter(Rater.user_id == item['user_id']
                ).exists() ).first()[0]
    
    has_business = sess.query( sess.query( Restaurant ).
                filter(Restaurant.business_id == item['business_id']
                ).exists()).first()[0]

    if has_user and has_business:
        print ( "has paired business and user ")
        return Rating( item['user_id'],item['business_id'],
                        item['date'],item['text'])

def parse_user ( bucket , line ):
    item = json.loads ( line )
    bucket.append( Rater( item[ 'user_id' ] ,
                          item[ 'name' ],
                          item[ 'yelping_since' ],
                          item[ 'average_stars' ]))

def parse_location ( bucket , line ):
    item = json.loads( line )
    bucket.append( Location(  item['neighborhood'],
                                item['address'],
                                item['city'],
                                item['state'],
                                item['postal_code'],
                                item['latitude'],
                                item['longitude'],
                                item['business_id'] ) )

def connect( user = user , passwd  = password  , 
                database = database , 
                port = port ,
                host = host_name , 
                migrate=False ):
    '''
    connect: connecting to a database through postgresql and psycopg2 
    
    Args:
        user (str) = config.user : adminstrator name for database 
        passwd ( str ) = config.password : administration password to connect database 
        database ( str ) = config.database : database that will be connecting to 
        port ( int ) = config.port : port number to the database 
        host ( int ) = config.host_name : host ip to connecting to 
        migrate ( bool ) =  False: wether or not to creating the and migrating the data 
    '''
    db_connect_str = "postgresql+psycopg2://{}:{}@{}:{}/{}".format( 
        user, passwd , host , port , database)
    return db_connect_str

def init_db( num_data = 300 , insert_threshhold = 100 ):
    sess = connect(migrate=True) # session to the current database

    bus_bucket , location_bucket , user_bucket ,rating_bucket = [] , [] , [] , []
    
    with open("../dataset/business.json","r",buffering = insert_threshhold 
        ) as businesses :

        for count , business in enumerate( businesses.readlines() ):
            if count > num_data : break
            
            parse_restaurant( bus_bucket , business )
            parse_location ( location_bucket , business )

            if len( bus_bucket ) == insert_threshhold : 
                sess.add_all( bus_bucket )
                sess.add_all( location_bucket )
                location_bucket , bus_bucket = [] , [] 
                print ( "Inserting 100 rows of business and location")
                sess.commit() 
    
    with open("../dataset/user.json" , "r",buffering = insert_threshhold 
        ) as rater:

        for count , rater in enumerate ( rater.readlines() ):
            if count > num_data : break 
            
            parse_user( user_bucket , rater )
            if len( user_bucket ) == insert_threshhold :
                sess.add_all( user_bucket )
                user_bucket = [] 
                print ( "Inserting 100 rows of users" )
                sess.commit() 
    
    with open("../dataset/review.json" , "r", buffering = 1000 ) as rating:
        start_t = time()    
        for rater in rating:
            if len( rating_bucket ) == num_data: break    
            
            review = parse_review ( rating_bucket , rater , sess )
            if review:
                sess.add( review )

                rating_bucket.append( review ) 
                print ( "Insert one review" )
                sess.commit() 
    
        end_t = time()
        print ( "Reading 300 line runs {} ms".format( 
                round( (end_t -  start_t) , 2) ) )


     