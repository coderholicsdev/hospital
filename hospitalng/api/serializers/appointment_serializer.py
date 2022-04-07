'''
serializers for Appointments 
'''
from rest_framework import serializers

# import serializer model 
from api.models import Appointment


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['appointment_id', 'created_by', 'appointment_date_time']

class BookAppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['apointment_with', ]