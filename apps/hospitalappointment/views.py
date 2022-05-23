
from django import forms
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from apps.hospitalappointment.forms import ContactForm, CustomUserForm ,DoctorAppointmentForm, PasswordResetForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout,authenticate
from apps.hospitalappointment.models import CustomUser, DoctorAppointment,Doctor 
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
    sub = ContactForm()
    if request.method == 'POST':
        sub = ContactForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['email']
            name=sub.cleaned_data['name']
            message = sub.cleaned_data['message']
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

def Signup(request):
    if(request.method == 'POST'):
        form = CustomUserForm(request.POST)
        if(form.is_valid()):
            # print("thanks")
            user = form.save()
            login(request, user)
            return redirect('login')
            # return HttpResponseRedirect('/')

    else:
        form = CustomUserForm()
    return render(request, 'newpages/signup.html', {'form': form})


from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm

# def SignUp(request):
#     if(request.method == "POST"):
#         form = CustomUserForm(request.POST)

#         if(form.is_valid):
#             # print("thanks")
#             form.save()
#             # login(request,user)
#             messages.success(request,"register successfully")
#             return redirect('login')
#             # return HttpResponseRedirect('/')
#     else:
#         messages.error(request,'invalid login')
#         form  = CustomUserForm()
#     return render(request,"newpages/signup.html",{'form':form})


  

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
               messages.info(request, f"You are now logged in as {username}.")
               return HttpResponseRedirect('/')
            else:
                pass
        else:
            return render(request,"newpages/sigIn.html",{'form':form})
    else:
        # messages.error(request,"Invalid Username and password")
        form = AuthenticationForm()
        return render(request,"newpages/sigIn.html",{'form':form})

def SignOut(request):
    logout(request)
    messages.info(request, "You have successfully logged out.") 
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



#password


from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
# from apps.hospitalappointment.forms import PasswordResetForm

def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = CustomUser.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "password/password_reset_email.txt"
					c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'Website',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'admin@gmail.com' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					return redirect ("/password_reset/done/")
	password_reset_form = PasswordResetForm()
    
	return render(request=request, template_name="password/password_reset.html", context={"password_reset_form":password_reset_form})
