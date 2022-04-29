'''
Serializer to handle all things Hospital
- Hosital model
- Patients 'MyHospital' Model
'''
# serializers
from rest_framework import serializers

from api.models import MyHospital, Hospital


class HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = '__all__'

class MyHospitalSerializer(serializers.ModelSerializer):
    hospital = serializers.CharField(source='hospital.name')
    class Meta:
        model = MyHospital
        fields = ['hospital', ]