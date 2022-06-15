from django.urls import path

from apps.hospitalappointment.views import About_us, Contact_us, DocDeleteAppt, DoctorInfo, Services, SignIn, SignOut, Signup, UserDeleteAppt, UserDetailsView, UserUpdateAppt, View_Doctor, ViewAppointment, approve_appointment_view, createAppointment, disapprove_appointment_view, index_page


# apps_name = "appointment"

urlpatterns = [
    path("", index_page, name='home'),
    path("about/", About_us, name='about'),
    path("contact/", Contact_us, name='contact'),
    path("service/", Services, name='service'),
    path('login/', SignIn, name="login"),
    path('logout/', SignOut, name="sign_out"),
    path('signup/', Signup, name="sign_up"),
    path("createAppointment/", createAppointment, name="createAppointment"),
    path("viewAppointment/", ViewAppointment, name="viewAppointment"),
    path("userdetailsview/", UserDetailsView, name="userdetailsview"),
    path('userdeleteappt/<int:id>/', UserDeleteAppt, name='userdeleteappt'),
    path('userupdateappt/<int:id>/', UserUpdateAppt, name='userupdateappt'),
    # path("password_reset/", password_reset_request, name="password_reset"),
    path("viewdoctor/", View_Doctor, name="viewdoctor"),
    path("doctorinfo/<int:pk>/", DoctorInfo, name="doctorinfo"),
    path('docdeleteappt/<int:id>/', DocDeleteAppt, name='docdeleteappt'),
    
    path('approve_appointment_view/<str:appointment_id>',approve_appointment_view,name="approve_appointment_view"),
    
    path('disapprove_appointment_view/<str:appointment_id>', disapprove_appointment_view,name="disapprove_appointment_view"),

]

