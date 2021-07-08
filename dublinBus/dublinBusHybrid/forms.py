from django import forms

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
    travel_date = forms.DateField(label='Please choose a date within the next 7 days')