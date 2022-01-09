"""
Balloon aircraft and licence model
"""

from django.db import models
from django.utils.translation import gettext

from .aircraft import Aircraft, AircraftComponent
from .aircraft_type import BALLOON, AircraftCompleteList, AircraftLicenceList
from .licence import AircraftLicence


class GasConnectionType(models.TextChoices):
    """list gas connection"""

    REGO = "R"
    TEMA = "T"


class Burner(AircraftComponent):
    """Burner info"""

    class BurnerType(models.IntegerChoices):
        """nb burner type"""

        SINGLE = 1
        DOUBLE = 2
        TRIPLE = 3
        QUADRA = 4

    weight = models.SmallIntegerField()

    burner_type = models.SmallIntegerField(choices=BurnerType.choices)
    gas_connection_type = models.CharField(
        max_length=1, choices=GasConnectionType.choices
    )

    liquid_pilot_light = models.BooleanField()
    # liquid vs gas pilot light


class FuelCylinder(AircraftComponent):
    """Fuel cylinder info"""

    capacity = models.SmallIntegerField()

    gas_connection_type = models.CharField(
        max_length=1, choices=GasConnectionType.choices
    )

    liquid_connection = models.BooleanField(default=False)


class MountingType(models.TextChoices):
    """type of connecting to the envelope"""

    POINTS4 = "4", gettext("4 mounting points")
    POINTS8 = "8", gettext("8 mounting points")
    GASTYPE = "G", gettext("Gas type")


class Basket(AircraftComponent):
    """Basket info"""

    mounting_point = models.CharField(max_length=1, choices=MountingType.choices)

    weight = models.SmallIntegerField()


class Envelope(AircraftComponent):
    """Envelope info"""

    weight = models.SmallIntegerField()

    enveloppe_size = models.SmallIntegerField()
    cubic_meter_size = models.BooleanField(default=True)
    # True : envelope_size in m3, False : ft3

    mounting_point = models.CharField(max_length=1, choices=MountingType.choices)

    description = models.CharField(max_length=250, blank=True)


class Balloon(Aircraft):
    """Balloon specific fields"""

    basket = models.ForeignKey(Basket, on_delete=models.PROTECT)
    envelope = models.ForeignKey(Envelope, on_delete=models.PROTECT)


class HotAirBalloon(Balloon):
    """Hot air balloon specific"""

    burner = models.ForeignKey(Burner, on_delete=models.PROTECT)
    fuel_cylinders = models.ManyToManyField(FuelCylinder)


class BalloonLicence(AircraftLicence):
    """Balloon specific licence"""

    BALLOON_CHOICE = AircraftCompleteList[BALLOON]
    LICENCE_CHOICE = AircraftLicenceList[BALLOON]

    class_type = models.CharField(max_length=5, choices=BALLOON_CHOICE)
    licence_specific_type = models.CharField(max_length=5, choices=LICENCE_CHOICE)
