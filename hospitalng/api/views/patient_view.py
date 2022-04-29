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
from django.db import IntegrityError

# import timezone
from django.utils import timezone

# import User model
from django.contrib.auth import get_user_model

# Views from rest_framework
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    DestroyAPIView,
    UpdateAPIView,
    GenericAPIView,
    RetrieveAPIView,
    )
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
from api.serializers.hospital_serializers import MyHospitalSerializer
from api.serializers.appointment_serializer import BookAppointmentSerializer
from api.serializers.ewallet_serializer import FundAccountSerializer, EwalletSerializer
from api.serializers.invoice_serializer import InvoicesSerializer, UpdateInvoiceSerializer
from api.serializers.cart_serializer import CartSerializer

# import models
from api.models import (
    PatientProfile,
    Appointment,
    MyHospital,
    Ewallet,
    Invoice,
    InvoiceItem
    )

# import invoice_id generator
from api.utils.invoice_id import generate_invoice_id

# User
User = get_user_model()

class PermissionMixin:
    permission_classes = [IsAuthenticated, ]

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

'''
This section represents all the views that the
appointment was created by the doctor (i.e appointment_with
= patients)
'''

class AppointmentsStatusMixin(ListAPIView):
    '''
    To deal with all appointments (i.e booked, rescheduled, cancelled) 
    that were made by the doctor to see the patient.
    '''
    serializer_class = AppointmentSerializer
    queryset = Appointment.objects.all()
    permission_classes = [IsAuthenticated, ]
    model_profile = PatientProfile

    def get_queryset(self):        
        queryset = Appointment.objects.filter(
        appointment_status=self.appointment_status, 
        **self.appointment_kwargs()
        )
        return queryset

    def user_doc_patient_check(self):
        user = User.objects.get(email=self.request.user)
        try:
            patient_doc = self.model_profile.objects.get(user=user)
        except ObjectDoesNotExist:
            return Response(data={
                'error': 'You are not allowed to view this page'
            },
            status=status.HTTP_403_FORBIDDEN
            )
        return patient_doc

    def appointment_kwargs(self, **kwargs):
        patient = self.user_doc_patient_check()
        kwargs['patient'] = patient
        return kwargs

class PatientsBookedAppointments(AppointmentsStatusMixin):
    # Get all the booked appointments a doctor has with a user
    appointment_status = 'Booked'

class PatientsCancelledAppointment(AppointmentsStatusMixin):
    # Get all the appointment that the user cancelled or was cancelled by
    # the doctor
    appointment_status = 'Cancelled'

class PatientsRescheduledAppointments(AppointmentsStatusMixin):
    appointment_status = 'Rescheduled'

class CancelAppointment(APIView):
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
        patient_appointment_is_for = appointment.patient.user.email
        logged_in_user =  request.user.email

        '''
        if the user that made the appointment is not the logged in user
        return an error and a 401 status
        '''
        if patient_appointment_is_for != logged_in_user:
            return Response(data=
                {'error': 'Sorry this Appointment is not for you'},
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
        
class CreateAppointment(CreateAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = BookAppointmentSerializer

    def perform_create(self, serializer):
        '''over-ride the perform_create method'''
        user = self.request.user
        # get the patientprofile Model
        patient = PatientProfile.objects.get(user=user)

        # generate the invoice
        invoice = Invoice.objects.create(
            invoice_id=generate_invoice_id(),
            user=user,
            invoice_status='Unpaid',
            issued_date=timezone.localdate(),
        )

        InvoiceItem(
            invoice=invoice,
            description= f'Appointment with the Doctor',
            unit_price=7800.00
        ).save()
        
        # save the serializer
        serializer.save(
            patient=patient,
            appointment_status='Booked'
        )


# Patients "My Hospital"
class CreateMyHospitalView(CreateAPIView):
    # create a hospital for the patients My Hospital section
    serializer_class = MyHospitalSerializer
    permission_classes = [IsAuthenticated, ]
    
    def perform_create(self, serializer):
        '''over ride perform_create and pass the user to the
        patient attribute'''
        user = User.objects.get(email=self.request.user)
        return serializer.save(patient=user)

class DeleteMyHospitalView(DestroyAPIView):
    # delete a hospital for the patients My Hospital section
    queryset = MyHospital.objects.all()
    serializer_class = MyHospitalSerializer
    permission_classes = [IsAuthenticated, ]
    lookup_field = 'hospital_id'

    def get_queryset(self):
        hospital_id = self.kwargs
        queryset = MyHospital.objects.filter(**hospital_id)
        return queryset

class ViewMyHospitals(ListAPIView):
    serializer_class = MyHospitalSerializer
    queryset = MyHospital.objects.all()
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        user = User.objects.get(email=self.request.user)
        queryset = MyHospital.objects.filter(patient=user)
        return queryset

''' Patients E-Wallet '''
class EwalletView(PermissionMixin, ListAPIView):
    serializer_class = EwalletSerializer
    queryset = Ewallet.objects.all()

    def get_queryset(self):
        user = User.objects.get(email=self.request.user)
        queryset = Ewallet.objects.filter(user=user)
        return queryset

class CreateWalletAccount(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request, *args, **kwargs):
        user = User.objects.get(email=request.user)
        try:
            ewallet_instance = Ewallet.objects.create(user=user, amount=0)
        except IntegrityError:
            return Response(
                {'error': 'You already Have an E-wallet created'},
                status=400
            )
        serializer = EwalletSerializer(ewallet_instance)
        return Response(
            {
                'success': 'E-Wallet successfully created.',
                'wallet-information': serializer.data
            }
        )
class FundWalletAccount(PermissionMixin, UpdateAPIView):
    '''
    updates the balance of the user when a successful payment
    has been received 
    '''
    serializer_class = FundAccountSerializer
    queryset = Ewallet.objects.all()
    lookup_field = 'id'

    def get_queryset(self):
        user = User.objects.get(email=self.request.user)
        queryset = Ewallet.objects.filter(user=user)
        return queryset


# Invoicing
class ViewInvoices(GenericAPIView):
    '''
    patients can view all their invoices both paid and unpaid
    '''
    queryset = Invoice.objects.all()
    serializer_class = InvoicesSerializer
    permission_classes = [IsAuthenticated, ]

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(
            serializer.data
        )

    def get_queryset(self):
        queryset = Invoice.objects.filter(user=self.request.user)
        return queryset

class PayThisInvoice(RetrieveAPIView):
    '''
    patients can select an invoice and make a payment with it
    '''
    queryset = Invoice.objects.all()
    serializer_class = InvoicesSerializer
    permission_classes = [IsAuthenticated, ]
    lookup_field = 'invoice_id'

    
    def get_queryset(self):
        queryset = Invoice.objects.filter(user=self.request.user)
        return queryset


class UpdateInvoice(GenericAPIView):
    serializer_class = UpdateInvoiceSerializer
    permission_classes = [IsAuthenticated,]

    def put(self, request, invoice_id, *args, **kwargs):
        invoice_get = Invoice.objects.get(user=request.user, invoice_id=invoice_id)
        if invoice_get.invoice_status == 'Paid':
            return Response(
                {
                    'error': 'This invoice has already been paid for',
                },
                status=400
            )
        invoice = Invoice.objects.filter(user=request.user, invoice_id=invoice_id)
        invoice.update(invoice_status='Paid')
        serializer = self.get_serializer(invoice, many=True)

        return Response(
            {
                'success': 'Invoice Updated',
                'data': serializer.data
            }
        )

class PayInvoiceWithEwallet(GenericAPIView):
    def put(self, request, invoice_id):
        user = request.user
        invoice_get = Invoice.objects.get(user=user, invoice_id=invoice_id)

        if invoice_get.invoice_status=='Paid':
            return Response(
                {
                    'error': 'This Invoice is marked as paid'
                },
                status=400
            )

        # get the patients E-wallet
        wallet = Ewallet.objects.get(user=user)
        wallet_balance = wallet.amount

        # get the price of the items from the invoice
        invoice_items = InvoiceItem.objects.filter(invoice=invoice_get)

        # total sum of invoice items 
        # (while calculating the total of unit_price * quantity)
        invoice_items_total = sum(
            [item.unit_price * item.quantity for item in invoice_items]
            )

        print(invoice_items_total)

        # when the wallet balance is less than the total_invoice_amount
        if wallet_balance < invoice_items_total:
            return Response(
                {
                    'error': 'Your Wallet Balance is too low, Top up your account to continue'
                }
            )
        
        # get the new balance 
        new_balance = wallet_balance - invoice_items_total

        # update the wallet balance
        Ewallet.objects.filter(user=user).update(amount=new_balance)

        # update the invoice status and update the paid date
        Invoice.objects.filter(user=user, invoice_id=invoice_id).update(invoice_status='Paid', paid_date=timezone.localdate())

        return Response(
            {
                'success': 'Payment successfully made with your E-Wallet',
            }
        )

'''
Views to handle the processing of items from the cart
into one invoice
'''
class ProcessCartItems(GenericAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        # get the serializer and validate data
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            data = serializer.data
        else:
            return Response({
                'errors': serializer.errors
                })
        
        # collect the json data from the serializer
        cart_items = data['cart_items']

        # create the invoice
        invoice = Invoice.objects.create(
            invoice_id= generate_invoice_id(),
            user=request.user,
            invoice_status='Unpaid',
            address='Richard Mille Hospitals',
            issued_date=timezone.localdate()
        )

        invoice_items_list = list()

        for item_position in range(len(cart_items)):
            cart_item = cart_items[item_position]
            invoice_item = InvoiceItem(
                invoice=invoice,
                description=cart_item['product'],
                unit_price=cart_item['price'],
                quantity=cart_item['quantity']
            )

            invoice_items_list.append(invoice_item)

        InvoiceItem.objects.bulk_create(invoice_items_list)

        invoice_serializer = InvoicesSerializer(invoice)

        return Response(
            {
                'success': 'Your cart is ready to be paid for',
                'data':invoice_serializer.data
            },
            status=201
        )
