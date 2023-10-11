from django.contrib import admin

from .models import Therapist, SafeguardLead, Appointment, Client


admin.site.register(Therapist)
admin.site.register(SafeguardLead)
admin.site.register(Client)
admin.site.register(Appointment)
