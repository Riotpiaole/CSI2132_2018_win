from sqlalchemy import ARRAY, Column, DateTime, ForeignKey, Float,  Integer, String
from sqlalchemy.ext.declarative import declarative_base
from model import Base , json 
from sqlalchemy.orm import relationship , sessionmaker 

class Restaurant(Base,object):
    __tablename__='restaurant'

    business_id = Column(String (22), primary_key=True)
    name = Column(String)

    stars = Column(Float) 
    review_count = Column(Integer)

    # 0 for closed, 1 for open
    is_open = Column(Integer)

    # type  attribute contains details about the cuisine, 
    # such as Italian, Indian, Middle Eastern, and so on.
    food_type = Column( ARRAY( String))
    hours = Column( ARRAY( String( 7))) # [ "Mon", "Tue" ... ]

    URL = Column(String)

    # 1 restaurant has N ratings
    ratings = relationship('Rating')

    # 1 restaurant has N locations
    locations = relationship('Location')

    # 1 restaurant serves M menu items
    items = relationship('MenuItem')

    def __init__(self,b_id,name,review_count,is_open):
        self.business_id=b_id
        self.name=name
        self.review_count=review_count
        self.is_open=is_open
