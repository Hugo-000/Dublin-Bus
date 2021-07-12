from django.urls import path

from . import views

urlpatterns = [
    path('home/', views.Index.as_view(), name='index'),
    path('journeyPlanner/', views.JourneyPlanner.as_view(), name='journeyPlanner'),
    path('Routes/', views.BusRoutes.as_view(), name='Routes'),
    path('CovidInfo/', views.CovidInfo.as_view(), name='CovidInfo'),
    path('LeapCard/', views.LeapCard.as_view(), name='LeapCard')
]
