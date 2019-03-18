from flask import Flask
from flask import (render_template,request,url_for,redirect,flash,jsonify)

import os,sys
from flask import session as login_session
import random,string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json

from flask import make_response
import requests

from database_setup import  Categories, Base, Item, User
import databaseController as dc

app = Flask(__name__)
CLIENT_ID = json.loads(
    open('client_secret.json','r').read()
)['web']['client_id']
APPLICATION_NAME = "Restaurant Menu Application"
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
    # protect user away for session hijacking,if user open the home page,he will get a random state code.
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state']=state
    cates = dc.getAllCategories()
    items = dc.getAllItems()
    if 'username' in login_session and 'user_id' in login_session:
        return render_template("home.html",categories=cates,listItems = items,STATE=state,logedIn=True)
    else:
        return render_template("home.html",categories=cates,listItems = items,STATE=state,logedIn=False)
@app.route('/gconnect',methods=['POST'])
def gconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'),401)
        response.headers['Content-Type'] = 'application/json'
        return response
    
    code = request.data

    try:
        oauth_flow = flow_from_clientsecrets('client_secret.json',scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'),401
        )
        response.headers['Content-Type'] = 'application/json'
        return response

    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'%access_token)
    print access_token
    h = httplib2.Http()
    res = h.request(url,'GET')[1]
    result = json.loads(res)
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')),500)
        response.headers['Content-Type'] = 'application/json'
        return response
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dump("Token's user ID doesnt match given user ID"),401
        )
        response.header['Content-Type'] = 'application/json'
        return response
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response
    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    login_session['access_token'] = credentials.access_token
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        dc.createUser(login_session)
        response = make_response(
            json.dumps("LogedIn"), 300)
        response.headers['Content-Type'] = 'text/plain'
        return response
    login_session['gplus_id'] = gplus_id

    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo?alt=json"
    params = {'access_token': credentials.access_token}
    answer = requests.get(userinfo_url,params=params)

    data = answer.json()
    
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    dc.createUser(login_session)
    response = make_response('LogedIn',200)
    response.headers['Content-Type'] = 'text/plain'
    return response
@app.route('/gdisconnect',methods=['POST'])
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print"access_token is none,the user is not connected"
        response = make_response(json.dump("current user not connected!"),401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result1 = h.request(url,'GET')
    result2 = result1[0]
    print login_session
    print result1
    print result2
    if result2['status'] == '200':
        if 'provider' in login_session:
            del login_session['provider'] 
        if 'gplus_id' in login_session:
            del login_session['gplus_id']
        if 'access_token' in login_session:
            del login_session['access_token']
        if 'username' in login_session:
            del login_session['username']
        if 'email' in login_session:
            del login_session['email']
        if 'picture' in login_session:
            del login_session['picture']
        if 'user_id' in login_session:
            del login_session['user_id']
       
        response = make_response('LogedOut',200)
        response.headers['Content-Type'] = 'text/plain'
        return response
    else:
        response = make_response(json.dumps("Failed to revoke token for given user.",400))
        response.headers["Content-Type"] = 'application/json'
        return response
@app.route('/catalog/<catalog>/items')
def showItems(catalog):
    cates = dc.getAllCategories()
    cid = dc.getCategoriesIdByName(catalog)
    items = dc.getItemsByCatId(cid)
    if 'username' in login_session and 'user_id' in login_session:
        return render_template("home.html",categories=cates,listItems = items,cata=catalog,logedIn=True)
    else:
        return render_template("home.html",categories=cates,listItems = items,cata=catalog,logedIn=False)

@app.route('/catalog/<catalog>/<item>')
def description(catalog,item):
    des = dc.getItemDescriptionByName(catalog,item)
    if 'username' in login_session and 'user_id' in login_session:
        return render_template("home.html",description = des,return_item = item,logedIn=True)
    else:
        return render_template("home.html",description = des,return_item = item,logedIn=False)
@app.route('/catalog/<item>/edit',methods=['GET','POST'])
def edit(item):
    if 'username' in login_session and 'user_id' in login_session:
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
    else:
        return redirect(url_for(home))

@app.route('/catalog/<item>/delete',methods=['GET','POST'])
def delete(item):
    if 'username' in login_session and 'user_id' in login_session:
        thisItem = dc.getItemByItemName(item)
        if request.method == 'GET':
            return render_template("delete.html",thisitem=thisItem)
        elif request.method == 'POST':
            dc.deleteItem(thisItem)
            flash("You have deleted this item succesfully!")
            return redirect(url_for("home"))
    else:
        return redirect(url_for(home))
@app.route('/catalog/add',methods=['GET','POST'])
def add():
    if 'username' in login_session and 'user_id' in login_session:
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
    else:
        return redirect(url_for(home))
     
@app.route('/catalog.json')
def jsondata():
    cates = dc.getAllCategories()
    a = jsonify(Category=[c.serialize for c in cates])
    return a
if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = False
    app.run(host='127.0.0.1',port = 8000)
