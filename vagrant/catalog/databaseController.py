from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,scoped_session,session
from database_setup import Base,Categories,Item,User

engine = create_engine(
    'sqlite:///menuitems.db'
)
Base.metadata.bind = engine
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance

session = scoped_session(sessionmaker(bind=engine))
# A Session instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback().Because of the scoped_session function,
# we dont neet to care about threads here.

#get all categories from database
def getAllCategories():
    allCates = session.query(Categories)
    return allCates

#get all items from database
def getAllItems():
    allItems = session.query(Item)
    return allItems

#get all items belong to this category
def getItemsByCatId(cId):
    items = session.query(Item).filter_by(Category_id=cId)
    return items

#get Category Id from Category bane
def getCategoriesIdByName(cName):
    cid = session.query(Categories).filter_by(name = cName).first().id
    return cid
def getCategoryByName(cName):
    category = session.query(Categories).filter_by(name=cName).first()
    return category
def getCategotyById(cId):
    category = session.query(Categories).filter_by(id = cId).first()
    return category
#get Item description from item name and category name
def getItemDescriptionByName(cName,iName):
    cid = getCategoriesIdByName(cName)
    itemdes = session.query(Item).filter_by(name = iName).filter_by(Category_id = cid).first().description 
    return itemdes
#get Item object from item name
def getItemByItemName(iName):
    item = session.query(Item).filter_by(name = iName).first()
    return item
#add new Item object to the database
def addNewItem(iName,iDes,categoryName):
    cate = getCategoryByName(categoryName)
    item = Item(name=iName,description=iDes,categories=cate)
    session.add(item)
    session.commit()
#edit item and commit the changes to the database
def editItem(iName,iDes,iCate,thisItem):
    oldItem = getItemByItemName(thisItem)
    oldItem.name = iName
    oldItem.description = iDes
    oldItem.categories = getCategoryByName(iCate)
    session.commit()
#delete item from the database
def deleteItem(dItem):
    session.delete(dItem)
    session.commit()
