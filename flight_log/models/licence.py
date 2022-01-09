"""
Licence model
"""

from django.db import models
from django.utils.translation import gettext
from polymorphic.models import PolymorphicModel

from .aircraft_type import AircraftTypeList
from .pilot import Pilot


class AircraftLicence(PolymorphicModel):
    """class to group all licence type"""

    licence_type = models.CharField(
        max_length=5,
        choices=AircraftTypeList,
    )

    pilot = models.ForeignKey(Pilot, on_delete=models.CASCADE)

    commercial = models.BooleanField(default=False)
    night = models.BooleanField(default=False)
    instructor = models.BooleanField(default=False)

    delivery_date = models.DateField()
    check_flight_date = models.DateField()


class Medical(models.Model):
    """Medical certificat information"""

    class MedicalType(models.TextChoices):
        """kind of medical certificat"""

        CLASS1 = "1", gettext("Class 1")
        CLASS2 = "2", gettext("Class 2")
        LAPL = "L", gettext("LAPL")

    pilot = models.ForeignKey(Pilot, on_delete=models.CASCADE)

    medical_type = models.CharField(max_length=1, choices=MedicalType.choices)
    delivery_date = models.DateField()
    expiration_date = models.DateField(blank=True)
