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
        ('EU 35', 'EU 35'),
        ('EU 36', 'EU 36'),
        ('EU 37', 'EU 37'),
        ('EU 38', 'EU 38'),
        ('EU 39', 'EU 39'),
        ('EU 40', 'EU 40'),
        ('EU 41', 'EU 41'),
        ('EU 42', 'EU 42'),
        ('EU 43', 'EU 43'),
        ('EU 44', 'EU 44'),
    )
    CLOTHES_SIZE_CHOISES = (
        ('XS', 'XS'),
        ('S', 'S'),
        ('M', 'M'),
        ('L', 'L'),
        ('XL', 'XL'),
    )
    gender = forms.ChoiceField(choices=GENDER_CHOISES, widget=forms.Select(attrs={'class':'custom-select', 'placeholder':'Gender'}))
    country = forms.ChoiceField(choices=country_choises, widget=forms.Select(attrs={'class':'custom-select', 'placeholder':'Country'}))
    sweater_size = forms.ChoiceField(choices=CLOTHES_SIZE_CHOISES, widget=forms.Select(attrs={'class':'custom-select', 'placeholder':'Sweater size'}))
    pants_size = forms.ChoiceField(choices=CLOTHES_SIZE_CHOISES, widget=forms.Select(attrs={'class':'custom-select', 'placeholder':'Pants size'}))
    shoes_size = forms.ChoiceField(choices=SHOES_SIZE_CHOISES, widget=forms.Select(attrs={'class':'custom-select', 'placeholder':'Shoes size'}))