"""
flight_log forms to add new flight, aircraft, etc
"""

from django import forms

from .models import AircraftManufacturer


class AircraftManufacturerForm(forms.ModelForm):
    """Form to create new Aircraft Manufacturer"""

    class Meta:
        model = AircraftManufacturer
        fields = ["name"]
