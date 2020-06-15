from INVISILATION.set_invisilation.main import app,centralEngineSubmitURL
from threading import Thread
from flask import request, render_template, make_response
import requests

def generatorJobIDs():
    for i in range(1,10):
        yield i

def sendPostRequests(url,jsonData, headers):
    requests.post(url = url,json = jsonData, headers=headers)

jobid = generatorJobIDs()

@app.route('/set_invisilation_register/getjobs',methods=['GET'])
def get_set_invisilation_register_jobs():
    jobList = ["1"]
    resp = make_response(render_template('node_jobs.html', joblist=jobList))
    resp.mimetype = 'text/plain'
    return resp

@app.route('/set_invisilation_register/renderjob/1', methods=['GET'])
def render_set_invisilation_register_job():
    resp = make_response(render_template('set_invisilation_register.html'))
    resp.mimetype = 'text/plain'
    return resp

@app.route('/set_invisilation_register/submit', methods = ['POST'])
def registerSubmit():
    invisilationData = {}
    invisilationData['profName'] = request.form['profName']
    invisilationData['studentName'] = request.form['studentName']
    invisilationData['studentRollNo'] = request.form['studentRollNo']
    invisilationData['roomNo'] = request.form['roomNo']
    invisilationData['examDate'] = request.form['examDate']
    invisilationData['timeSlot'] = request.form['timeSlot']
    invisilationData['nodeID'] = 'set_invisilation_register'
    invisilationData['wfID'] = 'invisilation'
    invisilationData['jobID'] = jobid.__next__()
    headers = {'Content-type': 'application/json'}
    Thread(target=sendPostRequests, args=(centralEngineSubmitURL,invisilationData,headers)).start()
    #requests.post(url = centralEngineSubmitURL,json = invisilationData, headers=headers)
    return 'success'
