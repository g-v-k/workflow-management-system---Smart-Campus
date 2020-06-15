from flask import Flask,request, render_template, redirect,session,g, jsonify,url_for
from INVISILATION.set_invisilation.main import app
from pymongo import MongoClient

mongoClient = MongoClient('localhost',27017)
credentialsCollection = mongoClient['login_credentials']['credentials']

@app.before_request
def before_request():
    if 'username' not in session and request.endpoint not in ['loginFunction','inviteMailInvisilation','thanksMailInvisilation','storePapersGivenInfo','storeAnswerSheetsReturnedInfo'] and '/static/' not in request.path:
        return redirect(url_for("loginFunction"))
    
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
    return response

@app.route('/', methods=['GET'])
def baseFunction():
    return redirect(url_for("loginFunction"))

@app.route('/login',methods=['GET','POST'])
def loginFunction():
    if request.method == "GET":
        if 'username' in session:
            return redirect('/dashboard')
        return render_template('login.html')
    elif request.method == "POST":
        credentials = request.json
        profileDoc = credentialsCollection.find_one({'username':credentials['username'],'password':credentials['password']})
        if  profileDoc != None:
            session['username'] = credentials['username']
            return jsonify({"login":"success","redirect": "/dashboard"})
        else:
            return jsonify({"login":"fail","redirect": "/login"})


@app.route('/logout',methods=['POST'])
def logout():
    session.pop('username', None)
    return jsonify({"logout":"success","redirect": "/login"})  
       



