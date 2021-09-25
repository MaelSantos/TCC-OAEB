from django.shortcuts import render
from django.views.generic import DetailView, ListView
from .models import Beneficiario

# Create your views here.
from django.http import HttpResponse


def index(request):
    return render(request, 'polls/principal.html')


class BeneficiarioListView(ListView):
    model = Beneficiario


class BeneficiarioDetailView(DetailView):
    model = Beneficiario
