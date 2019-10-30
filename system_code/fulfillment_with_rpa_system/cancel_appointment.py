import pydialogflow_fulfillment as pf
import json
from datetime import datetime, timedelta, time
import tagui as t
from multiprocessing import Process
import tagui_util as util
import base64
import requests
from oauth2client.client import OAuth2Credentials
from googleapiclient.discovery import build
from httplib2 import Http


def decode_jwt_token(token):
    segments = token.split('.')
    segment = segments[1]
    segment += "=" * ((4 - len(segment) % 4) % 4) #ugh
    user_info = base64.b64decode(segment).decode("utf-8")
    user_info = json.loads(user_info)
    return user_info["email"]

def get_sub_id(token):
    segments = token.split('.')
    segment = segments[1]
    segment += "=" * ((4 - len(segment) % 4) % 4) #ugh
    user_info = base64.b64decode(segment).decode("utf-8")
    user_info = json.loads(user_info)
    return user_info["sub"]

def get_event_json():
    return {
      'summary': 'Checkup Appointment',
      'location': '1E Kent Ridge Rd, Singapore 119228',
      'description': 'Regular checkup appointment.',
      'start': {
        'dateTime': '2015-05-28T09:00:00-07:00',
        'timeZone': 'Asia/Singapore',
      },
      'end': {
        'dateTime': '2015-05-28T17:00:00-07:00',
        'timeZone': 'Asia/Singapore',
      },
      'attendees': [
        {'email': 'lpage@example.com'},
      ],
      'reminders': {
        'useDefault': True
      }
    }

def get_google_credentials(sub_id):
    airtable_url = "https://api.airtable.com/v0/app4l7uUwpnOQedPM/google-credentials"
    api_key = "keyOrtPlDobjLtiaJ"
    params = {
        'api_key': api_key,
        'filterByFormula': "googleid='"+sub_id+"'"
    }
    response = requests.get(airtable_url,params=params)
    response = response.json()
    if response is None:
        return None
    records = response['records']
    if records is None or len(records) <=0:
        return None
    record = records[0]
    field = record['fields']
    credential = OAuth2Credentials.from_json(field['credential'])
    if credential and credential.access_token_expired and credential.refresh_token:
        credential.refresh(Http())
    return credential

def get_events(service,date):
    start_date = datetime.combine(date, time.min)
    end_date = datetime.combine(date, time.max)
    format_start_date = start_date.isoformat() + 'Z'
    format_end_date = end_date.isoformat() + 'Z'
    events_result = service.events().list(calendarId='primary', timeMin=format_start_date,
                                                timeMax=format_end_date,
                                                maxResults=50, singleEvents=True,
                                                orderBy='startTime').execute()
    return events_result.get('items', [])

def cancel_appointment_slot(from_date,token):
    email = decode_jwt_token(token)
    sub_id = get_sub_id(token)
    credential = get_google_credentials(sub_id)
    if credential is None:
        return
    calendar_service = build('calendar','v3',credentials=credential)
    events = get_events(calendar_service,from_date)
    for event in events:
        event_time = event['start']['dateTime'].split('+')[0]
        event_time = event_time.replace('Z','')
        event_time = datetime.strptime(event_time,'%Y-%m-%dT%H:%M:%S')
        if "Pregnancy checkup" in event['summary']:
            calendar_service.events().delete(calendarId='primary',eventId=event['id']).execute()
            break
        



def rpa_process(from_date,phone_number,token):
    t.init()
    t.url("https://sangam-test-website.herokuapp.com/cancel_input")
    util.wait_for_pageload('//button[@id="btnsubmit"]')

    t.click('//input[@id="txtHandNo"]')
    t.type('//input[@name="txtHandNo"]', phone_number)
    t.click('//button[@id="btnsubmit"]')

    util.wait_for_pageload('//button[@id="btnsubmit"]')
    from_date_obj = from_date
    from_date = from_date.strftime("%d/%m/%Y")

    t.click('//label[contains(.,"'+str(from_date)+'")]')
    t.click('//button[@id="btnsubmit"]')
    t.close()

    cancel_appointment_slot(from_date_obj,token)

class Cancel_appointment:

    def __init__(self,query):
        self.query = query
        self.response = {}

    def handle_intent(self,token):
        print("Handling cancel_appointment intent")
        parsed_query = pf.DialogflowRequest(self.query)
        from_date = parsed_query.get_parameter('from_date')
        from_date = datetime.strptime(from_date.split('+')[0], '%Y-%m-%dT%H:%M:%S')
        phone_number = parsed_query.get_parameter('phone_number')
        

        proc = Process(target=rpa_process,args=(from_date,phone_number,token,))
        proc.start()
        
        
        aog = pf.dialogflow_response.DialogflowResponse()
        aog.add(pf.SimpleResponse("Your appointments will be modified successfully","Your appointments will be modified successfully"))
        
        
        return aog.get_final_response()