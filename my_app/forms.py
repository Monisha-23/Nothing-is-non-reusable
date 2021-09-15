from django import forms
from .models import *

class EditUserProfileForm(UserChangeForm):
    password = None

    class Meta:
        model = home
        fields = ['username','first_name','last_name','email','date_joined','last_login','is_active']
        labels = {'email': 'Email'}