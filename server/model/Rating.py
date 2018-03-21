from sqlalchemy import ARRAY, Column, DateTime, ForeignKey, Float,  Integer, String
from sqlalchemy.ext.declarative import declarative_base
from model import Base 

class Rating(Base):
    __tablename__='rating'

    #mapper
    user_id = Column(String (22), ForeignKey('rater.user_id'))
    business_id  = Column(String (22), ForeignKey('restaurant.business_id'))
    item_id = Column(String (22), ForeignKey('menuitem.item_id'))
    
    date = Column(DateTime, primary_key=True)
    
    # price, food, mood, staff attributes may 
    # take a value between 1(low) to 5(high)
    price = Column(Integer)
    food = Column(Integer)
    mood = Column(Integer)
    staff= Column(Integer)


    comments =Column(String)

    def __init__(self, user_id, business_id, date, comments ):
        self.user_id = user_id
        self.business_id = business_id
        self.date = date
        self.comments = comments