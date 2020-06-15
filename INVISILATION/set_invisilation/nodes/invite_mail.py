from  INVISILATION.set_invisilation.main import app, centralEngineSubmitURL
from flask import request
from threading import Thread
from email.message import EmailMessage
import smtplib,requests


def sendPostRequests(url,jsonData, headers):
    requests.post(url = url,json = jsonData, headers=headers)

@app.route('/set_invisilation/invite_mail_invisilation', methods=['POST'])
def inviteMailInvisilation():
    roomDetails =  request.json
    profName = roomDetails['profName']
    studentName = roomDetails['studentName']
    studentRollNo = roomDetails['studentRollNo']
    roomNo = roomDetails['roomNo']
    examDate = roomDetails['examDate']
    timeSlot = roomDetails['timeSlot']
    
    fromAddr = 'cs18m005@iittp.ac.in'
    toAddr = 'cs18m005@iittp.ac.in'

    message = EmailMessage()
    message['Subject'] = "Invisilation Duty"
    message['From'] = fromAddr
    message['To'] = toAddr
    message.set_content("""\
       This mail is to inform that {}({}) and {} have been assigned invisilation duty in room number {} on {} during {}
    """.format(studentName,studentRollNo,profName,roomNo,examDate,timeSlot))

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login('cs18m005@iittp.ac.in', 'arjunkrishna')
        smtp.sendmail('cs18m005@iittp.ac.in', [toAddr], message.as_string())
    roomDetails['nodeID'] = 'mail_invite_invisilation'
    headers = {'Content-type': 'application/json'}
    Thread(target=sendPostRequests, args=(centralEngineSubmitURL,roomDetails,headers)).start()
    #requests.post(url = centralEngineSubmitURL,json = roomDetails, headers=headers)
    return 'success'