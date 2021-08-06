
import json
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.urls import reverse
from users.forms import CustomUserCreationForm, AddressesForm
from django.views.generic import View
from users.models import Addresses

# from users.models import AuthUser

# Create your views here.
# users/views.py

class Dashboard(View):
    def get(self, request):
        print(self.request)
        
        user_id = request.user.id
        context = {
            'userAddresses' : self.getUserAddresses(user_id=user_id).addresses.items(),
            'form' : AddressesForm()
        }
        return render(request, 'users/dashboard.html', context=context)

    def post(self, request, *args, **kwargs):
        user_id = request.user.id

        if 'delete' in request.POST:
            self.deleteAddress(user_id, request.POST['addressName'])
        else:
            self.createOrUpdateAddress(user_id, AddressesForm(request.POST))

        context = {
            'userAddresses': self.getUserAddresses(user_id=user_id).addresses.items(),
            'form': AddressesForm(),
        }
        return render(request, 'users/dashboard.html', context)

    def hasAddresses(self, user_id):
        try: 
            json_address = Addresses.objects.get(user_id=user_id)
            return True
        except:
            return False

    def createOrUpdateAddress(self, user_id, form):
        if form.is_valid():
            fd = form.cleaned_data

            if self.hasAddresses(user_id):
                self.updateAddress(user_id, fd.get('addressName'), fd.get('address'))
            else:
                self.addFirstAddress(user_id, fd.get('addressName'), fd.get('address'))

    def getUserAddresses(self, user_id):
        if self.hasAddresses(user_id):
            return Addresses.objects.get(user_id=user_id)
        else:
            return []

    def deleteAddress(self, user_id, addressName):
        try:
            deleteAddress = self.getUserAddresses(user_id=user_id)
            deleteAddress.addresses.pop(addressName)
            deleteAddress.save(update_fields=['addresses'])
            return True
        except:
            return False

    def updateAddress(self, user_id, addressName, address):
        try:
            updateAddress = self.getUserAddresses(user_id=user_id)
            updateAddress.addresses[addressName] = address
            updateAddress.save(update_fields=['addresses'])
            return True
        except:
            return False
    
    def addFirstAddress(self, user_id, addressName, address):
        try: 
            firstAddress = {addressName:address}
            Addresses.objects.create(user_id=user_id, address=firstAddress)
            return True
        except:
            return False

def register(request):
    if request.method == "GET":
        return render(
            request, 
            "users/register.html",
            {"form": CustomUserCreationForm}
        )
    elif request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.backend = "django.contrib.auth.backends.ModelBackend"
            user.save()
            login(request, user)
            return redirect(reverse("dashboard"))
    else:
        form = CustomUserCreationForm()
    return render(
        request, 
        "users/register.html",
        {"form":form}
    )