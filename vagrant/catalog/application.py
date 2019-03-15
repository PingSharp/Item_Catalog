from flask import Flask
from flask import (render_template,request,url_for,redirect,flash,jsonify)

import os,sys
from flask import session as login_session
import random,string

from database_setup import  Categories, Base, Item, User
import databaseController as dc

app = Flask(__name__)
#rendering css file on time
@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)

@app.route('/')
def home():
    cates = dc.getAllCategories()
    items = dc.getAllItems()
    return render_template("home.html",categories=cates,listItems = items)
@app.route('/catalog/<catalog>/items')
def showItems(catalog):
    cates = dc.getAllCategories()
    cid = dc.getCategoriesIdByName(catalog)
    items = dc.getItemsByCatId(cid)
    return render_template("home.html",categories=cates,listItems = items,cata=catalog)

@app.route('/catalog/<catalog>/<item>')
def description(catalog,item):
    des = dc.getItemDescriptionByName(catalog,item)
    return render_template("home.html",description = des,return_item = item)
@app.route('/catalog/<item>/edit',methods=['GET','POST'])
def edit(item):
    thisItem = dc.getItemByItemName(item)
    cates = dc.getAllCategories()
    cateId = dc.getCategotyById(thisItem.Category_id).id
    if request.method == 'GET':
        return render_template("edit.html",thisitem=thisItem,categories=cates,cId=cateId)
    elif request.method == 'POST':
        iName = request.form['name']
        iDes = request.form['description'] 
        iCate = request.form['catalog']
        dc.editItem(iName,iDes,iCate,item)
        flash("You have edited this item succesfully!")
        return redirect(url_for("home"))

@app.route('/catalog/<item>/delete',methods=['GET','POST'])
def delete(item):
    thisItem = dc.getItemByItemName(item)
    if request.method == 'GET':
        return render_template("delete.html",thisitem=thisItem)
    elif request.method == 'POST':
        dc.deleteItem(thisItem)
        flash("You have deleted this item succesfully!")
        return redirect(url_for("home"))
@app.route('/catalog/add',methods=['GET','POST'])
def add():
    cates = dc.getAllCategories()
    if request.method == 'GET':
        return render_template("add.html",categories=cates)
    elif request.method == 'POST':
        iName = request.form['name']
        iDes = request.form['description']
        iCate = request.form['catalog']
        dc.addNewItem(iName,iDes,iCate)
        flash("You have added the new item succesfully!")
        return redirect(url_for("home"))
     
@app.route('/catalog.json')
def json():
    cates = dc.getAllCategories()
    a = jsonify(Category=[c.serialize for c in cates])
    return a
if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='127.0.0.1',port = 9000)
