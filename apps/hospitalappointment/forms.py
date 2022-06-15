from django import forms
from django.contrib.auth.forms import UserCreationForm
from apps.hospitalappointment.models import  Contactus, CustomUser,DoctorAppointment


class CustomUserForm(UserCreationForm):
    class Meta:
        model=CustomUser
        fields =("fullname","username","address","phone","email",)
        

class DoctorAppointmentForm(forms.ModelForm):
    class Meta:
        model = DoctorAppointment
        exclude = ("user","Approved","status",) #except user field display all field
        widgets={
            'date':forms.DateInput(attrs={'type':'date'}),
            # 'timeslot':forms.TimeField(attrs={'type':'timeslot'}),
            'symptoms' : forms.Textarea(attrs={'rows':3, 'cols':47})

        }

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contactus
        fields = ("name","email","number","message",)



# class PasswordResetForm(forms.ModelForm):
#     class Meta:
#         model = PasswordReset()
#         fields = ("email",)
