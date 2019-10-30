import pydialogflow_fulfillment as pf
import json
from datetime import datetime, timedelta
import requests

class Get_failed_appointments:

    def __init__(self,query):
        self.query = query
        self.response = {}

    def handle_intent(self,email):
        print("Handling get_failed_appointments intent")
        parsed_query = pf.DialogflowRequest(self.query)
        #phone_number = parsed_query.get_parameter('phone_number')
        request_url = "https://sangam-test-website.herokuapp.com/get_failed_appointments?email="+str(email)

        failed_appointments = requests.get(request_url)
        print('Failed appointments',failed_appointments.json())
        failed_appointments_json = failed_appointments.json()
        failed_appointments_list = failed_appointments_json['data']
        cards = []
        for appointment in failed_appointments_list:
            tempdict = {}
            tempdict['date'] = appointment['appointment_datetime'].replace('T', ',')
            tempdict['doctor_name'] = appointment['doctor_name']
            tempdict['remarks'] = appointment['symptoms']
            cards.append(tempdict)
        print('cards:', cards)
        print('card length',len(cards))
        aog = pf.dialogflow_response.DialogflowResponse()
        if len(cards) == 0:
            aog.add(pf.SimpleResponse("All your appointments are successfully booked","Hurray!! All your appointments are successfully booked."))
            return aog.get_final_response()

        response_message = "These are your failed appointments\n"
        for card in cards:
            response_message = response_message + "\n------------------------------- \nAppointment Date : "+ str(card['date'])
            response_message = response_message + "\nDoctor : "+ str(card['doctor_name'])
            response_message = response_message + "\nRemarks : "+ str(card['remarks'])

        
        

        

        
        aog.add(pf.SimpleResponse(response_message,"These are your failed appointments"))
        
        return aog.get_final_response()