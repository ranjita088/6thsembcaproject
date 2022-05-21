from django import forms
from django.contrib.auth.forms import UserCreationForm
from apps.hospitalappointment.models import  Contactus, CustomUser,DoctorAppointment, PasswordReset

class CustomUserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model  =CustomUser
        fields =("username","address","phone","email",'password1', 'password2')
        
        # fields =("email",)

class DoctorAppointmentForm(forms.ModelForm):
    class Meta:
        model = DoctorAppointment
        exclude = ("user","done",   ) #except user field display all field
        widgets={
            'date':forms.DateInput(attrs={'type':'date'}),
            'time':forms.TimeInput(attrs={'type':'time'}),
            'symptoms' : forms.Textarea(attrs={'rows':3, 'cols':47})

        }

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contactus
        fields = ("name","email","number","message",)

# class ContactForm(forms.Form):
#     Name = forms.CharField(max_length=30)
#     Email = forms.EmailField(max_length = 150)
#     Number = forms.IntegerField()
#     Message = forms.CharField(max_length=500,widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))


class PasswordResetForm(forms.ModelForm):
    class Meta:
        model = PasswordReset()
        fields = ("email",)
