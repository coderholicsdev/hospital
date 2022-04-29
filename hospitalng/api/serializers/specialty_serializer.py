from rest_framework import serializers
from api.models import Specialty

class AddSpecialtySerializer(serializers.ModelSerializer):
    '''
    serializer to add doctor specialty
    '''
    class Meta:
        model = Specialty
        fields = ['title']

class ViewSpecialtySerializer(serializers.ModelSerializer):
    '''
    serializer to view the Specialty title and slug
    '''
    class Meta:
        model = Specialty
        fields = ['title', 'slug']

