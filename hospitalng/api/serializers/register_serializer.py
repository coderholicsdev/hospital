'''
Form to handle signup process 
'''
# from django.contrib.auth.forms import UserCreationForm

# import User
from django.contrib.auth import get_user_model

# import serializer from rest_framework
from rest_framework import serializers

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        style={'input_type': 'password'}
    )

    class Meta:
        model = get_user_model()
        fields = ['email', 'first_name', 'last_name', 'password']

    # def validate(self, attrs):
    #     if attrs['password'] != attrs['password2']:
    #         raise serializers.ValidationError('Your passwords don\'t match')
    #     return attrs

    def create(self, validated_data):
        user = self.Meta.model.objects.create(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name = validated_data['last_name'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
        