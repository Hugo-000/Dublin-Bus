from django import forms

import datetime
from scrapper.models import Stops

class JourneyPlannerForm(forms.Form):
    origin_location = forms.CharField(
        # label = 'Origin',
        label = "",
        max_length = 150,
        widget=forms.TextInput(attrs={'placeholder': 'Origin', 'style': 'width: 300px;', 'class': 'form-control'})
    )

    destination_location = forms.CharField(
        # label = 'Destination',
        label = "",
        max_length = 150,
        widget=forms.TextInput(attrs={'placeholder': 'Destination', 'style': 'width: 300px;', 'class': 'form-control'})
    )
    # start_point = forms.CharField(
    #     label='Starting Point', 
    #     max_length=100
    #     )
    # destination_point = forms.CharField(
    #     label='Destination Point', 
    #     max_length=100
    #     )
    travel_date = forms.DateField(
        # label='Date',
        label = "",
        widget=forms.TextInput(attrs={'placeholder': 'Date', 'style': 'width: 300px;', 'class': 'form-control'})
        ) 
    travel_time = forms.TimeField(
        # label='Time',
        label = "",
        widget=forms.TextInput(attrs={'placeholder': 'Time', 'style': 'width: 300px;', 'class': 'form-control'})
    )
    

    def clean(self):
        cd = self.cleaned_data
        start = cd.get('start_point')
        destination = cd.get('destination_point')

        # is the origin in the database under User:
        #     if yes then retrun that address

        # if destiantion is the database under user:
        #     return that address

        # if len(Stops.objects.filter(stop_name=start)) == 0:
        #     self.add_error('start_point', 'No starting stop with this name')

        # if len(Stops.objects.filter(stop_name=destination)) == 0:
        #     self.add_error('destination_point', 'No destination stop with this name')

        travel_date = cd.get('travel_date')
        today = datetime.date.today()

        if travel_date and travel_date < today:
            self.add_error('travel_date', 'Invalid date - date of travl is in past')

        # Check if a date is in the allowed range (+4 weeks from today).
        if travel_date and travel_date > today + datetime.timedelta(days=5):
            self.add_error('travel_date', 'Invalid date - date of travel is too far in the future')
        
        travel_time = cd.get('travel_time')
        bus_start_time = datetime.time(5, 0)
        bus_finish_time = datetime.time(0,0)
        if travel_time and travel_time < bus_start_time:
            self.add_error('travel_date', 'Invalid time - the buses start at 05:00')
        if travel_time and travel_time > bus_finish_time and travel_time < bus_start_time:
            self.add_error('travel_date', 'Invalid time - last bus at 00:00')

        return cd

