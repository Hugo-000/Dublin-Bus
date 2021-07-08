from django.shortcuts import render
from django.template import loader
from django.views.generic import View

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import Http404


from .forms import JourneyPlannerForm

from scrapper.models import Stops

class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')

class JourneyPlanner(View):
    # def get(self, request, *args, **kwargs):
    #     return render(request, 'journey-planner.html')

    def get(self, request):
        s = Stops.objects.filter(stop_name='Parnell Square West')
        print("HELLO", s)
        return render(request, 'journey-planner.html', {'form': JourneyPlannerForm()})

    # def post(self, request, *args, **kwargs):
    #     return HttpResponse('This is POST request') 

    def post(self, request, *args, **kwargs):
        print(request.POST)
        s = Stops.objects.filter(stop_name='Parnell Square West')
        print("HELLO", s)
        form = JourneyPlannerForm(request.POST)
        print(form.errors)
        # check whether it's valid:
        if form.is_valid():
            start_point = form.cleaned_data['start_point']
            print('Start Point', start_point)
            destination_point = form.cleaned_data['destination_point']
            print('Destination', destination_point)
            s = Stops.objects.filter(stop_name=start_point)
            d = Stops.objects.filter(stop_name=destination_point)
            print("HELLO", s)
            if s.count() == 0:		
                raise Http404("No starting stop with this name")

            if d.count() == 0:
                raise Http404("No destination stop with this name")
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponse('thanks')
        else:
            return render(request, 'journey-planner.html', {'form': form})


    