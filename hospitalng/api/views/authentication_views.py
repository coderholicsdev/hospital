'''
This view handles all things authentication 
(registration, login, ChangePassword, etc)
'''
from rest_framework.generics import CreateAPIView, GenericAPIView

# import response
from rest_framework.response import Response

# import authentication
from rest_framework.permissions import AllowAny

# import serializer
from api.serializers.register_serializer import RegisterSerializer

class RegisterView(CreateAPIView):
    permission_classes = []
    serializer_class = RegisterSerializer

    def get(self, request, *args, **kwargs):
        return Response({
            'success': 'Welcome to the Registration page.'
        })
