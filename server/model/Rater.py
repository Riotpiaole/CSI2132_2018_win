from sqlalchemy import ARRAY, Column, DateTime, ForeignKey, Float,  Integer, String
from sqlalchemy.ext.declarative import declarative_base
from model import Base 
from sqlalchemy.orm import relationship , sessionmaker 

class Rater(Base):
    __tablename__='rater'

    #mapper
    user_id = Column(String (22), primary_key=True)
    email = Column(String)

    # an alias such as SuperSizeMe
    name = Column(String)

    # show when this rater first joined the website
    join_date = Column(DateTime)

    # type of rater (blog, online, food critic)
    rater_type = Column(String) 

    # takes a value between 1 and 5
    # the value based on the number of people who found 
    # this  rater’s opinion helpful, and the default value is 1 (lowest).
    reputation = Column(Integer) 

    # 1 rater writes N ratings
    ratings = relationship('Rating')

    def __init__(self, user_id, name, join_date, reputation):
        self.user_id = user_id
        self.name = name
        self.join_date = join_date
        self.reputation = reputation
    