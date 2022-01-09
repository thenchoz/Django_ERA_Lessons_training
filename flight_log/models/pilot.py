"""
Pilot and Flight model
"""

from django.contrib.auth import get_user_model as User
from django.db import models
from polymorphic.models import PolymorphicModel

from .aircraft import Aircraft


class Pilot(models.Model):
    """Pilot class"""

    user = models.OneToOneField(User(), on_delete=models.CASCADE)


class FlightBook(PolymorphicModel):
    """a list of flights from a pilot"""

    pilot = models.OneToOneField(Pilot, on_delete=models.CASCADE)


class Flight(PolymorphicModel):
    """a specific flight"""

    book = models.ForeignKey(FlightBook, on_delete=models.CASCADE)
    aircraft = models.ForeignKey(Aircraft, on_delete=models.PROTECT)
    notes = models.CharField(max_length=500, null=True)

    take_off_time = models.DateTimeField()
    take_off_place = models.CharField(max_length=250)

    landing_time = models.DateTimeField()
    landing_place = models.CharField(max_length=250)
    nb_landing = models.SmallIntegerField(default=1)
