'''
Serializer to handle all things Hospital
- Hosital model
- Patients 'MyHospital' Model
'''
# serializers
from rest_framework import serializers

from api.models import MyHospital


class MyHospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyHospital
        fields = ['hospital', ]