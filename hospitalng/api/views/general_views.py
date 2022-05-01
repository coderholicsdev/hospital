from rest_framework.response import Response
from rest_framework.generics import ListAPIView

# import models
from api.models import Hospital

# import serializers
from api.serializers.hospital_serializers import HospitalSerializer

class ListAllHospitals(ListAPIView):
    queryset = Hospital.objects.all()
    serializer_class = HospitalSerializer