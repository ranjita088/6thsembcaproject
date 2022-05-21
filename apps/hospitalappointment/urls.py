from django.urls import path

from apps.hospitalappointment.views import About_us,Contact_us,Services, SignIn, SignOut, SignUp, UserDeleteAppt, UserDetailsView, UserUpdateAppt, ViewAppointment,createAppointment,index_page, password_reset_request

# apps_name = "appointment"

urlpatterns = [
    
    path("",index_page,name='home'),
   
    path("about/",About_us,name = 'about'),
    path("contact/",Contact_us,name = 'contact'),
    path("service/",Services,name = 'service'),
    
    path('login/',SignIn, name = "login"),
    
    path('logout/',SignOut, name = "sign_out"),
    path('signup/',SignUp, name = "sign_up"),

    path("createAppointment/",createAppointment,name="createAppointment"),
    path("viewAppointment/",ViewAppointment,name="viewAppointment"),
    path("userdetailsview/",UserDetailsView,name="userdetailsview"),
    path('userdeleteappt/<int:id>/',UserDeleteAppt,name='userdeleteappt'),
    path('userupdateappt/<int:id>/',UserUpdateAppt,name='userupdateappt'),

    path("password_reset/", password_reset_request,name="password_reset"),

]

