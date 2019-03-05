
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Categories,Item,User,Base

engine = create_engine('sqlite:///menuitems.db')

Base.metadata.bind = engine
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

#Create dummy datas
Category = Categories(name = "Soccer")
session.add(Category)
session.commit()

Item1 = Item(name = "Shinguards",description = "A shin guard or shin pad is a piece of equipment worn on the front of a players shin to protect them from injury.",Category_id = 1)
session.add(Item1)
session.commit()
Item2 = Item(name = "Jersey",description = "The shirt",categories = Category)
session.add(Item2)
session.commit()
Item3 = Item(name = "Soccer Cleats",description = "The shoes",categories = Category)
session.add(Item3)
session.commit()

Category1 = Categories(name = "Basketball")
session.add(Category1)
session.commit()

Category2 = Categories(name = "Baseball")
session.add(Category2)
session.commit()
Item4 = Item(name = "Bat",description = "The bat",categories = Category2)
session.add(Item4)
session.commit()

Category3 = Categories(name = "Frisbee")
session.add(Category3)
session.commit()
Item5 = Item(name = "Frisbee",description = "A frisbee is a gliding toy or sporting item that is generally plastic and roughly 8 to 10 inches (20 to 25 cm) in diameter with a pronounced lip.",categories = Category3)
session.add(Item5)
session.commit()

Category4 = Categories(name = "Snowboarding")
session.add(Category4)
session.commit()
Item6 = Item(name = "Goggles",description = "Goggles, or safety glasses, are forms of protective eyewear that usually enclose or protect the area surrounding the eye in order to prevent particulates, water or chemicals from striking the eyes. ",
categories = Category4)
session.add(Item6)
session.commit()
Item7 = Item(name = "Snowboard",description = "Snowboards are boards where both feet are secured to the same board, which are wider than skis, with the ability to glide on snow.",
categories = Category4)
session.add(Item7)
session.commit()

Category5 = Categories(name = "Rock Climbing")
session.add(Category5)
session.commit()

Category6 = Categories(name = "Foosball")
session.add(Category6)
session.commit()

Category7 = Categories(name = "Skating")
session.add(Category7)
session.commit()

Category8 = Categories(name = "Hockey")
session.add(Category8)
session.commit()
Item8 = Item(name = "Stick",description = "A hockey stick is a piece of sport equipment used by the players in all the forms of hockey to move the ball or puck  either to push, pull, hit, strike, flick, steer, launch or stop the ball/puck during play with the objective being to move the ball/puck around the playing area using the stick.",
categories = Category8)

print("added items!")