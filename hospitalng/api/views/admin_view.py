'''
view to handle admin dashboard and handling hospital
admin stuff.
'''
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    UpdateAPIView,
    ListAPIView,
    GenericAPIView)

# import models
from api.models import (
    Hospital,
    Invoice,
    Specialty
    )

# serializers
from api.serializers.hospital_serializers import HospitalSerializer
from api.serializers.invoice_serializer import AdminInvoicesSerializer
from api.serializers.specialty_serializer import AddSpecialtySerializer, ViewSpecialtySerializer

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

'''Invoicing'''
class PaidInvoices(ListAPIView):
    permission_classes = [IsAuthenticated,]
    queryset = Invoice.objects.all()
    serializer_class = AdminInvoicesSerializer

    def get_queryset(self):
        queryset = Invoice.objects.filter(invoice_status='Paid')
        return queryset

class UnPaidInvoices(PaidInvoices):
    def get_queryset(self):
        queryset = Invoice.objects.filter(invoice_status='Unpaid')
        return queryset 

'''
Specialties
'''
class CreateSpecialty(CreateAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = AddSpecialtySerializer

class ViewSpeiclaties(ListAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = ViewSpecialtySerializer
    queryset = Specialty.objects.all()


class SpecialtyQuerySetOverideMixin:
    def get_queryset(self):
        slug = self.kwargs['specialty_slug']
        queryset = Specialty.objects.filter(slug=slug)
        return queryset


class UpdateSpecialties(SpecialtyQuerySetOverideMixin, GenericAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = AddSpecialtySerializer
    queryset = Specialty.objects.all()

    def put(self, request, specialty_slug, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        queryset = self.get_queryset()
        print(queryset)
        if serializer.is_valid():
            data = serializer.data
        else:
            return Response(
                {
                    'error': serializer.errors
                }
            )
        
        queryset.update(**data)
        view_change = ViewSpecialtySerializer(queryset, many=True)
        return Response(
            {
                'success': 'successfully Updated',
                'data': view_change.data
            },
            status=201
        )

    

class DeleteSpecialty(SpecialtyQuerySetOverideMixin ,GenericAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = AddSpecialtySerializer
    queryset = Specialty.objects.all()

    def delete(self, request, specialty_slug, *args, **kwargs):
        queryset = self.get_queryset()
        if queryset.exists():    
            queryset.delete()
            return Response(
                {
                    'success': 'Successfully removed specialty'
                },
                status=204
            )
        return Response(
                {
                    'error': 'Item doesnot exist'
                },
                status=400
            )
