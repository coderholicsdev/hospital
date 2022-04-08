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
from api.models import Appointment


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['appointment_id', 'created_by', 'date', 'time']

class BookAppointmentSerializer(serializers.ModelSerializer):
    appointment_with = serializers.CharField(allow_blank=False, allow_null=False)
    class Meta:
        model = Appointment
        fields = ['appointment_with', 'date', 'time']
    
    def validate_appointment_with(self, attrs):
        try:
            user = get_user_model().objects.get(email=attrs)
        except ObjectDoesNotExist:
            return Response(
                data={
                    'error': 'This user does not exist, try a different one'
                },
                status=status.HTTP_404_NOT_FOUND
            )
        attrs = user
        return super().validate(attrs)

    def validate_date(self, attrs):
        today = date.today()
        if attrs < today:
            raise serializers.ValidationError({'error':'You cannot book an appointment a past date.'})
        return super().validate(attrs)
