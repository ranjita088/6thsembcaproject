from django.contrib import admin

from apps.hospitalappointment.models import CustomUser, Doctor, DoctorAppointment, MedicalDepartment



admin.site.register(MedicalDepartment)
admin.site.register(Doctor)
admin.site.register(CustomUser)
admin.site.register(DoctorAppointment)
# admin.site.register(Contactus)
