from django.shortcuts import render
from web.models import Appointment, FailedAppointment
from datetime import datetime
from web.MultiAgentCommunicator import MultiAgentSystem
from django.http import JsonResponse


# Create your views here.
def index(request):
    if 'name' in request.POST:
        name = request.POST.get("name")
        print(name)
    return render(request,'index.html')

def change_input(request):
    if 'txtHandNo' in request.POST:
        number = request.POST.get("txtHandNo")
        print(number)
    return render(request, 'change_input.html')
def cancel_input(request):
    if 'txtHandNo' in request.POST:
        number = request.POST.get("txtHandNo")
        print(number)
    return render(request, 'cancel_input.html')

def cancel_appointment(request):
    if 'txtHandNo' in request.POST:
        txtHandNo = request.POST.get("txtHandNo")
    now = datetime.now()
    patient_appointments = Appointment.objects.all().filter(telephone_mobile=txtHandNo ).filter(appointment_datetime__gte=now).order_by('appointment_datetime')
    patient_appointments = patient_appointments.values_list('id', 'appointment_datetime')
    appointment_string_list = []
    for item in (patient_appointments):
        templist = []
        templist.append(item[0])
        string_date = item[1].strftime("%d/%m/%Y, %H:%M:%S")
        templist.append(string_date)
        appointment_string_list.append(templist)
    return render(request,'make_cancel.html',{'appointments': appointment_string_list})


def add_appointment(request):

    try:
        txtDateTimePicker  =  request.POST.get("txtDateTimePicker")
        print(txtDateTimePicker)  
        ddlHR = request.POST.get("ddlHR")
        ddlMin = request.POST.get("ddlMin")
        datestring = txtDateTimePicker+ ','+ddlHR+':'+ddlMin
        appointment_datetime = datetime.strptime(datestring,'%d/%m/%Y,%H:%M')
        appointment_datetime_calendar = appointment_datetime.strftime('%Y-%m-%dT%H:%M:%S')
        print(appointment_datetime)
        
    except:
        print('Date Time Error')
    if 'txtSpecificDoc' in request.POST:
        txtSpecificDoc = request.POST.get("txtSpecificDoc")
    if 'name' in request.POST:
        name = request.POST.get("name")
        print(name)
    if 'txtCondition' in request.POST:
        txtCondition = request.POST.get("txtCondition")
        
        
        
    m = MultiAgentSystem(['chitra', 'joe', 'padmini', 'helen'])
    calendar_request = {
        'doctor': txtSpecificDoc,
        'date': appointment_datetime_calendar,
        'name': name,
        'message': txtCondition
    }
    calendar_response = m.book_appointment(calendar_request)
    print('Calendar Request :', calendar_request)
    print('Calendar reaponse : ', calendar_response)
    if calendar_response['availability']:
        a = Appointment()
        message = "Appointment added successfully"
    else:
        a = FailedAppointment()
        message = "Sorry!!!! Appointment Unsuccessful. Doctor not available! Try another slot"
    
    
    
    a.appointment_datetime = appointment_datetime
    a.doctor_name = txtSpecificDoc
    a.name = name
    a.symptoms = txtCondition

    
    if 'email' in request.POST:
        email = request.POST.get("email")
        a.email = email
    
    if 'txtCountry' in request.POST:
        txtCountry = request.POST.get("txtCountry")
        a.country = txtCountry
    if 'txtHandNo' in request.POST:
        txtHandNo = request.POST.get("txtHandNo")
        a.telephone_mobile = txtHandNo
    if 'txtHomeNo' in request.POST:
        txtHomeNo = request.POST.get("txtHomeNo")
        a.telephone_home = txtHomeNo
    if 'txtOfficeNo' in request.POST:
        txtOfficeNo = request.POST.get("txtOfficeNo")
        a.telephone_office = txtOfficeNo
    if 'txtFaxNo' in request.POST:
        txtFaxNo = request.POST.get("txtFaxNo")
        a.fax_number = txtFaxNo
    if 'ddlInstitution' in request.POST:
        ddlInstitution = request.POST.get("ddlInstitution")
        a.institution = ddlInstitution
    
    if 'txtRemarks' in request.POST:
        txtRemarks = request.POST.get("txtRemarks")
        a.remarks = txtRemarks
    
        
    
    
    a.save()
    return render(request,'appointment_successful.html',{'message': message}) 

def change_appointment(request):
    if 'txtHandNo' in request.POST:
        txtHandNo = request.POST.get("txtHandNo")
    now = datetime.now()
    patient_appointments = Appointment.objects.all().filter(telephone_mobile=txtHandNo).filter(appointment_datetime__gte=now).order_by('appointment_datetime')
    
    patient_appointments = patient_appointments.values_list('id', 'appointment_datetime')
    appointment_string_list = []
    for item in (patient_appointments):
        templist = []
        templist.append(item[0])
        string_date = item[1].strftime("%d/%m/%Y, %H:%M:%S")
        templist.append(string_date)
        appointment_string_list.append(templist)
        
    return render(request,'make_change.html',{'appointments': appointment_string_list})

def make_change(request):
    if 'date_id' in request.POST:
        date_id = request.POST.get("date_id")
        print('date_id is ', date_id)
    patient_appointment = Appointment.objects.all().filter(id=date_id)
    try:
        txtDateTimePicker  =  request.POST.get("txtDateTimePicker")
        print(txtDateTimePicker)  
        ddlHR = request.POST.get("ddlHR")
        ddlMin = request.POST.get("ddlMin")
        datestring = txtDateTimePicker+ ','+ddlHR+':'+ddlMin
        appointment_datetime = datetime.strptime(datestring,'%d/%m/%Y,%H:%M')
        print(appointment_datetime)
        patient_appointment.update(appointment_datetime = appointment_datetime)
        patient_appointment.save()
    except:
        print('Date Time Error')
    
    return render(request,'change_successful.html' )

def make_cancel(request):
    if 'date_id' in request.POST:
        date_id = request.POST.get("date_id")
        print('date_id is ', date_id)
    Appointment.objects.filter(id=date_id).delete()
    
    return render(request,'cancel_successful.html' )
def get_failed_appointments(request):
    now = datetime.now()
    if 'email' in request.GET:
        email = request.GET.get('email')
    failed_appointments = FailedAppointment.objects.all().filter(email=email).filter(appointment_datetime__gte=now).values()
    print('handling get request')
    print(failed_appointments)
    return JsonResponse({'data':list(failed_appointments)},safe=False)

def get_future_appointments(request):
    now = datetime.now()
    if 'email' in request.GET:
        email = request.GET.get('email')
    failed_appointments = Appointment.objects.all().filter(email=email).filter(appointment_datetime__gte=now).values()
    print('handling get request')
    print(failed_appointments)
    return JsonResponse({'data':list(failed_appointments)},safe=False)