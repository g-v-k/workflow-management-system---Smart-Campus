from INVISILATION.set_invisilation.main import app, centralEngineSubmitURL
from pymongo import MongoClient
from flask import render_template,request, make_response
import requests, json
from threading import Thread
from datetime import datetime,date


mongoClient = MongoClient('localhost',27017)
myDB = mongoClient['invisilation']
myCollection = myDB['ans_sheets_returned']
logCollection = mongoClient['workflow_log']['log']

def sendPostRequests(url,jsonData, headers):
    requests.post(url = url,json = jsonData, headers=headers)

@app.route('/ans_sheets_returned/getjobs',methods=['GET'])
def get_ans_sheets_returned_jobs():
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

@app.route('/ans_sheets_returned/renderjob/<jobID>', methods=['GET'])
def render_ans_sheets_returned_job(jobID):
    job = myCollection.find_one({"jobID":int(jobID)})
    resp = make_response(render_template('ans_sheets_returned.html', job=job))
    resp.mimetype = 'text/plain'
    return resp


@app.route('/ans_sheets_returned/submit', methods=['POST'])
def ans_sheets_returned_submit():
    jobID = request.form['jobID']
    row = myCollection.find_one({"jobID":int(jobID)})
    row['papersReturnedOrNot'] = request.form['returnedOrNot']
    myCollection.delete_one({"jobID":int(jobID)})
    headers = {'Content-type': 'application/json'}
    del row['_id']
    Thread(target=sendPostRequests, args=(centralEngineSubmitURL,row,headers)).start()
    #requests.post(url = centralEngineSubmitURL,json = row, headers=headers)
    return 'Node submitted'


# Store the information coming from Central Engine
@app.route('/ans_sheets_returned/store_info',methods=['POST'])
def storeAnswerSheetsReturnedInfo():
    jsonInfo = request.json
    jsonInfo['nodeID'] = 'ans_sheets_returned'
    myCollection.insert_one(jsonInfo)
    logCollection = mongoClient['workflow_log']['log']
    logCollection.insert_one({
            'date':date.today().strftime("%d/%m/%Y"),
            'processed-time':datetime.now().strftime("%H:%M:%S"),
            'wfID': jsonInfo['wfID'],
            'nodeID':'ans_sheets_returned',
            'jobID':jsonInfo['jobID'],
            'status':"Recieved.Processing..."

    }) 
    return 'success'
