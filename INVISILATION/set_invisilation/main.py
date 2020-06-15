from flask import Flask
from flask_cors import CORS
import sys


app = Flask(__name__,template_folder = './templates')
app.secret_key = "iittp_set_invisilators"
CORS(app)

sys.path.append("/media/vamsi/Everything else/MTP")

centralEngineSubmitURL = 'http://localhost:2000/wfEngine/submit'

from INVISILATION.set_invisilation.nodes.set_invisilation_register import *
from INVISILATION.set_invisilation.nodes.invite_mail import *
from INVISILATION.set_invisilation.nodes.papers_given_to_profs import *
from INVISILATION.set_invisilation.nodes.ans_sheets_returned import *
from INVISILATION.set_invisilation.nodes.thanks_mail import *
from INVISILATION.set_invisilation.nodes.login import *
from INVISILATION.set_invisilation.nodes.dashboard import *

if __name__ == '__main__':
    app.run(host='localhost',port='3000')
