# users/forms.py
from django.forms import forms
from users.models import Addresses
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.forms.widgets import Input
from django.utils.translation import ugettext_lazy as _


class CustomUserCreationForm(UserCreationForm):
    username = forms.RegexField(
        label=_(""), max_length=30, regex=r"^[\w.@+-]+$",
        help_text= None,
        error_messages={
            'invalid': _(
                "This value may contain only letters, numbers and @/./+/-/_ characters."
                )},
        widget=Input(attrs={
            'class': 'form-control', 
            'required': 'true',
            'placeholder': 'Username'
            }),
    )

    password1 = forms.CharField(
        label=_(""),
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'required': 'true',
            'placeholder': 'Password'
            })
    )
    password2 = forms.CharField(
        label=_(""),
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'type': 'password',
            'required': 'true',
            'placeholder': 'Confirm Password'
            }),
        help_text= None,
    )
    email = forms.CharField(
        label=_(""),
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'type': 'email',
            'placeholder': 'Email',
            'required': 'true'
            })
    )

    class Meta(UserCreationForm.Meta):

        fields = UserCreationForm.Meta.fields + ("email",)
        # widgets = {
        #     "username": Input(attrs={
        #         "type":"text",
        #         "placeholder":"Username",
        #         "class":"user",
        #     }),
        #     "email": Input(attrs={
        #         "type": "text",
        #         "placeholder": "Email",
        #         "class": "email",
        #     }),
        #     "password1": Input(attrs={
        #         "type": "text",
        #         "class": "password",
        #     }),
        #     "password2": Input(attrs={
        #         "type": "text",
        #         "class": "password",
        #     }),
        #
        # }
        # labels = {
        #     "username":"Username :",
        #     "email":"Email :",
        # }
        # help_texts = {
        #     'username': _('Some useful help text.'),
        #     'password1':None,
        #     'password2':_('Some useful help text.'),
        # }

class AddressesForm(forms.Form):
    addressName = forms.CharField(max_length='20', label='Bookmark Name')
    address = forms.CharField(max_length='200', label='Address Name')
    # class Meta:
    #     model = Addresses
    #     fields = [
    #         'addresses'
    #     ]
