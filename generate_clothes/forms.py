from django import forms
from django.forms import Textarea
from .models import CountrySettings
from django.core.exceptions import ValidationError
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
import json


class UserSettingsForm(forms.Form):

    countr_settings_q = CountrySettings.objects.all()
    country_choises = [[country.country,country.country] for country in countr_settings_q]
    GENDER_CHOISES = (
        ('M', 'Male'),
        ('F', 'Female')
    )
    SHOES_SIZE_CHOISES = (
        ('1853', 'EU 36'),
        ('2340', 'EU 37'),
        ('2339', 'EU 38'),
        ('2332', 'EU 39'),
        ('2325', 'EU 40.5'),
        ('2334', 'EU 41'),
        ('2337', 'EU 42'),
        ('2331', 'EU 43'),
        ('1855', 'EU 44'),
        ('2034', 'EU 45'),
        ('2324', 'EU 46'),
    )
    CLOTHES_SIZE_CHOISES = (
        ('1997', 'XS'),
        ('1873', 'S'),
        ('1848', 'M'),
        ('1943', 'L'),
        ('1881', 'XL'),
    )
    clothes_size = forms.ChoiceField(choices=CLOTHES_SIZE_CHOISES)
    shoes_size = forms.ChoiceField(choices=SHOES_SIZE_CHOISES)
    country = forms.ChoiceField(choices=country_choises)
    gender = forms.ChoiceField(choices=GENDER_CHOISES)