'''
View for doctors appointment logic, etc
'''

# django exceptions
from django.core.exceptions import ObjectDoesNotExist

# rest_framework stuff
from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response

# import permission
from rest_framework.permissions import IsAuthenticated

# import model
from api.models import DoctorProfile, Appointment

# import serializer
from api.serializers.doctor_serializer import DoctorProfileSerializer
from api.serializers.appointment_serializer import RescheduleSerializer
from api.serializers.appointment_serializer import AppointmentSerializer

# import mixin
from .patient_view import AppointmentsStatusMixin

# import packages
from api.packages.converterv2 import TodaysDate, OtherDateFilters

class DoctorsDashboard(ListAPIView):
    # Dashboard to view doctors profile
    serializer_class = DoctorProfileSerializer
    permission_classes = [IsAuthenticated, ]
    queryset = DoctorProfile.objects.all()

    def get_queryset(self):
        query = DoctorProfile.objects.filter(user=self.request.user)
        return query

class DoctorsAppointmentMixin(AppointmentsStatusMixin):
    '''
    Reusable mixin to override appointment_kwargs from AppointmentsStatusMixin
    '''
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
            try:
                appointment = Appointment.objects.get(appointment_id=appointment_id)
            except ObjectDoesNotExist:
                return Response(
                    {'error': 'this appointment ID does not exist'},
                    status=404
                )
            # check if this appointment belongs to the logged in doctor
            if appointment.doctor.user != request.user:
                return Response(
                    {
                        'error':  'Sorry this appointment is not booked for you'
                    },
                    status=403
                )

            # change appointment status
            try:
                doctor = DoctorProfile.objects.get(user=request.user)
            except ObjectDoesNotExist:
                return Response(
                    data={
                        'error': 'Sorry you do not have authorization to view this page'
                    }, 
                    status=403
                )
            Appointment.objects.filter(doctor=doctor).update(appointment_status='Rescheduled')

            return Response(
                data={
                    'success':'Appointment successfully Rescheduled',
                    'info': serializer.data
                    }
            )
        # serializer errors
        return Response(data=serializer.errors, status=400)

class AllAppointmentsDashboard(GenericAPIView):
    '''
    view to handle doctor viewing all appointments for given
    range periods i.e today, this week, this year.
    '''
    appointment_model = Appointment
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated, ]

    def get(self, request, *args, **kwargs):
        # date filters initialization
        todays_date = TodaysDate().localize_time()
        date_filters = OtherDateFilters()

        # get doctors profile
        doctor = self.doctors_profile()

        # the dates to filter from
        # i.e mondays date, years start date, etc.
        mondays_date = date_filters.monday()
        month_starts_date = date_filters.monthStart()
        year_starts_date = date_filters.janFirst()

        # filter appointments
        todays_appointment = self.appointment_model.objects.filter(doctor=doctor, appointment_status='Booked', date=todays_date)
        this_weeks_appointments = self.appointment_model.objects.filter(doctor=doctor, appointment_status='Booked', date__range=[mondays_date, todays_date])
        this_months_appointments = self.appointment_model.objects.filter(doctor=doctor, appointment_status='Booked', date__range=[month_starts_date, todays_date])
        this_years_appointments = self.appointment_model.objects.filter(doctor=doctor, appointment_status='Booked', date__range=[year_starts_date, todays_date])
        
        # serializers
        todays_serializer = self.get_serializer(todays_appointment, many=True)
        this_weeks_serializer = self.get_serializer(this_weeks_appointments, many=True)
        this_months_serializer = self.get_serializer(this_months_appointments, many=True)
        this_years_serializer = self.get_serializer(this_years_appointments, many=True)

        return Response(data={
            'info': f'Hello {request.user}',
            'todays_appointments': {
                'date': f'{todays_date}',
                'data': todays_serializer.data},
            'this_weeks_appointments': this_weeks_serializer.data,
            'this_months_appointments': this_months_serializer.data,
            'this_years_data': this_years_serializer.data
        })

    def doctors_profile(self):
        try:
            doctor = DoctorProfile.objects.get(user=self.request.user)
        except ObjectDoesNotExist:
            return Response(
                {'error': 'You do not have a doctor\'s profile'},
                status=403
            )
        return doctor