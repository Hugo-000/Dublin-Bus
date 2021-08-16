from django import forms

import datetime
from scrapper.models import Stops

class JourneyPlannerForm(forms.Form):
    origin_location = forms.CharField(
        label = 'Origin',
        max_length = 150,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Origin',
                'class': 'form-control form-control-fw'
            }
        )
    )

    destination_location = forms.CharField(
        label = 'Destination',
        max_length = 150,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Destination ',
                'class': 'form-control form-control-fw'
            }
        )
    )
    
    today = datetime.date.today()
    todayString = today.strftime('%Y-%m-%d')
    datedelta = datetime.timedelta(days=4)
    maxDate = today + datedelta
    maxDateString = maxDate.strftime('%Y-%m-%d')
    travel_date = forms.DateField(
        label='Date',
        # widget=forms.SelectDateWidget(empty_label=("Choose Year", "Choose Month", "Choose Day")),
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Date', 
                'class': 'form-control form-control-fw', 
                'type':'date', 
                'name':"trip-start",
                'value':todayString,
                'min':todayString, 
                'max':maxDateString,
            }
        ),
        required = False
    ) 
    
    travel_time = forms.TimeField(
        label='Time',
        widget=forms.TimeInput(
            format='%H:%M',
            attrs={
            'placeholder': 'Time: e.g. 14:00',
            'class': 'form-control form-control-fw'
            }
        ),
        required = False
    )
    

    def clean(self):
        cd = self.cleaned_data
        today = datetime.date.today()
        now = datetime.datetime.now().time()
        today_datetime = datetime.datetime.combine(today, now)

        if cd.get('travel_time') == None or cd.get('travel_time') == "":
            cd['travel_time'] = now

        travel_date = cd.get('travel_date')
        travel_time = cd.get('travel_time')

        today = datetime.date.today()
        
        travel_datetime = datetime.datetime.combine( travel_date, travel_time)

        bus_start_time = datetime.time(5, 0)
        bus_finish_time = datetime.time(0,0)

        if travel_date and travel_date < today:
            self.add_error('travel_date', 'Invalid date - date of travel is in past')

        # Check if a date is in the allowed range (+4 weeks from today).
        if travel_date and travel_date > today + datetime.timedelta(days=5):
            self.add_error('travel_date', 'Invalid date - date of travel is too far in the future')

        if travel_time and travel_time > bus_finish_time and travel_time < bus_start_time:
            self.add_error('travel_time', 'Invalid time - buses run between 05:00 and 00:00')
        elif travel_time and travel_datetime < today_datetime:
            self.add_error('travel_time', 'Invalid time - cannot make a prediction of the past')
        if travel_date != today and travel_time == '':
            self.add_error('Please provide a time for departure')

        return cd