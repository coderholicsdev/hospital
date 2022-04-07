from rest_framework import serializers

# import models
from api.models import PatientProfile, DoctorProfile, AdminProfile


class ProfileSerializerMixin(serializers.ModelSerializer):
    def validate(self, validated_data):
        user = validated_data.get('user')
        try:
            self.Meta.model.objects.create(user=user)
        except:
            raise serializers.ValidationError('User with this account exists already')
        return super().validate(validated_data)

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
