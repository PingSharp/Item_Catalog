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
    cid = dc.getCategoriesIdByName(catalog)
    items = dc.getItemsByCatId(cid)
    output ="<p>%s items here</p>"%catalog
    output += "<ol>"
    for i in items:
        output += "<li>%s</li>"%i.name
    output += "</ol>"
    return output

@app.route('/catalog/<catalog>/<item>')
def description(catalog,item):
    des = dc.getItemDescriptionByName(catalog,item)
    output = "<p>%s %s description here</p>"%(catalog,item)
    output += "<p>%s</p>"%des
    output += "<a href='http://localhost:9000/catalog/%s/edit'>edit</a><br>"%item
    output += "<a href='http://localhost:9000/catalog/%s/delete'>delete</a>"%item
    return output
@app.route('/catalog/<item>/edit',methods=['GET','POST'])
def edit(item):
    thisItem = dc.getItemByItemName(item)
    cates = dc.getAllCategories()
    cateId = dc.getCategotyById(thisItem.Category_id).id
    if request.method == 'GET':
        output = "<h1>%s Item edit</h1>"%thisItem.name
        output += "<form  method='POST'>"
        output += "<input name='name' type='text' value='%s'>"%thisItem.name
        output += "<input name='description' type='text' value='%s'>"%thisItem.description
        output += "<select name='catalog'>"
        for c in cates:
            if c.id == cateId:
                output += "<option value='%s' selected>%s</option>"%(c.name,c.name)
            output += "<option value='%s'>%s</option>"%(c.name,c.name)
        output += "</select>"
        output += "<input type='submit' value='Edit'>"
        output += "</form>"
        return output
    elif request.method == 'POST':
        iName = request.form['name']
        iDes = request.form['description'] 
        iCate = request.form['catalog']
        dc.editItem(iName,iDes,iCate,item)
        return "<p>edit %s,%s,%s succesfully!</p>"%(iName,iDes,iCate)

@app.route('/catalog/<item>/delete',methods=['GET','POST'])
def delete(item):
    thisItem = dc.getItemByItemName(item)
    if request.method == 'GET':
        output = "<h1>Item delete</h1>"
        output += "<form action='http://localhost:9000/catalog/%s/delete' method='POST'>"%item
        output += "<label>Are you sure you want to delete this item(%s)?</label>"%thisItem.name
        output += "<input type='submit' value='Delete'>"
        output += "</form>"
        return output
    elif request.method == 'POST':
        dc.deleteItem(thisItem)
        return "<p>delete item succesfully!</p>"

@app.route('/catalog/add',methods=['GET','POST'])
def add():
    cates = dc.getAllCategories()
    if request.method == 'GET':
        output = "<h1>Add Item </h1>"
        output += "<form action='http://localhost:9000/catalog/add' method='POST'>"
        output += "<input type='text' name='name'><br>"
        output += "<input type='text' name='description'><br>"
        output += "<select name='catalog'>"
        output += "<option value=''>please choose a category</option>"
        for c in cates:
            output += "<option value='%s'>%s</option>"%(c.name,c.name)
        output += "</select>"
        output += "<input type='submit' value='Add'>"
        output += "</form>"
        return output
    elif request.method == 'POST':
        iName = request.form['name']
        iDes = request.form['description']
        iCate = request.form['catalog']
        dc.addNewItem(iName,iDes,iCate)
        return "<p>add %s,%s,%s succesfully!</p>"%(iName,iDes,iCate)
     
@app.route('/catalog.json')
def json():
    cates = dc.getAllCategories()
    a = jsonify(Category=[c.serialize for c in cates])
    return a
if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='127.0.0.1',port = 9000)
