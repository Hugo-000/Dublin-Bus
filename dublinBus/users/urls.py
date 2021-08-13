# users/urls.py
from django.urls import path
from django.conf.urls import include, url
from users.views import  register #dashboard,
from . import views

urlpatterns = [
    url(r"^accounts/", include("django.contrib.auth.urls")),
    # url(r"^dashboard/", dashboard, name="dashboard"),
    url(r"^oauth/", include("social_django.urls")),
    url(r"^register/", register, name="register"),

    path('dashboard/', views.Dashboard.as_view(), name='dashboard'),
    path('delete/', views.Delete.as_view(), name='delete'),
]