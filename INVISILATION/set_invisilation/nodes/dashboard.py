from flask import Flask, render_template,g,session
from INVISILATION.set_invisilation.main import app
import json
from pymongo import MongoClient

mongoClient = MongoClient('localhost',27017)
credentialsCollection = mongoClient['login_credentials']['credentials']


@app.route('/dashboard', methods =['GET'])
def dashboard():
    return render_template("dashboard.html")

