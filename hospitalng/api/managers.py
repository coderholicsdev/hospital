'''
The managers Model is responsible for changing the User model
to accept Email as username
'''

from django.contrib.auth.base_user import BaseUserManager

# lazy text
from django.utils.translation import ugettext_lazy as _

class UserManager(BaseUserManager):
    '''
    Custom UserManager where email is the identifieer instead of 
    username
    '''
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_('The Email Must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('SuperUser must have is_staff=True'))
        
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('SuperUser must have is_superuser=True'))

        return self.create_user(email, password, **extra_fields)