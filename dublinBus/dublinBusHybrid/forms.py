from django import forms

import datetime
from scrapper.models import Stops

class JourneyPlannerForm(forms.Form):
    origin_location = forms.CharField(
        # label = 'Origin',
        label = "",
        max_length = 150,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Origin', 
                'style': 'width: 300px;', 
                'class': 'form-control'})
    )

    destination_location = forms.CharField(
        # label = 'Destination',
        label = "",
        max_length = 150,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Destination ', 
                'style': 'width: 300px;', 
                'class': 'form-control'})
    )
    
    today = datetime.date.today()
    todayString = today.strftime('%Y-%m-%d')
    datedelta = datetime.timedelta(days=4)
    maxDate = today + datedelta
    maxDateString = maxDate.strftime('%Y-%m-%d')
    travel_date = forms.DateField(
        # label='Date',
        label = "",
        # widget=forms.SelectDateWidget(empty_label=("Choose Year", "Choose Month", "Choose Day")),
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Date', 
                'style': 'width: 300px;', 
                'class': 'form-control;', 
                'type':'date', 
                'name':"trip-start",
                'value':todayString,
                'min':todayString, 
                'max':maxDateString,}),
        required = False
        ) 
    travel_time = forms.TimeField(
        # label='Time',
        label = "",
        widget=forms.TextInput(attrs={'placeholder': 'Time: e.g. 14:00', 'style': 'width: 300px;', 'class': 'form-control'}),
        required = False
    )
    

    def clean(self):
        cd = self.cleaned_data

        travel_date = cd.get('travel_date')
        today = datetime.date.today()

        if travel_date and travel_date < today:
            self.add_error('travel_date', 'Invalid date - date of travel is in past')

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
        if travel_date != today and travel_time == '':
            self.add_error('Please provide a time for departure')

        return cd

    # class Meta:
    #     fields = [
    #         "whatever"
    #     ]

class LeapCradForm(forms.Form):
    leap_username = forms.CharField(
        label = "",
        max_length = 150,
        widget=forms.TextInput(attrs={'placeholder': 'Username', 'style': 'width: 300px;', 'class': 'form-control'})
    )

    leap_password = forms.CharField(
        label = "",
        max_length = 150,
        widget=forms.TextInput(attrs={'placeholder': 'Password', 'style': 'width: 300px;', 'class': 'form-control'})
    )
    def clean(self):
        cd = self.cleaned_data
        return cd