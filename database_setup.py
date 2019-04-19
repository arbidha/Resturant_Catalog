import sys
import os 
from sqlalchemy import Column, ForeignKey, Integer, String 
# used fot configuration and classcode
from sqlalchemy.ext.declarative import declarative_base
# to create foreign key relationship
from sqlalchemy.orm import relationship
# configuration at the end of the file
from sqlalchemy import create_engine

#create instance of declarative_base class 
Base = declarative_base()

# declarative base will let our classes are special SQLAlchemy classes 
# that correspond to tables in our database


class User(Base):
    # representing our table inside the database
    __tablename__ = 'user'

    id = Column(Integer, primary_key = True) 
    name = Column(String(250), nullable = False)    
    email = Column(String(250), nullable = False)
    picture = Column(String(250))
     

#We added this serialize function to be able to send JSON objects in a serializable format
    @property
    def serialize(self):
       
       return {
           'name'         : self.name,
           'email'        : self.email,
           'picture'      : self.picture,
           'id'           : self.id,
       }
 

class Restaurant(Base):
    #representing our table inside the database
    __tablename__ = 'restaurant'
    id = Column(Integer,primary_key = True)
    name = Column(String(80),nullable = False)
    user_id = Column(Integer,ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
       
       return {
           'name'         : self.name,
           'id'           : self.id
       }      
        

class MenuItem(Base):
    # representing our table inside the database
    __tablename__ = 'menu_item'

    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    description = Column(String(250))
    price = Column(String(8))
    course = Column(String(250))
    restaurant_id = Column(Integer,ForeignKey('restaurant.id'))
    restaurant = relationship(Restaurant) 
    user_id = Column(Integer,ForeignKey('user.id'))
    user = relationship(User)

#We added this serialize function to be able to send JSON objects in a serializable format
    @property
    def serialize(self):
       
       return {
           'name'         : self.name,
           'description'  : self.description,
           'id'           : self.id,
           'price'        : self.price,
           'course'       : self.course,
       }
 



######## insert at end of file ########
engine = create_engine('sqlite:///restaurantmenuwithusers.db')

Base.metadata.create_all(engine)



