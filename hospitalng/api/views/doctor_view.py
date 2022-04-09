'''
View for doctors appointment logic, etc
'''
from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response

# import permission
from rest_framework.permissions import IsAuthenticated

# import model
from api.models import DoctorProfile

# import serializer
from api.serializers.doctor_serializer import DoctorProfileSerializer
from api.serializers.appointment_serializer import RescheduleSerializer

# import mixin
from .patient_view import AppointmentsStatusMixin

class DoctorsDashboard(ListAPIView):
    serializer_class = DoctorProfileSerializer
    permission_classes = [IsAuthenticated, ]
    queryset = DoctorProfile.objects.all()

    def get_queryset(self):
        query = DoctorProfile.objects.filter(user=self.request.user)
        return query

class DoctorsAppointmentMixin(AppointmentsStatusMixin):
    model_profile = DoctorProfile

    def appointment_kwargs(self, **kwargs):
        doctor = self.user_doc_patient_check()
        kwargs['doctor'] = doctor
        return kwargs

class DoctorBookedAppointments(DoctorsAppointmentMixin):
    appointment_status = 'Booked'

class DoctorCancelledAppointment(DoctorsAppointmentMixin):
    # Get all the appointment
    appointment_status = 'Cancelled'

class DoctorRescheduledAppointments(DoctorsAppointmentMixin):
    appointment_status = 'Rescheduled'


class RescheduleAppointmentWithPatient(GenericAPIView):
    serializer_class = RescheduleSerializer

    def post(self, request, appointment_id, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            print(appointment_id)
            return Response(
                data={'info': serializer.data}
            )
        return Response(data=serializer.errors, status=400)