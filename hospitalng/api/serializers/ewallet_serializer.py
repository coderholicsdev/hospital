'''
Serializers for Patient Ewallet
account funding and displaying Ewallet Information
'''
from rest_framework import serializers

from api.models import Ewallet

class FundAccountSerializer(serializers.ModelSerializer):
    '''
    serializer to handle Funding account of the Patients 
    Ewallet account
    '''
    class Meta:
        model = Ewallet
        fields = ['amount', ]

class EwalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ewallet
        fields = '__all__'