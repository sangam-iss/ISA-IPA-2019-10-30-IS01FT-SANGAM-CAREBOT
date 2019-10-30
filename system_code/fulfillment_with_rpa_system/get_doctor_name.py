import pydialogflow_fulfillment as pf
import json
from datetime import datetime, timedelta
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
        return
    records = response['records']
    if records is None or len(records) <=0:
        return
    record = records[0]
    field = record['fields']
    credential = OAuth2Credentials.from_json(field['credential'])
    if credential and credential.access_token_expired and credential.refresh_token:
        credential.refresh(Http())
    return credential


def book_calendar_slot(future_appointments,sub_id):
    credential = get_google_credentials(sub_id)
    calendar_service = build('calendar','v3',credentials=credential)
    event = get_event_json()
    for appointment in future_appointments:
        print("blocking calendar for date "+appointment['appointment_datetime'])
        appointment_date_string = appointment['appointment_datetime']
        appointment_date = datetime.strptime(appointment_date_string,"%Y-%m-%dT%H:%M:%S")
        event['summary'] = appointment["symptoms"]
        event['description'] = appointment["symptoms"]
        event['start']['dateTime'] = appointment['appointment_datetime']+"+08:00"
        end_date = appointment_date + timedelta(minutes=30)
        event['end']['dateTime'] = end_date.strftime("%Y-%m-%dT%H:%M:%S") + "+08:00"
        calendar_service.events().insert(calendarId='primary',body=event).execute()


def rpa_process(lmp_date,doctor_name,preferred_time,phone_number,patient_name,symptoms,email,sub_id):
        hour = preferred_time.hour
        minute = preferred_time.minute
        checkup_dates=[]
        day_list = [45,75,105,135,165,195,210,225,240,255,262,269,275,280]
        week_list = [6,10,14,18,22,26,28,30,32,34,36,37,38,39]
        for day in day_list:
            checkup = lmp_date + timedelta(days=day)
            checkup = str(checkup.day) + "/" + str(checkup.month) + "/" + str(checkup.year)
            checkup_dates.append(checkup)
        t.init()
        
        for index,i in enumerate(checkup_dates):

            t.url("http://127.0.0.1:8000/")
            util.wait_for_pageload('//button[@id="btnsubmit"]')

            t.click('//input[@class="form-control"]')
            t.type('//input[@name="name"]', patient_name)

            t.click('//input[@id="email"]')
            t.type('//input[@name="email"]', email)

            symptoms = "Pregnancy checkup after week "+str(week_list[index])

            t.type('//textarea', symptoms)

            t.click('//input[@id="txtHandNo"]')
            t.type('//input[@name="txtHandNo"]', phone_number)

            t.click('//div[@class="filter-option-inner-inner"]')
            t.click('//a[@role= "option"][.='+str(hour)+']')
            t.click('//select[@id="ddlMin"]')
            t.click('//a[@role= "option"][.='+str(minute)+']')

            t.click('//input[@name="txtDateTimePicker"]')
            t.type('//input[@name="txtDateTimePicker"]', i)

            t.click('//select[@id="txtSpecificDoc"]')
            t.click('//a[@role= "option"][.="'+str(doctor_name)+'"]')

            t.click('//button[@id="btnsubmit"]')
        
        t.close()
        request_url = "http://127.0.0.1:8000/get_future_appointments?email="+str(email)
        future_appointments = requests.get(request_url)
        book_calendar_slot(future_appointments.json()['data'],sub_id)



class Get_doctor_name:
    def __init__(self,query):
        self.query = query
        self.response = {}

    def handle_intent(self, idToken):
        print("Handling Get_doctor_name intent")

        

        parsed_query = pf.DialogflowRequest(self.query)
        output_context = parsed_query.get_single_ouputcontext('book_appointment')
        output_parameters = output_context.get('parameters',None)
        lmp_date = output_parameters['lmp_date']
        lmp_date = datetime.strptime(lmp_date.split('+')[0], '%Y-%m-%dT%H:%M:%S')

        #Generate checkup dates
        

        phone_number = output_parameters['phone_number']
        patient_name = output_parameters['patient_name']

        doctor_name = parsed_query.get_parameter('doctor_name')
        doctor_name = doctor_name['name']
        preferred_time = parsed_query.get_parameter('preferred_time')
        preferred_time = datetime.strptime(preferred_time.split('+')[0], '%Y-%m-%dT%H:%M:%S')

        symptoms = 'pregnancy checkup'
        
                    
        email = decode_jwt_token(idToken)
        proc = Process(target=rpa_process,args=(lmp_date,doctor_name,preferred_time,phone_number,patient_name,symptoms,email,get_sub_id(idToken),))
        proc.start()

        aog = pf.dialogflow_response.DialogflowResponse()
        aog.add(pf.SimpleResponse("Your appointments will be booked successfully","Your appointments will be booked successfully"))
        return aog.get_final_response() 