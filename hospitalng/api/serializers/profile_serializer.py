from rest_framework import serializers

# import models
from api.models import PatientProfile, DoctorProfile, AdminProfile

class PatientProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientProfile
        exclude = ['user',]

class DoctorProfileSerailizer(serializers.ModelSerializer):
    class Meta:
        model = DoctorProfile
        exclude = ['user',]

class AdminProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminProfile
        exclude = ['user']
