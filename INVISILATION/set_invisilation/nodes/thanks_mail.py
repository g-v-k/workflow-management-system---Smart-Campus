from INVISILATION.set_invisilation.main import app, centralEngineSubmitURL
from flask import request
from threading import Thread
from email.message import EmailMessage
import requests, smtplib


def sendPostRequests(url,jsonData, headers):
    requests.post(url = url,json = jsonData, headers=headers)


@app.route('/set_invisilation/thanks_mail_invisilation', methods=['POST'])
def thanksMailInvisilation():
    jsonInfo = request.json
    fromAddr = 'cs18m005@iittp.ac.in'
    toAddr = 'cs18m005@iittp.ac.in'

    message = EmailMessage()
    message['Subject'] = "Invisilation Duty"
    message['From'] = fromAddr
    message['To'] = toAddr
    message.set_content("""\
    Dear sir/madam,
         We thank you for your time and effort for carrying out the invisilation duty.
    """)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    
        smtp.login('cs18m005@iittp.ac.in', 'arjunkrishna')
        smtp.sendmail('cs18m005@iittp.ac.in', [toAddr], message.as_string())
    
    paramData= {'nodeID':'thanks_mail_invisilation','wfID':jsonInfo['wfID'],'jobID':jsonInfo['jobID']}
    headers = {'Content-type': 'application/json'}
    Thread(target=sendPostRequests, args=(centralEngineSubmitURL,paramData,headers)).start()
    #requests.post(url = centralEngineSubmitURL,json = paramData, headers=headers)
    return 'success'