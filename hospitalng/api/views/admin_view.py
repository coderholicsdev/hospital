'''
view to handle admin dashboard and handling hospital
admin stuff.
'''
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    UpdateAPIView,
    ListAPIView)

# import models
from api.models import Hospital

# serializers
from api.serializers.hospital_serializers import HospitalSerializer

class ViewHospitals(ListAPIView):
    serializer_class = HospitalSerializer
    permission_classes = [IsAuthenticated, ]
    queryset = Hospital.objects.all()

class CreateHospitalPageView(CreateAPIView):
    serializer_class = HospitalSerializer
    permission_classes = [IsAuthenticated, ]

class DeleteHospitalPageView(DestroyAPIView):
    serializer_class = HospitalSerializer
    permission_classes = [IsAuthenticated, ]
    lookup_field = 'hospital_id'
    queryset = Hospital.objects.all()

    def get_queryset(self):
        hospital_id = self.kwargs
        queryset = Hospital.objects.filter(**hospital_id)
        return queryset

class UpdateHospitalPageView(UpdateAPIView):
    serializer_class = HospitalSerializer
    permission_classes = [IsAuthenticated, ]
    lookup_field = 'hospital_id'
    queryset = Hospital.objects.all()
