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
from .views import admin_view


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
    path('patient/booked-appointments/', patient_view.PatientsBookedAppointments.as_view(), name='booked-appointments'),

    # cancel appointment
    path('patient/cancelled-appointments/', patient_view.PatientsCancelledAppointment.as_view(), name='cancelled-appointments'),
    path('patient/cancel-appointment/<str:appointment_id>/', patient_view.CancelAppointment.as_view(), name='cancel-an-appointment'),

    # rescheduled
    path('patient/rescheduled-appointments/', patient_view.PatientsRescheduledAppointments.as_view(), name='rescheduled-appointments'),

    # my hospital
    path('patient/my-hospital/create/<str:hospital_id>/', patient_view.CreateMyHospitalView.as_view(), name='create-patient-my-hospital'),
    path('patient/my-hospital/delete/<str:hospital_id>/', patient_view.DeleteMyHospitalView.as_view(), name='delete-patient-my-hospital'),
    path('patient/my-hospitals/', patient_view.ViewMyHospitals.as_view(), name='all-patient-my-hospital'),

    # E-wallets
    path('patient/wallet/', patient_view.EwalletView.as_view(), name='patient-wallet'),
    path('patient/wallet/create-ewallet/', patient_view.CreateWalletAccount.as_view(), name='create-patient-wallet'),
    path('patient/wallet/fund-account/<str:id>/', patient_view.FundWalletAccount.as_view(), name='fund-wallet'),

    # Invoices
    path('patient/invoices/', patient_view.ViewInvoices.as_view(), name='patient-invoices'),
]

urlpatterns += [
    path('doctor/dashboard/', doctor_view.DoctorsDashboard.as_view(), name='doctors-homepage'),

    # appointment schedule timing
    path('doctor/appointment-scheduling/', doctor_view.AllAppointmentsDashboard.as_view(), name='doctors-appointment-schedule-timing'),

    # appointments (booked, cancelled, rescheduled)
    path('doctor/booked-appointments/', doctor_view.DoctorBookedAppointments.as_view(), name='doctor-booked-appointments'),
    path('doctor/cancelled-appointments/', doctor_view.DoctorCancelledAppointment.as_view(), name='doctor-cancelled-appointments'),
    path('doctor/rescheduled-appointments/', doctor_view.DoctorRescheduledAppointments.as_view(), name='doctor-rescheduled-appointments'),

    # reschedule an appointment
    path('doctor/reschedule-appointment/<str:appointment_id>/', doctor_view.RescheduleAppointmentWithPatient.as_view(), name='reschedule-appointment-with-patient')
]

'''
admin routes
'''
urlpatterns += [
    path('admin/hospital/all/', admin_view.ViewHospitals.as_view(), name='all-hospitals'),
    path('admin/hospital/create/', admin_view.CreateHospitalPageView.as_view(), name='create-hospital'),
    path('admin/hospital/delete/<str:hospital_id>/', admin_view.DeleteHospitalPageView.as_view(), name='delete-hospital'),
    path('admin/hospital/update/<str:hospital_id>/', admin_view.UpdateHospitalPageView.as_view(), name='update-hospital'),
]