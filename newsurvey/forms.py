"""
form details
"""
from django import forms

class LoginForm(forms.Form):
    """
    Login_form details
    """
    username = forms.CharField(max_length=40, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                            'placeholder': 'email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                 'placeholder': 'password'}))

class AdminForm(forms.Form):
    """
    admin form
    """
    admin_name = forms.CharField(max_length=40,
                                 widget=forms.TextInput(attrs={'class': 'form-control',
                                                               'placeholder': 'admin_name'}))
    ad_username = forms.CharField(max_length=40,
                                  widget=forms.TextInput(attrs={'class': 'form-control',
                                                                'placeholder': 'uname'}))
    ad_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                    'placeholder': 'password'}))
    admin_email = forms.EmailField(max_length=40,
                                   widget=forms.TextInput(attrs={'class': 'form-control',
                                                                 'placeholder': 'email'}))
    company = forms.CharField(max_length=40,
                              widget=forms.TextInput(attrs={'class': 'form-control',
                                                            'placeholder': 'Org name'}))


class EventsForm(forms.Form):
    """
    Event form
    """
    name = forms.CharField(max_length=40,
                           widget=forms.TextInput(attrs={'class': 'form-control',
                                                         'placeholder': 'Org name'}))

