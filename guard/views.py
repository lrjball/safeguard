from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.conf import settings
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Therapist, Appointment, Client, SafeguardLead


@login_required
def index(request):
    return render(
        request=request,
        template_name="guard/index.html",
        context={'title': f'Hello {request.user}'},
    )


class TherapistListView(ListView):
    model = Therapist
    paginate_by = 100
    template_name="guard/lead_list.html"

    # def get_queryset(self):
    #     return Therapist.objects.filter(administrator=self.request.user.administrator)
    # def get_context_data(self, **kwargs):


class TherapistDetailView(DetailView):
    model = Therapist
    template_name="guard/therapist.html"


def therapist_detail_view(request, therapist_id):
    template_name="guard/therapist.html"
    therapist = Therapist.objects.get(id=therapist_id)
    return render(request, template_name, {
        'therapist': therapist, 
        'appointments': therapist.appointment_set.all()
        })


class ClientDetailView(DetailView):
    model = Client
    template_name="guard/client.html"

    #def get(self):


#@login_required
#def 
