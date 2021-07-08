from django import forms

import datetime
from scrapper.models import Stops

class JourneyPlannerForm(forms.Form):
    start_point = forms.CharField(
        label='Starting Point', 
        max_length=100, 
        # required=True, 
        # widget=forms.TextInput(
        # attrs={
        #     'style': 'width: 400px',
        #     'class': 'basicAutoComplete',
        #     'data-url': "/dublinbushybrid/stopID_autocomplete/"
        )
    destination_point = forms.CharField(label='Destination Point', max_length=100)
    travel_date = forms.DateField(label='Please choose a date within the next 7 days') #, widget=forms.DateInput(format = '%d/%m/%Y'), input_formats=settings.DATE_INPUT_FORMATS)

    def clean(self):
        cd = self.cleaned_data
        start = cd.get('start_point')
        destination = cd.get('destination_point')

        if len(Stops.objects.filter(stop_name=start)) == 0:
            self.add_error('start_point', 'No starting stop with this name')

        if len(Stops.objects.filter(stop_name=destination)) == 0:
            self.add_error('destination_point', 'No destination stop with this name')

        travel_date = cd.get('travel_date')
        today = datetime.date.today()

        if travel_date and travel_date < today:
            self.add_error('travel_date', 'Invalid date - date of travl is in past')

        # Check if a date is in the allowed range (+4 weeks from today).
        if travel_date and travel_date > today + datetime.timedelta(days=7):
            self.add_error('travel_date', 'Invalid date - date of travel is too far in the future')

        return cd
