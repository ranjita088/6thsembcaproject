
from django import forms
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from apps.hospitalappointment.forms import DoctorAppointmentForm
from django.contrib.auth.decorators import login_required
from apps.hospitalappointment.forms import CustomUserForm ,DoctorAppointmentForm
from django.contrib.auth import logout,authenticate
from apps.hospitalappointment.models import CustomUser, DoctorAppointment

from apps.hospitalappointment.models import Doctor 
from django.core.mail import send_mail

from config import settings

def index_page(request):
    context = dict()
    if(request.user.is_authenticated):
        if(request.user.is_doctor):
            d = Doctor.objects.get(user__id = request.user.id)
            appointments = DoctorAppointment.objects.filter(doctor__id=d.id)
            context['appointments'] = appointments
        else:
            appointments = DoctorAppointment.objects.filter(user__id = request.user.id)
            context['appointments'] = appointments
    return render(request,"pages/index.html",context)

def About_us(request):
    context =dict()
    return render(request,"pages/about_us.html",context)    

# def Contact_us(request):
#     context = dict()
#     return render(request,"pages/contact_us.html",context) 

def Contact_us(request):
    sub = forms.ContactusForm()
    if request.method == 'POST':
        sub = forms.ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name=sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']
            send_mail(str(name)+' || '+str(email),message,settings.EMAIL_HOST_USER, settings.EMAIL_RECEIVING_USER, fail_silently = False)
            return render(request, 'newpages/contactussuccess.html')
    return render(request, 'pages/contact_us.html', {'form':sub})

def Services(request):
    context =dict()
    return render(request,"pages/services.html",context) 


@login_required(login_url ='/login/')
def createAppointment(request):
    if(request.method == "POST"):
        form = DoctorAppointmentForm(request.POST)
        if(form.is_valid):
            # print("thanks")
            a = form.save(commit=False)
            a.user =request.user # currnet login user ko info aauxa
            a.save()
            return HttpResponseRedirect('/')
    else:
        form = DoctorAppointmentForm()
    return render(request,"newpages/appoint_form.html",{'form':form})


# def SignUp(request):
#     if(request.method == "POST"):
#         pass
#     else:
#         form  = UserCreationForm()
#     return render(request,"signup.html",{'form':form})

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm

def SignUp(request):
     if(request.method == "POST"):
        form = CustomUserForm(request.POST)

        if(form.is_valid):
            # print("thanks")
            user = form.save()
            login(request,user)
            messages.success(request,"register successfully")
            return redirect('login')
            # return HttpResponseRedirect('/')
     else:
        messages.error(request,'invalid login')
        form  = CustomUserForm()
     return render(request,"newpages/signup.html",{'form':form})


def SignIn(request):
    if(request.method == "POST"):
        form = AuthenticationForm(request,data=request.POST)
        if form.is_valid():
            # print(request.POST)
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username = username, password=password)
            if user is not None:
               login(request,user)
            #    messages.info(request, f"You are now logged in as {username}.")
               return HttpResponseRedirect('/')
            else:
                messages.error(request,"Invalid Username and password")
        else:
            return render(request,"newpages/sigIn.html",{'form':form})
    else:
        # messages.error(request,"Invalid Username and password")
        form = AuthenticationForm()
        return render(request,"newpages/sigIn.html",{'form':form})

def SignOut(request):
    logout(request)
    # messages.info(request, "You have successfully logged out.") 
    return HttpResponseRedirect('/')



@login_required(login_url ='/login/')
def ViewAppointment(request):
  context = dict()
  print(request.user.id)
  doctor = Doctor.objects.get(user__id = request.user.id)
  appointments = DoctorAppointment.objects.filter(doctor__id = doctor.id)
  context['appointments'] = appointments
  appointments = DoctorAppointment.objects.filter(doctor__id = 4,done=False)
  return render(request,"newpages/viewappoint_form.html",context)
    

def UserDetailsView(request):
    context = dict()
    appointments = DoctorAppointment.objects.filter(user__id = request.user.id)
    context['appointments'] = appointments
    return render(request, "newpages/user_details.html",context)


def UserDeleteAppt(request,id):
    appointment = DoctorAppointment.objects.get(id=id)
    appointment.delete()
    return HttpResponseRedirect('/')
   
def UserUpdateAppt(request,id):
    if (request.method == "POST"):
        appointment = DoctorAppointment.objects.get(id=id)
        form =  DoctorAppointmentForm(request.POST, request.FILES,instance = appointment)
        if (form.is_valid()):
            form.save()
            return HttpResponseRedirect('/')
    else:
        appointment = DoctorAppointment.objects.get(id=id)
        form = DoctorAppointmentForm(instance=appointment)


    context = {
        'form': form,
    }
    return render(request, "newpages/user_updateappt.html", context)


