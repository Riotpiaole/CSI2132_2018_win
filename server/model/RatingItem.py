from sqlalchemy import ARRAY, Column, DateTime, ForeignKey, Float,  Integer, String
from sqlalchemy.ext.declarative import declarative_base
from model import Base 


class RatingItem(Base):
    __tablename__='ratingitem'

    user_id  = Column(String (22), primary_key=True)
    date = Column(DateTime, primary_key=True)
    item_id   = Column(String (22), primary_key=True)
    rating = Column(Integer)
    comment = Column(String)