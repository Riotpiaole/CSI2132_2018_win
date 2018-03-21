from sqlalchemy import ARRAY, Column, DateTime, ForeignKey, Float,  Integer, String
from sqlalchemy.ext.declarative import declarative_base
from model import Base

class Location(Base):
    __tablename__='location'
    neighborhood    = Column(String)
    address         = Column(String)
    city            = Column(String)
    state           = Column(String)
    postal_code     = Column(String)
    latitude        = Column(Float)
    longtitude      = Column(Float)

    location_id = Column(Integer , primary_key=True )
    first_open_date = Column(DateTime) 
    manager_name = Column(String)
    phone_number = Column(String(10))
    hour_open = Column( ARRAY( String( 7)))
    hour_close = Column( ARRAY( String( 7)))

    # restaurant id is a foreign key
    business_id  = Column(String (22), ForeignKey('restaurant.business_id'))

    def __init__(self, neighborhood, address, city, state, postal_code, latitude, longtitude, business_id):
        
        self.neighborhood = neighborhood
        self.address = address
        self.city = city
        self.state = state
        self.postal_code = postal_code
        self.latitude = latitude
        self.longtitude = longtitude
        self.business_id = business_id
