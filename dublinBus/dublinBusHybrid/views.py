from django.shortcuts import render
from django.template import loader
from django.views.generic import View

# Create your views here.
from django.http import HttpResponse

class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')

class JourneyPlanner(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'journey-planner.html')

    def post(self, request, *args, **kwargs):
        return HttpResponse('This is POST request') 