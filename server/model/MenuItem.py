from sqlalchemy import ARRAY, Column, DateTime, ForeignKey, Float,  Integer, String
from sqlalchemy.ext.declarative import declarative_base
from model import Base 
from sqlalchemy.orm import relationship , sessionmaker 

class MenuItem(Base):
    __tablename__='menuitem'

    item_id  = Column(String (22), primary_key=True)
    name = Column(String) 

    # food or beverage 
    item_type = Column(String)

    # starter, main, desert 
    category = Column(String)
    description  = Column(String)
    price  = Column(String)

    # restaurant id is a foreign key
    business_id  = Column(String (22), ForeignKey('restaurant.business_id'))

    # M menu item  has N ratings
    ratings = relationship('Rating') 