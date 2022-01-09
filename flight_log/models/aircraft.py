"""
Aircraft model
"""

from django.db import models
from polymorphic.models import PolymorphicModel

from .aircraft_type import AircraftTypeList


class AircraftManufacturer(models.Model):
    """use to group aircraft manufacturer"""

    name = models.CharField(max_length=150, unique=True)


class AircraftModel(models.Model):
    """use to group some attribut"""

    manufacturer = models.ForeignKey(AircraftManufacturer, on_delete=models.PROTECT)
    aircraft_type = models.CharField(max_length=1, choices=AircraftTypeList)
    aircraft_specific_type = models.CharField(max_length=5, blank=True)
    model = models.CharField(max_length=200, unique=True)


class AircraftComponent(PolymorphicModel):
    """abstract class use for specific component in aircraft"""

    manufacturer = models.ForeignKey(AircraftManufacturer, on_delete=models.PROTECT)
    model = models.CharField(max_length=200)
    serial_number = models.CharField(max_length=100)


class Aircraft(PolymorphicModel):
    """a specific aircraft"""

    model = models.ForeignKey(AircraftModel, on_delete=models.PROTECT)
    immatriculation = models.CharField(max_length=10, unique=True)

    weight = models.IntegerField()
    passengers_seat = models.SmallIntegerField()

    construction = models.DateField()
