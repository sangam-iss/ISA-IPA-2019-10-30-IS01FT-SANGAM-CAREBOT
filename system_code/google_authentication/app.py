from flask import Flask,render_template
from oauth2client import client
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from flask import request,jsonify
import json
import pydialogflow_fulfillment as pf
import base64
import requests
flaskapp = Flask(__name__)

def decode_jwt_token(token):
    segments = token.split('.')
    segment = segments[1]
    segment += "=" * ((4 - len(segment) % 4) % 4) #ugh
    user_info = base64.b64decode(segment).decode("utf-8") 
    print(user_info)
    user_info = json.loads(user_info)
    print(user_info["email"])
    for segment in segments:
        segment += "=" * ((4 - len(segment) % 4) % 4) #ugh
        string = base64.b64decode(segment)
        print(string)

def ask_permission(request):
    req = pf.DialogflowRequest(json.dumps(request))
    dialogflow_response = pf.DialogflowResponse()
    dialogflow_response.add(pf.AskForSignin())
    dialogflow_response.dialogflow_response.pop("fulfillmentText")
    dialogflow_response.dialogflow_response.pop("source")   
    return dialogflow_response.get_final_response()

def welcomeIntent(request):
    isUserVerified = False
    idToken = None
    dialogflow_response = pf.DialogflowResponse()
    originalDetectIntentRequest = request.get('originalDetectIntentRequest',None)
    if originalDetectIntentRequest:
        payload = originalDetectIntentRequest.get('payload',None)
        if payload:
            user = payload.get('user',None)
            if user:
                userVerificationStatus = user.get('userVerificationStatus',"NO")
                if userVerificationStatus == "VERIFIED":
                    isUserVerified = True
                    idToken = user['idToken']
    if isUserVerified is False:
        data = "Hi! I can show you examples of helper intents. We recommend trying this sample on a phone so you can see all helper intents."
        dialogflow_response.add(pf.SimpleResponse(data,data))
    else:
        
        print("\nuser_details\n")
        decode_jwt_token(idToken)
        data = "Hello! welcome to CareBot. Ask your queries."
        dialogflow_response.add(pf.SimpleResponse(data,data))
    return dialogflow_response.get_final_response()

@flaskapp.route('/calendar/permission')
def render_calendar_permission():
    return render_template('permission.html')

@flaskapp.route('/')
def index_app():
    return "Hello Application - index file !!"

@flaskapp.route('/calendar/storeauthcode', methods = ['POST'])
def store_auth_code():
    req = request.get_data()
    CLIENT_SECRET_FILE = 'credentials.json'
    credentials = client.credentials_from_clientsecrets_and_code(
    CLIENT_SECRET_FILE,
    ['https://www.googleapis.com/auth/calendar', 'https://www.googleapis.com/auth/calendar.events'],
    req)

    airtable_url = "https://api.airtable.com/v0/app4l7uUwpnOQedPM/google-credentials"
    api_key = "keyOrtPlDobjLtiaJ"
    cred = json.loads(credentials.to_json())
    response = {'records': [{
        'fields': {
        'googleid':cred['id_token']['sub'],    
        'credential':json.dumps(cred)
        }}
    ]}
    headers = {
        'Authorization': 'Bearer '+api_key,
        'Content-Type': 'application/json'
    }
    airtable_response = requests.post(airtable_url, data = json.dumps(response), headers = headers)
    print(airtable_response.status_code)
    print(airtable_response.text)
    return req

@flaskapp.route('/v1/hello',methods=['POST'])
def hello():
    req = request.get_json()
    print(req)
    if req['queryResult']['intent']['displayName'] == "AskPermission":
        response = ask_permission(req)
    elif req['queryResult']['intent']['displayName'] == "Welcome":
        response = welcomeIntent(req)
    print("\n\n")
    print(response)
    print("\n\n")
    return response


if __name__ == '__main__':
    flaskapp.run()
