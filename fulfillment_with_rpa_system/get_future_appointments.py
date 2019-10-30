import pydialogflow_fulfillment as pf
import json
from datetime import datetime, timedelta
import requests

class Get_future_appointments:

    def __init__(self,query):
        self.query = query
        self.response = {}

    def handle_intent(self,email):
        print("Handling get_future_appointments intent")
        parsed_query = pf.DialogflowRequest(self.query)
        #phone_number = parsed_query.get_parameter('phone_number')
        request_url = "http://127.0.0.1:8000/get_future_appointments?email="+str(email)

        future_appointments = requests.get(request_url)
        print('Future appointments',future_appointments.json())
        future_appointments_json = future_appointments.json()
        future_appointments_list = future_appointments_json['data']
        cards = []
        for appointment in future_appointments_list:
            tempdict = {}
            tempdict['date'] = appointment['appointment_datetime'].replace('T', ',')
            tempdict['doctor_name'] = appointment['doctor_name']
            tempdict['remarks'] = appointment['symptoms']
            cards.append(tempdict)
        print('cards:', cards)
        print('card length',len(cards))
        aog = pf.dialogflow_response.DialogflowResponse()
        if len(cards) == 0:
            aog.add(pf.SimpleResponse("You don't have any upcoming appointments","Oops!! Looks like you don't have any upcoming appointments"))
            return aog.get_final_response()

        response_message = "These are your upcoming appointments\n"
        for card in cards:
            response_message = response_message + "\n------------------------------- \nAppointment Date : "+ str(card['date'])
            response_message = response_message + "\nDoctor : "+ str(card['doctor_name'])
            response_message = response_message + "\nRemarks : "+ str(card['remarks'])

        
        

        

        
        aog.add(pf.SimpleResponse(response_message,"These are your upcoming appointments"))
        
        return aog.get_final_response()