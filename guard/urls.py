from django.urls import path

from . import views

urlpatterns = [
    path("", views.TherapistListView.as_view(), name="therapists"),
    path("therapist/<int:pk>/", views.TherapistDetailView.as_view(), name="therapist_detail"),
    path("appointment/<int:pk>/", views.AppointmentDetailView.as_view(), name="appointment_detail"),
    path("appointment/<int:pk>/check_in", views.appointment_check_in, name="appointment_check_in"),
    path("appointment/<int:pk>/check_out", views.appointment_check_out, name="appointment_check_out"),
]