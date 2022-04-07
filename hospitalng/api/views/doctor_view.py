'''
View for doctors appointment logic, etc
'''
from rest_framework.generics import ListAPIView

# import permission
from rest_framework.permissions import IsAuthenticated

# import model
from api.models import DoctorProfile

# import serializer
from api.serializers.doctor_serializer import DoctorProfileSerializer 

class DoctorsDashboard(ListAPIView):
    serializer_class = DoctorProfileSerializer
    permission_classes = [IsAuthenticated, ]
    queryset = DoctorProfile.objects.all()

    def get_queryset(self):
        query = DoctorProfile.objects.filter(user=self.request.user)
        return query
