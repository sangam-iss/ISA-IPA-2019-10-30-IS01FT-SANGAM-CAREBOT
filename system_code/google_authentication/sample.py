from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from oauth2client.client import OAuth2Credentials
from httplib2 import Http
import datetime
from urllib import parse
import requests

airtable_url = "https://api.airtable.com/v0/app4l7uUwpnOQedPM/google-credentials"

params = {
    'api_key': 'keyOrtPlDobjLtiaJ',
    'filterByFormula': "googleid='107111560998788383369'"
}

response = requests.get(airtable_url,params=params)
response = response.json()
if len(response):
    record = response['records'][0]
    field = record['fields']
    credential = OAuth2Credentials.from_json(field['credential'])
    if credential and credential.access_token_expired and credential.refresh_token:
        credential.refresh(Http())
    service = build('calendar', 'v3', credentials=credential)
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('datetime'))
        print(start, event['summary'])
    