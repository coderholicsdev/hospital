'''
Serializer to handle doctor profile
'''
from rest_framework import serializers

# import doctorprofile
from api.models import DoctorProfile

class DoctorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorProfile
        fields = ['name', 'phone_number', 'qualifications', 'specialty_or_department', 'title', 'hospital_name', 'profile_picture']
