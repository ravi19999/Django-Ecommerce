from django import forms

from .models import Address


class AddressForm(forms.ModelForm):
    class Mets:
        model = Address
