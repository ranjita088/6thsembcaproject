
from distutils.command.upload import upload
from django.db import models
# from django.contrib.auth.models import User


# src/users/model.py
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self,email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


# src/users/model.py
from django.contrib.auth.models import AbstractUser
# from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    fullname = models.CharField(max_length= 225,null=True)
    username = models.CharField(max_length= 225,null=True)
    address = models.CharField(max_length=255,null=True)
    phone = models.CharField(max_length=100,null=True)
    email = models.EmailField(_('email'), unique=True)
    is_doctor = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []    

    objects = CustomUserManager()

    def __str__(self):
        return self.email



class MedicalDepartment(models.Model):
    DEPT_CHOICES = [
        ('Cardiologist','Cardiologist'),
        ('Dermatologists','Dermatologists'),
        ('Emergency Medicine Specialists','Emergency Medicine Specialists'),
        ('Allergists/Immunologists','Allergists/Immunologists'),
        ('Anesthesiologists','Anesthesiologists'),
        ('Colon and Rectal Surgeons','Colon and Rectal Surgeons')
    ]
    department = models.CharField(max_length=255,choices= DEPT_CHOICES)
    create_at = models.DateTimeField(auto_now_add=True)
    uodate_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.department


class Doctor(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    doc_name = models.CharField(max_length=200,null=True)
    doc_email = models.EmailField(max_length=200,null=True)
    doc_number = models.CharField(null=True,max_length=200)
    doc_address = models.CharField(max_length=200,null=True)
    department = models.ForeignKey(MedicalDepartment,on_delete=models.CASCADE)
    nmc = models.CharField(max_length=255)
    degree = models.CharField(max_length=255) #many to many choice field
    doc_image = models.FileField(null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (self.user.email) #display email in db


class DoctorAppointment(models.Model):
    
    TIMESLOT_LIST = [
        (1, '09:00 - 09:30'),
        (2, '10:00 - 10:30'),
        (3, '11:00 - 11:30'),
        (4, '12:00 - 12:30'),
        (5, '13:00 - 13:30'),
        (6, '14:00 - 14:30'),
        (7, '15:00 - 15:30'),
        (8, '16:00 - 16:30'),
        (9, '17:00 - 17:30'),
    ]

    STATUS_CHOICES=[
        ('Pending','Pending'),
        ('Accept','Accept'),
        ('Reject','Reject')
    ]
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    patient_name=models.CharField(max_length=100)
    patient_address=models.CharField(max_length=100)
    patient_number=models.CharField(max_length=100)
    doctor=models.ForeignKey(Doctor,on_delete=models.CASCADE)
    date=models.DateField()
    timeslot = models.IntegerField(choices=TIMESLOT_LIST,null=True)
    symptoms = models.TextField(null=True)
    create_at = models.DateTimeField(auto_now_add=True,null=True)
    update_at = models.DateTimeField(auto_now=True,null=True)
    status = models.CharField(max_length=100,choices= STATUS_CHOICES,default="Pending",null=True)
    Approved = models.BooleanField(default=False)
    


    @property
    def time(self):
        return self.TIMESLOT_LIST[self.timeslot][1]
    
     
    # class Meta:
    #     unique_together = ('doctor', 'date', 'timeslot')
    
    def __str__(self):
        return self.user.email

class Contactus(models.Model):
    name =models.CharField(max_length=30)
    email = models.EmailField()
    number = models.CharField(max_length=100,null=True)
    message = models.TextField(max_length=500)


    def __str__(self):
        return (self.user.name)
        
# class PasswordReset(models.Model):
#     user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
#     email = models.EmailField()

#     def __str__(self):
#         return (self.user.email)

