from flask import Flask
from flask import (render_template,request,url_for,redirect,flash,jsonify)

import os
from flask import session as login_session
import random,string

from database_setup import  Categories, Base, Item, User

app = Flask(__name__)

@app.route('/')
def home():
    output = "<h1>Hi,Welcome</h1>"
    return output
@app.route('/catalog/<catalog>/items')
def items(catalog):
    output ="<p>%s items here</p>"%catalog
    return output
@app.route('/catalog/<catalog>/<item>')
def description(catalog,item):
    output = "<p>%s %s description here</p>"%(catalog,item)
    return output
@app.route('/catalog/<item>/edit')
def edit(item):
    output = "<p>%s edit here</p>"%item
    return output
@app.route('/catalog/<item>/delete')
def delete(item):
    output = "<p>%s delete here</p>"%item
    return output
@app.route('/catalog/<catalog>/add')
def add(catalog):
    output = "<p>add item to %s</p>"%catalog
    return output
@app.route('/catalog.json')
def json():
    output ="<p>all catalogies and items in json </p>"
    return output
if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = False
    app.run(host='127.0.0.1',port = 9000)
