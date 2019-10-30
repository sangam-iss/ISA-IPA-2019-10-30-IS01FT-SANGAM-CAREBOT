from django.db import models

class Appointment(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    symptoms = models.TextField()
    country = models.CharField(max_length=50)
    telephone_mobile = models.CharField(max_length=10)
    telephone_home = models.CharField(max_length=10)
    telephone_office = models.CharField(max_length=10)
    fax_number = models.CharField(max_length=10)
    appointment_datetime = models.DateTimeField()
    institution = models.CharField(max_length=50)
    doctor_name = models.CharField(max_length=100)
    remarks = models.CharField(max_length=200)

class FailedAppointment(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    symptoms = models.TextField()
    country = models.CharField(max_length=50)
    telephone_mobile = models.CharField(max_length=10)
    telephone_home = models.CharField(max_length=10)
    telephone_office = models.CharField(max_length=10)
    fax_number = models.CharField(max_length=10)
    appointment_datetime = models.DateTimeField()
    institution = models.CharField(max_length=50)
    doctor_name = models.CharField(max_length=100)
    remarks = models.CharField(max_length=200)