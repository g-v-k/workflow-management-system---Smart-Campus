from INVISILATION.set_invisilation.main import app, centralEngineSubmitURL
from pymongo import MongoClient
from flask import render_template,request, make_response
import requests, json
from threading import Thread
from datetime import datetime,date

mongoClient = MongoClient('localhost',27017)
myDB = mongoClient['invisilation']
myCollection = myDB['papers_given_to_profs']
logCollection = mongoClient['workflow_log']['log']

def sendPostRequests(url,jsonData, headers):
    requests.post(url = url,json = jsonData, headers=headers)


@app.route('/papers_given_to_profs/getjobs',methods=['GET'])
def get_papers_given_to_profs_jobs():
    jobList = []
    cursor = myCollection.find({},{'jobID':1})
    for doc in cursor:
        jobList.append(doc['jobID'])
    if len(jobList)!=0:
        resp = make_response(render_template('node_jobs.html', joblist=jobList))
        resp.mimetype = 'text/plain'
        return resp
    else:
        return 'No Data'


@app.route('/papers_given_to_profs/renderjob/<jobID>', methods=['GET'])
def render_papers_given_to_profs_job(jobID):
    job = myCollection.find_one({"jobID":int(jobID)})
    resp = make_response(render_template('papers_given_to_profs.html', job=job))
    resp.mimetype = 'text/plain'
    return resp


@app.route('/papers_given_to_profs/submit', methods=['POST'])
def papers_given_submit():
    jobID = request.form['jobID']
    row = myCollection.find_one({"jobID":int(jobID)})
    row['papersGivenOrNot'] = request.form['givenOrNot']
    myCollection.delete_one({"jobID":int(jobID)})
    headers = {'Content-type': 'application/json'}
    del row['_id']
    Thread(target=sendPostRequests, args=(centralEngineSubmitURL,row,headers)).start()
    #requests.post(url = centralEngineSubmitURL,json = row, headers=headers)
    return 'Node submitted'

# Stores the information coming from Central Engine
@app.route('/papers_given_to_profs/store_info',methods=['POST'])
def storePapersGivenInfo():
    jsonInfo = request.json
    jsonInfo['nodeID'] = 'papers_given_to_profs'
    myCollection.insert_one(jsonInfo)
    logCollection.insert_one({
            'date':date.today().strftime("%d/%m/%Y"),
            'processed-time':datetime.now().strftime("%H:%M:%S"),
            'wfID': jsonInfo['wfID'],
            'nodeID':'papers_given_to_profs',
            'jobID':jsonInfo['jobID'],
            'status':"Recieved.Processing..."

    })  
    return 'success'