import json 
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from model.Location import Location
from model.Rating import Rating 
from model.MenuItem import MenuItem
from model.Rater import Rater 
from model.RatingItem import RatingItem 
from model.Restaurant import Restaurant 
