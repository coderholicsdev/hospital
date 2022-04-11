'''
serializers for Appointments 
'''
# import date
from datetime import date
# import objectdoesnotexist
from django.core.exceptions import ObjectDoesNotExist

# import User
from django.contrib.auth import get_user_model

# serializers rest_framework
from rest_framework import serializers

# import Response
from rest_framework.response import Response

# import status
from rest_framework import status

# import serializer model 
from api.models import Appointment, DoctorProfile


class AppointmentSerializer(serializers.ModelSerializer):
    '''
    serializer to view appointment used to view
    cancelled schedules, Reschedule, and booked
    appointments
    '''
    doctor = serializers.CharField(source='doctor.name')
    patient = serializers.CharField(source='patient.user.last_name')

    class Meta:
        model = Appointment
        fields = ['appointment_id', 'appointment_status', 'patient', 'doctor', 'date', 'time']

class BookAppointmentSerializer(serializers.ModelSerializer):
    '''
    serializer to help patients book appointments with
    a doctor
    '''
    doctor = serializers.CharField(allow_blank=False, allow_null=False)

    class Meta:
        model = Appointment
        fields = ['doctor', 'date', 'time']
    
    def validate_doctor(self, attrs):
        user = get_user_model().objects.get(email=attrs)
        try:
            doctor = DoctorProfile.objects.get(user=user)
        except ObjectDoesNotExist:
            return Response(
                data={
                    'error': 'This is not a valid Doctor Profile'
                },
                status=status.HTTP_404_NOT_FOUND
            )
        attrs = doctor
        return super().validate(attrs)

    def validate_date(self, attrs):
        today = date.today()
        if attrs < today:
            raise serializers.ValidationError({'error':'You cannot book an appointment a past date.'})
        return super().validate(attrs)

class RescheduleSerializer(serializers.ModelSerializer):
    '''
    serializer to handle Doctor being able to reschedule an
    appointment with a patient.
    '''
    patient = serializers.EmailField(allow_blank=False)
    class Meta:
        model = Appointment
        fields = ['patient', 'date', 'time']
