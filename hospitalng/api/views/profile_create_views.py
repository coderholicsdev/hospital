'''
View to handle ther creation of profiles for 
- Patient
- Doctor
- Admin
'''
# import IntegrityError
from django.db import IntegrityError

# import rest_framework's CreateAPIView
from rest_framework.generics import CreateAPIView

# authentication classes
from rest_framework.permissions import IsAuthenticated

# import response, status
from rest_framework.response import Response
from rest_framework import status 


# serializer
from api.serializers.profile_serializer import PatientProfileSerializer, DoctorProfileSerailizer, AdminProfileSerializer


class CreateAPIViewAuthenticationMixin(CreateAPIView):
    permission_classes = [IsAuthenticated, ]

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except IntegrityError:
            return Response({'error': 'A profile already exists for this User'}, 
            status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        # override pefrom_create to include the user
        # in save.
        serializer.save(user=self.request.user)
        return serializer

class CreatePatientProfileView(CreateAPIViewAuthenticationMixin):
    serializer_class = PatientProfileSerializer

class CreateDoctorProfileView(CreateAPIViewAuthenticationMixin):
    serializer_class = DoctorProfileSerailizer

class CreateAdminProfileView(CreateAPIViewAuthenticationMixin):
    serializer_class = AdminProfileSerializer

