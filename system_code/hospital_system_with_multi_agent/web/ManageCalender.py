from osbrain.agent import Agent
import pickle
from datetime import datetime,timedelta, time
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import json


class ManageCalenderAgent(Agent):

    EVENT = {
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

    def __init__(self, name='', host=None, serializer=None, transport=None,
                 attributes=None):
        super().__init__(name=name, host=host, serializer=serializer, transport=transport,
                         attributes=attributes)
        self.credentials = None
        self.service = None
        self.name = name
        self.agent_address = self.bind('REP', alias=name, handler=self.handle_request)

    def handle_request(self, request):
        req = json.loads(request)
        self.refresh_credentials()
        self.get_calendar_service()

        if req['intent'] == 'book':
            date = datetime.strptime(req['date'], '%Y-%m-%dT%H:%M:%S')
            response = self.book_slots(date, req['name'], req['message'])
            response['status'] = 200
        elif req['intent'] == 'check_available_slot':
            date = datetime.strptime(req['date'], '%Y-%m-%dT%H:%M:%S')
            response = self.check_available_slots(date)
            response['status'] = 200
        elif req['intent'] == 'cancel':
            date = datetime.strptime(req['date'], '%Y-%m-%dT%H:%M:%S')
            response = self.cancel_event(date)
            response['status'] = 200
        else:
            response = {
                'status': 401,
                'message': "Unknown Request"
            }
        return json.dumps(response)

    def get_agent_address(self):
        return self.agent_address

    def refresh_credentials(self):
        credential_file = self.name+".pickle"
        print(credential_file)
        with open(credential_file, 'rb') as token:
            creds = pickle.load(token)
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        with open(credential_file, 'wb') as token:
            pickle.dump(creds, token)
        self.credentials = creds

    def get_calendar_service(self):
        self.service = build('calendar', 'v3', credentials=self.credentials)

    def get_doctor_availability(self,message):
        pass

    def get_events(self,date):
        assert isinstance(date,datetime)

        start_date = datetime.combine(date.date(), time.min)
        end_date = datetime.combine(date.date(), time.max)
        format_start_date = start_date.isoformat() + 'Z'
        format_end_date = end_date.isoformat() + 'Z'
        events_result = self.service.events().list(calendarId='primary', timeMin=format_start_date,
                                                   timeMax=format_end_date,
                                                   maxResults=50, singleEvents=True,
                                                   orderBy='startTime').execute()
        return events_result.get('items', [])

    def check_available_slots(self, date):
        assert isinstance(date, datetime)
        response = {
            'availability':True,
            'slots':[]
        }
        booked_slots = []

        start_date = datetime.combine(date.date(), time.min)
        end_date = datetime.combine(date.date(), time.max)
        slot_start_date = start_date.replace(hour=7, minute=0, second=0, microsecond=0)
        slot_end_date = end_date.replace(hour=23, minute=0, second=0, microsecond=0)

        events_result = self.service.events().list(calendarId='primary', timeMin=start_date.isoformat() + 'Z',
                                                   timeMax=end_date.isoformat() + 'Z',
                                                   maxResults=50, singleEvents=True,
                                                   orderBy='startTime').execute()
        events = events_result.get('items', [])
        if not events:
            return response
        for event in events:
            slot={}
            appointment_start = event['start']['dateTime'].split('+')[0]
            appointment_start = appointment_start.replace('Z','')
            appointment_end = event['end']['dateTime'].split('+')[0]
            appointment_end = appointment_end.replace('Z','')
            slot['start'] = datetime.strptime(appointment_start, '%Y-%m-%dT%H:%M:%S')
            slot['end'] = datetime.strptime(appointment_end, '%Y-%m-%dT%H:%M:%S')
            if slot['start'] == date:
                response['availability'] = False
            booked_slots.append(slot['start'])
        print(booked_slots)
        while slot_start_date < slot_end_date:
            if slot_start_date not in booked_slots:
                response['slots'].append(slot_start_date.strftime('%Y-%m-%dT%H:%M:%S'))
            slot_start_date += timedelta(minutes=30)
        return response

    def book_slots(self, date, name, message):
        assert isinstance(date, datetime)
        available_slots = self.check_available_slots(date)

        if available_slots['availability'] is True:
            event = ManageCalenderAgent.EVENT
            event['summary'] = 'Appointment with '+name
            event['description'] = message
            event['start']['dateTime'] = date.strftime('%Y-%m-%dT%H:%M:%S')+'+08:00'
            date += timedelta(minutes=30)
            event['end']['dateTime'] = date.strftime('%Y-%m-%dT%H:%M:%S') + '+08:00'
            self.service.events().insert(calendarId='primary', body=event).execute()

        return available_slots

    def cancel_event(self, date):
        assert isinstance(date, datetime)
        response = {
            'cancelled': False
        }

        events = self.get_events(date)
        for event in events:
            event_time = event['start']['dateTime'].split('+')[0]
            event_time = datetime.strptime(event_time, '%Y-%m-%dT%H:%M:%S')
            if date == event_time:
                self.service.events().delete(calendarId='primary', eventId=event['id']).execute()
                response['cancelled'] = True
                break
        return response
