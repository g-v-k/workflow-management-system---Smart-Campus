
from flask import Flask, request, jsonify, render_template
from threading import Thread
import os, sys,requests
from importlib import import_module,reload
import pandas as pd
from datetime import datetime,date
from pymongo import MongoClient
from flask_cors import CORS
app = Flask(__name__,template_folder = './')
CORS(app)


conditionsBaseFolder= '/media/vamsi/Everything else/MTP' 
sys.path.append(conditionsBaseFolder)

def sendPostRequests(url,jsonData, headers):
    requests.post(url = url,json = jsonData, headers=headers)

@app.route('/wfConditions/reload/<module>')
def conditionsReload(module):
    moduleName = import_module("SET_INVISILATION.wf_conditions."+module)
    reload(moduleName)
    return "vamsi"

@app.route('/wfEngine/submit',methods = ['GET','POST'])
def wf_submit() :
    #timer starts
    jsonData = request.json
    wfID = jsonData['wfID']
    nodeID = jsonData['nodeID']
    jobID = jsonData['jobID']
    store_log(wfID,nodeID,jobID,'processed')
    conditionsModule = import_module("INVISILATION.wf_conditions."+wfID)
    targetNodes = conditionsModule.conditionHandler(jsonData,nodeID)
    if targetNodes == None:
        return 'Workflow finished'
    headers = {'Content-type': 'application/json'}
    for node in targetNodes:
        Thread(target=sendPostRequests, args=(node['URL'],jsonData,headers)).start()
        #requests.post(url = node['URL'],json = jsonData, headers=headers)
    resp = jsonify(success=True)
    #timer ends
    # time1 - time2
    #0.000000006 sec
    return resp
    
@app.route('/wfEngine/display_log', methods=['GET'])
def display_log():
    mongoClient = MongoClient('localhost',27017)
    logCollection = mongoClient['workflow_log']['log']
   
    cursor = logCollection.find({},{ "_id": 0})
    myList = []
    for d in cursor:
        myList.append(d)
    if len(myList) == 0:
        return 'No Log found'
    else:
        workflow_log = pd.DataFrame(myList)
        return render_template('display_log.html',mydf=workflow_log)
        

def store_log(wfID, nodeID, jobID, status): 
    mongoClient = MongoClient('localhost',27017) 
    logCollection = mongoClient['workflow_log']['log']
    logCollection.insert_one({
            'date':date.today().strftime("%d/%m/%Y"),
            'processed-time':datetime.now().strftime("%H:%M:%S"),
            'wfID': wfID,
            'nodeID':nodeID,
            'jobID':jobID,
            'status':"Processed"

    })      

@app.route('/wfEngine/clear_log', methods=['GET'])
def clear_log():
    mongoClient = MongoClient('localhost',27017)
    logCollection = mongoClient['workflow_log']['log']
    logCollection.delete_many({})
    resp = jsonify(success=True)
    return resp


if __name__ == '__main__':
    app.run(port='2000')