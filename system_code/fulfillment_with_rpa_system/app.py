from flask import Flask,render_template
from flask import request,jsonify
import pydialogflow_fulfillment as pf
from book_appointment import Book_appointment
from get_doctor_name import Get_doctor_name
from change_appointment import Change_appointment
from cancel_appointment import Cancel_appointment
from get_failed_appointments import Get_failed_appointments
from get_future_appointments import Get_future_appointments
import json
import base64

app = Flask(__name__)

attraction_db = None

def decode_jwt_token(token):
    segments = token.split('.')
    segment = segments[1]
    segment += "=" * ((4 - len(segment) % 4) % 4) #ugh
    user_info = base64.b64decode(segment).decode("utf-8")
    user_info = json.loads(user_info)
    return user_info["email"]

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
    if originalDetectIntentRequest is not None:
        payload = originalDetectIntentRequest.get('payload',None)
        if payload is not None:
            user = payload.get('user',None)
            if user is not None:
                userVerificationStatus = user.get('idToken',None)
                if userVerificationStatus is not None:
                    isUserVerified = True
                    idToken = userVerificationStatus
    if isUserVerified is False:
        data = "Hi! To serve you better we need access to some of your information. Do you want to proceed?"
        dialogflow_response.add(pf.SimpleResponse(data,data))
    else:
        
        print("\nuser_details\n")
        
        data = "Hello! welcome to CareBot. Ask your queries."
        dialogflow_response.add(pf.SimpleResponse(data,data))
    return dialogflow_response.get_final_response()

def ask_for_calendar_permsision(req):
    ff_response = pf.dialogflow_response.DialogflowResponse()
    response = "https://iss-carebot.herokuapp.com/calendar/permission"
    ff_response.add(pf.SimpleResponse(response,"Please allow access by signin using the link"))
    card = {
            "basicCard": {
              "title": "Give Permission",
              "formatted_text": "Please give google calendar permission for us to manage your calendar",
              "buttons": [
                {
                  "title": "sign-in",
                  "openUrlAction": {
                    "url": "https://iss-carebot.herokuapp.com/calendar/permission"
                  }
                }
              ]
            }
          }
    ff_response.rich_response['items'].append(card)
    ff_response.google_payload['richResponse'] = ff_response.rich_response
    ff_response.add(pf.LinkOutSuggestion("Sign-in",response))
    return ff_response.get_final_response()
    

def make_default_response(response):
    ff_response = pf.dialogflow_response.DialogflowResponse()
    ff_response.add(pf.SimpleResponse(response,response))
    return ff_response.get_final_response()


def make_error_response(code):
    response = f"Sorry ! unable to process your request! Error - {code}"
    return make_default_response(response)


# @app.before_first_request
# def get_database():
#     global attraction_db
#     with open('tourist_data_clean.json') as fh:
#         attraction_db = json.load(fh)
#     print(attraction_db[0])

@app.route('/calendar/permission')
def render_calendar_permission():
    return render_template('permission.html')

@app.route('/calendar/storeauthcode', methods = ['POST'])
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
    return req

@app.route('/v1/carebot/',methods=['POST'])
def intent_resolver():
    req = request.get_json()
    originalDetectIntentRequest = req.get('originalDetectIntentRequest',None)
    idToken = None
    email = None
    if originalDetectIntentRequest is not None:
        payload = originalDetectIntentRequest.get('payload',None)
        if payload is not None:
            user = payload.get('user',None)
            if user is not None:
                idToken = user.get('idToken',None)
    if idToken is not None:
        email = decode_jwt_token(idToken)
    print("\n\n")
    print(req)
    print("\n\n")
    query = req.get('queryResult',None)
    if query is None:
        return jsonify(make_error_response("Query Result is Empty"))
    intent = query.get('intent')
    if intent is None:
        return jsonify(make_error_response("intent is Empty"))
    intent_name = intent.get("displayName", "defaultResponse")

    if intent_name == "book_appointment":
        intent_handler = Book_appointment(json.dumps(req))
        response = intent_handler.handle_intent()
    elif intent_name == "get_doctor_name_and_preferred_time":
        originalDetectIntentRequest = req.get('originalDetectIntentRequest',None)
        if originalDetectIntentRequest is not None:
            payload = originalDetectIntentRequest.get('payload',None)
            if payload is not None:
                user = payload.get('user',None)
                if user is not None:
                    idToken = user.get('idToken',None)
        intent_handler = Get_doctor_name(json.dumps(req) )
        response = intent_handler.handle_intent(idToken)
    elif intent_name == "change_appointment_to_date":
        intent_handler = Change_appointment(json.dumps(req))
        response = intent_handler.handle_intent(idToken)
    elif intent_name == "cancel_appointment":
        intent_handler = Cancel_appointment(json.dumps(req))
        response = intent_handler.handle_intent(idToken)
    elif intent_name == "AskPermission":
        response = ask_permission(req)
    elif intent_name == "Welcome":
        response = welcomeIntent(req)
    elif intent_name == "get_failed_appointments":
        intent_handler = Get_failed_appointments(json.dumps(req))
        response = intent_handler.handle_intent(email)
    elif intent_name == "get_future_appointments":
        intent_handler = Get_future_appointments(json.dumps(req))
        response = intent_handler.handle_intent(email)
    elif intent_name == "askCalendarPermission":
        response = ask_for_calendar_permsision(json.dumps(req))

    else:
        response = make_default_response("Intent Matching Failed, Can you please rephrase the question")
    print("\n\n")
    print(response)
    print("\n\n")
    return response

@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
