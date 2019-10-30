import pydialogflow_fulfillment as pf
import json
from datetime import datetime, timedelta

class Book_appointment:

    def __init__(self,query):
        self.query = query
        self.response = {}

    def handle_intent(self):
        print("Handling book_appointment intent")
        parsed_query = pf.DialogflowRequest(self.query)
        lmp_date = parsed_query.get_parameter('lmp_date')
        lmp_date = datetime.strptime(lmp_date.split('+')[0], '%Y-%m-%dT%H:%M:%S')

        #Generate checkup dates
        checkup_dates=[]
        day_list = [45,75,105,135,165,195,210,225,240,255,262,269,275,280]
        for day in day_list:
            checkup = lmp_date + timedelta(days=day)
            checkup = str(checkup.day) + "/" + str(checkup.month) + "/" + str(checkup.year)
            checkup_dates.append(checkup)
        doctor_names = ['Chitra Mattar','Joe Stephie','Padmini Ramesh','Helen Cho']

        dates_string = '\n'.join(checkup_dates)
        dates_string = 'Checkup Dates \n'+ dates_string +'\n Please choose your preferred Doctor.'

        aog = pf.dialogflow_response.DialogflowResponse()
        aog.add(pf.SimpleResponse(dates_string,"These are your checkup dates. Please choose your preferred Doctor."))
        aog.add(pf.Suggestions(doctor_names))
        return aog.get_final_response()