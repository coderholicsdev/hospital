from django.core.exceptions import ObjectDoesNotExist

# import status and Response
from rest_framework.response import Response
from rest_framework import status

# import models
from api.models import Appointment, PatientProfile

def check_patient_profile(function):
    def wrap(request, *args, **kwargs):
        try:
            PatientProfile.objects.get(user=request.user)
        except ObjectDoesNotExist:
            return Response(data={
                'error': 'You are not allowed to view this page'
            },
            status=status.HTTP_403_FORBIDDEN
            )

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap