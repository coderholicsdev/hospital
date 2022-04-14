# import uuid
from uuid import uuid4
# AbstracUser, models and Ugettext
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext as _

# import custom manager
from api.managers import UserManager


class User(AbstractUser):
    '''
    Modification of User to use email
    instead of username as the primary authentication key
    '''
    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email 

class Hospital(models.Model):
    # model for the hospital registered.
    hospital_id = models.UUIDField(default=uuid4, primary_key = True)
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class PatientProfile(models.Model):
    # model for a patient's profile
    marital_status_list = (
        ('Single', 'Single'),
        ('Married', 'Married'),
        ('Divorced', 'Divorced'),
        ('Widow', 'Widow'),
        ('Widower', 'Widower'),
    )

    patients_sex = (
        ('M', 'M'),
        ('F', 'F'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_picture/patient/')
    address = models.CharField(max_length=200)
    date_of_birth = models.DateField()
    sex = models.CharField(max_length=1, choices=patients_sex)
    height = models.DecimalField(max_digits=5, decimal_places=2)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    phone_number = models.CharField(max_length=11)
    marital_status = models.CharField(max_length=20, choices=marital_status_list)
    spouse_name = models.CharField(max_length=100, blank=True, null=True) #if married.
    next_of_kins_phone_number = models.CharField(max_length=11)
    next_of_kins_email = models.EmailField(max_length=50)

    def __str__(self):
        return self.user.email

class MyHospital(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    hospital = models.OneToOneField(Hospital, on_delete=models.CASCADE)


class DoctorProfile(models.Model):
    # model for a doctor's profile
    doctor_title = (
        ('Doctor','Doctor'),
        ('Radiographer','Radiographer'),
        ('Sonographer', 'Sonographer')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=11)
    qualifications = models.CharField(max_length=200)
    specialty_or_department = models.CharField(max_length=100)
    title = models.CharField(max_length=20, choices=doctor_title)
    hospital_name = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='hospital')
    profile_picture = models.ImageField(upload_to='profile_picture/doctor/')

    def __str__(self):
        return self.name

class AdminProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_picture/admin/')
    full_name = models.CharField(max_length=100, default='')
    phone_number = models.CharField(max_length=11)
    position = models.CharField(max_length=100)

class Appointment(models.Model):
    appointment_status_options = (
        ('Open', 'Open'),
        ('Booked', 'Booked'),
        ('Rescheduled', 'Rescheduled'),
        ('Suspended', 'Suspended'),
        ('Cancelled', 'Cancelled'),
    )
    appointment_id = models.UUIDField(default=uuid4)
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, default=1)
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, default=1)
    appointment_status = models.CharField(max_length=30, choices=appointment_status_options)
    date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return 'Appointment ID - ' + str(self.appointment_id)


class Ewallet(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'E-wallet ID - {self.id}'
  
class Invoice(models.Model):
    invoice_status_list = (
        ('Expired', 'Expired'),
        ('Paid', 'Paid'),
        ('Unpaid', 'Unpaid'),
    )

    invoice_id = models.CharField(unique=True, max_length=9)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    invoice_status = models.CharField(max_length=30, choices=invoice_status_list)
    address = models.TextField()
    issued_date = models.DateField()
    paid_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.invoice_id

class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, related_name='items', on_delete=models.CASCADE)
    description = models.CharField(max_length=100)
    unit_price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return self.description
