import sys
from sqlalchemy import Column,ForeignKey,Integer,String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

#create the base class
Base = declarative_base()

#create new class,this class will be the class to which we map this table.
#Within the class,we define details about the table to which we will be mapping.
class Categories(Base):
    __tablename__ = 'categories'
    id = Column(Integer,primary_key=True)
    name = Column(String(80),nullable = False)

class Item(Base):
    __tablename__ = 'item'
    id = Column(Integer,primary_key = True)
    name = Column(String(80),nullable=False)
    description = Column(String(250),nullable = True)
    Category_id = Column(
        Integer,ForeignKey('categories.id')
    )
    categories = relationship("Categories")
    
class User(Base):
    __tablename__ = 'user'
    id = Column(Integer,primary_key = True)
    username = Column(String(50),nullable = False)
    email = Column(String(80),nullable = False)
    picture = Column(String(250),nullable = True)

#create an instance of engine
engine = create_engine(
    'sqlite:///menuitems.db'
)
#combine the Base and the engine to get database
Base.metadata.create_all(engine)