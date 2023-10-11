from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("therapist/", views.TherapistListView.as_view(), name="therapists"),
    path("therapist/<int:pk>/", views.TherapistDetailView.as_view(), name="therapist_detail"),
    # path(r"^therapist/(\w+)$", views.TherapistDetailView.as_view(), name="therapist_detail"),
]