from django.urls import path

# simplejwt token authentication (login and refresh token) 
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
# import views
from .views.authentication_views import RegisterView
from .views.profile_create_views import CreatePatientProfileView, CreateDoctorProfileView, CreateAdminProfileView
from .views import patient_view
from .views import doctor_view


app_name = 'api'


urlpatterns = [
    # authentication routes

    # register route
    path('register/', RegisterView.as_view(), name='register'),

    # login and refresh token
    path('login-token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]


urlpatterns += [
    # profile creation routes (patients, doctors, admin)
    path('profile/create/patients/', CreatePatientProfileView.as_view(), name='create-patient-profile-view'),
    path('profile/create/doctors/', CreateDoctorProfileView.as_view(), name='create-doctor-profile-view'),
    path('profile/create/admin/', CreateAdminProfileView.as_view(), name='create-admin-profile-view'),
]

urlpatterns+=[
    # patient dashboard
    path('patient/dashboard/', patient_view.PatientDashboard.as_view(), name='patient-dashboard'),

    # create an appointment
    path('patient/create-appointment/', patient_view.CreateAppointment.as_view(), name='create-appointment-patient'),

    # book appointment 
    path('patient/book-appointment/<str:appointment_id>/', patient_view.BookAppointment.as_view(), name='patient-book-appointment'),
    path('patient/booked-appointments/', patient_view.PatientsBookedAppointmentsByDoctor.as_view(), name='booked-appointments'),

    # cancel appointment
    path('patient/cancelled-appointments/', patient_view.PatientsCancelledAppointment.as_view(), name='cancelled-appointments'),
    path('patient/cancel-appointment/<str:appointment_id>/', patient_view.CancelAppointment.as_view(), name='cancel-an-appointment'),

    # rescheduled
    path('patient/rescheduled-appointments/', patient_view.PatientsRescheduledAppointments.as_view(), name='rescheduled-appointments'),
]

urlpatterns += [
    path('doctor/dashboard/', doctor_view.DoctorsDashboard.as_view(), name='doctors-homepage'),
]