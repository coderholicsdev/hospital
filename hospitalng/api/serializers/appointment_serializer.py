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
    doctor = serializers.CharField(source='doctor.name')
    class Meta:
        model = Appointment
        fields = ['appointment_id', 'doctor', 'date', 'time']

class BookAppointmentSerializer(serializers.ModelSerializer):
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
