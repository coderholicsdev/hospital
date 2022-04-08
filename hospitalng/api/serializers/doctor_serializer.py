'''
Serializer to handle doctor profile
'''
from rest_framework import serializers

# import doctorprofile
from api.models import DoctorProfile

class DoctorProfileSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.email", read_only=True)
    hospital_name = serializers.CharField(source='hospital_name.name', read_only=True)

    class Meta:
        model = DoctorProfile
        fields = ['user', 'name', 'phone_number', 'qualifications', 'specialty_or_department', 'title', 'hospital_name', 'profile_picture']
