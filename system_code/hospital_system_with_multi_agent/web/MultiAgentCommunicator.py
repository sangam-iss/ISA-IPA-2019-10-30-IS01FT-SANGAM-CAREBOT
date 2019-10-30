from osbrain import run_agent,run_nameserver
from web.ManageCalender import ManageCalenderAgent
import json


class MultiAgentSystem:
    def __init__(self, agents):
        self.name_server = run_nameserver()
        self.communicator = run_agent('communicator')
        self.agents = {}
        for agent in agents:
            print(agent)
            self.agents[agent] = run_agent(name=agent, base=ManageCalenderAgent)
            self.communicator.connect(self.agents[agent].get_agent_address(), agent)

    def book_appointment(self, request):
        request['intent'] = 'book'
        self.communicator.send(request['doctor'], json.dumps(request))
        return json.loads(self.communicator.recv(request['doctor']))

    def cancel_appointment(self, request):
        request['intent'] = 'cancel'
        self.communicator.send(request['doctor'], json.dumps(request))
        return json.loads(self.communicator.recv(request['doctor']))

    def check_available_slots(self, request):
        request['intent'] = 'check_available_slot'
        response = {}
        if request.get('doctor',None) is None:
            for agent in self.agents:
                self.communicator.send(agent, json.dumps(request))
                response[agent] = json.loads(self.communicator.recv(agent))
        else:
            self.communicator.send(request['doctor'], json.dumps(request))
            response[request['doctor']] = json.loads(self.communicator.recv(request['doctor']))
        return response
