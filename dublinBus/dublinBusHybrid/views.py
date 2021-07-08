from django.shortcuts import render
from django.template import loader
from django.views.generic import View

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import Http404


from .forms import JourneyPlannerForm

from scrapper.models import Stops

import datetime

class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')

class JourneyPlanner(View):
    # def get(self, request, *args, **kwargs):
    #     return render(request, 'journey-planner.html')

    def get(self, request):
        return render(request, 'journeyPlanner.html', {'form': JourneyPlannerForm()})

    def post(self, request, *args, **kwargs):
        form = JourneyPlannerForm(request.POST)

        if form.is_valid():
            return render(request, 'journeyPlanner/map.html', { 'form': form })
        else:
            return render(request, 'journeyPlanner.html', { 'form': form })


    