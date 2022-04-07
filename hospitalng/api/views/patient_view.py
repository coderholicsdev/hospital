'''
View for patient Dashboard
- Appointment handling 
    > manage doctors appointment (make, and cancel)

- Ewallet Info.
    > update payment details
    > Fund e-wallet 

- Invoicing
- Hospitals
- Pharmacy
- 
'''
# import exception from django.db
from django.core.exceptions import ObjectDoesNotExist

# GenericAPIView
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView

# response
from rest_framework.response import Response

# status
from rest_framework import status

# DRF permissions
from rest_framework.permissions import IsAuthenticated

# decorators 
from api.decorators import check_patient_profile

# import serializers
from api.serializers.profile_serializer import PatientProfileSerializer
from api.serializers.appointment_serializer import AppointmentSerializer

# import patient model
from api.models import PatientProfile
from api.models import Appointment
from api.serializers.appointment_serializer import BookAppointmentSerializer

class CheckIsPatientMixin(APIView):
    model = None
    permission_classes = [IsAuthenticated, ]

    def get(self, request, *args, **kwargs):
        try:
            user_model = self.model.objects.get(user=self.request.user)
        except ObjectDoesNotExist:
            return Response(data={
                'error': 'You are not allowed to view this page'
            },
            status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = self.serializer_class(user_model)
        kwargs['user'] = f'Hello {user_model.user}'
        kwargs['data'] = serializer.data
        return Response(
            data=kwargs
        )

    def get_user_model(self):
        try:
            self.user_model = self.model.objects.get(user=self.request.user)
        except ObjectDoesNotExist:
            return Response(data={
                'error': 'You are not allowed to view this page'
            },
            status=status.HTTP_403_FORBIDDEN
            )


class PatientDashboard(CheckIsPatientMixin):
    model = PatientProfile
    serializer_class =  PatientProfileSerializer

class ViewAppointments(ListAPIView, CheckIsPatientMixin):
    '''
    View to display all the available appointments with a Doctor
    '''
    serializer_class = AppointmentSerializer
    queryset = Appointment.objects.all()
    status = 'Open'
    permission_classes = [IsAuthenticated, ]
    
    def get_queryset(self):
        queryset = Appointment.objects.filter(appointment_status=self.status)
        return queryset

class BookAppointment(APIView):
    '''
    View to help patients book appointments
    '''
    # @check_patient_profile
    def post(self, request, appointment_id):
        try:
            #  check if the appointment id exists
            appointment = Appointment.objects.get(appointment_id=appointment_id)

        except ObjectDoesNotExist:
            ''' 
            if the appointment_id does not exist return a response and a
            404 status
            '''
            return Response(data={
                    'id_not_found': 'Sorry The ID you were looking for Does not exist'
                },
            status=status.HTTP_404_NOT_FOUND
            )
        
        # catch an appointment that is not Open
        if appointment.appointment_status != 'Open':
            return Response(
                data={
                    'error': 'Sorry This appointment is unavailable for booking'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        # Book the appointment 
        Appointment.objects.filter(appointment_id=appointment_id).update(appointment_with=request.user, appointment_status='Booked')

        return Response(
            data={
                'success': 'Appointment Successfully Booked'
            },
            status=status.HTTP_201_CREATED
        )

class AppointmentsStatusMixin(ListAPIView):
    '''
    To allow patients view the appointments they have made
    if any
    '''
    serializer_class = AppointmentSerializer
    queryset = Appointment.objects.all()
    permission_classes = [IsAuthenticated, ]
    
    def get_queryset(self):
        try:
            patient = PatientProfile.objects.get(user=self.request.user)
        except ObjectDoesNotExist:
            return Response(data={
                'error': 'You are not allowed to view this page'
            },
            status=status.HTTP_403_FORBIDDEN
            )
            
        queryset = Appointment.objects.filter(appointment_with=patient, 
        appointment_status=self.appointment_status)

        return queryset

class PatientsBookedAppointments(AppointmentsStatusMixin):
    # Get all the booked appointments a user has made if any
    appointment_status = 'Booked'

class PatientsCancelledAppointment(AppointmentsStatusMixin):
    # Get all the appointment that the user cancelled or was cancelled by
    # the doctor
    appointment_status = 'Cancelled'

class PatientsRescheduledAppointments(AppointmentsStatusMixin):
    appointment_status = 'Rescheduled'

class CancelAppointment(APIView):
    serializer_class = BookAppointmentSerializer
    permission_classes = [IsAuthenticated, ]

    def post(self, request, appointment_id, *args, **kwargs):
        try:
            #  check if the appointment id exists
            appointment = Appointment.objects.get(appointment_id=appointment_id)

        except ObjectDoesNotExist:
            ''' 
            if the appointment_id does not exist return a response and a
            404 status
            '''
            return Response(data={
                    'id_not_found': 'Sorry The ID you were looking for Does not exist'
                },
            status=status.HTTP_404_NOT_FOUND
            )

        # get the same type of user for the logged in user and 
        # user that made the appointment
        user_that_made_appointment = appointment.appointment_with.user.email
        logged_in_user =  request.user.email

        '''
        if the user that made the appointment is not the logged in user
        return an error and a 401 status
        '''
        if user_that_made_appointment != logged_in_user:
            return Response(data=
                {'error': 'Sorry you did not make this appointment'},
                status=status.HTTP_401_UNAUTHORIZED)
        
        # if the appointment has already been cancelled
        if appointment.appointment_status == 'Cancelled':
            return Response(
                data={
                    'error': 'This Appointment has already been cancelled'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # if the appointment is opened
        if appointment.appointment_status == 'Open':
            return Response(
                data={
                    'error': "This Appointment is Open, you can't cancel it "
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        Appointment.objects.filter(appointment_id=appointment_id).update(appointment_status='Cancelled')

        return Response(
            data={
                'success': 'Appoinment successfully cancelled'
            }
        )
        
