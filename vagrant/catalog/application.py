from flask import Flask
from flask import (render_template,request,url_for,redirect,flash,jsonify)

import os,sys
from flask import session as login_session
import random,string

from database_setup import  Categories, Base, Item, User
import databaseController as dc

app = Flask(__name__)


@app.route('/')
def home():
    cates = dc.getAllCategories()
    items = dc.getAllItems()
    output = "<h1>Hi,Welcome</h1>"
    output += "<ol>"
    for c in cates:
        output += "<li>%s</li>"%c.name
    output += "</ol>"
    output += "<ol>"
    for i in items:
        output += "<li>%s</li>"%i.name
    output += "</ol>"
    return output
@app.route('/catalog/<catalog>/items')
def items(catalog):
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
    return output
@app.route('/catalog/<item>/edit',methods=['GET','PUT'])
def edit(item):
    if request.method == 'GET':
        output = "<h1>Item edit</h1>"
        output += "<form action='http://localhost:9000/catalog/%s/edit' method='PUT'>"%item
        output += "<input name='name' type='text'>"
        output += "<input name='description' type='text'>"
        output += "<input type='submit' value='Edit'>"
        output += "</form>"
        return output
    elif request.method == 'PUT':
        return None    

@app.route('/catalog/<item>/delete',methods=['GET','DELETE'])
def delete(item):
    if request.method == 'GET':
        output = "<h1>Item delete</h1>"
        output += "<form action='http://localhost:9000/catalog/%s/delete' method='DELETE'>"%item
        output += "<label>Are you sure you want to delete this items?</label>"
        output += "<input type='submit' value='Delete'>"
        output += "</form>"
        return output
    elif request.method == 'DELETE':
        return None  
@app.route('/catalog/<catalog>/add',methods=['GET','POST'])
def add(catalog):
    cates = dc.getAllCategories()
    if request.method == 'GET':
        output = "<h1>Add Item </h1>"
        output += "<form action='http://localhost:9000/catalog/%s/add' method='POST'>"%catalog
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
    output ="<p>all catalogies and items in json </p>"
    return output
if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='127.0.0.1',port = 9000)
