"""
Aircraft views
"""

from django.core.exceptions import ValidationError
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import generic

from ..forms import AircraftManufacturerForm
from ..models import Aircraft, AircraftManufacturer


class IndexAircraftView(generic.ListView):
    """generic view, see all aircraft"""

    template_name = "flight_log/index_aircraft.html"
    context_object_name = "aircraft_list"

    def get_queryset(self):
        """return every aircraft, alphabetical immatriculation"""

        aircrafts = Aircraft.objects.all().order_by("immatriculation")

        return aircrafts


class IndexAircraftManufacturerView(generic.ListView):
    """generic view, see all aircraft manufacturer"""

    template_name = "flight_log/index_aircraft_manufacturer.html"
    context_object_name = "aircraft_manufacturer_list"

    def get_queryset(self):
        """return every aircraft manufacturer, alphabetical immatriculation"""

        aircraft_manufacturers = AircraftManufacturer.objects.all().order_by("name")

        return aircraft_manufacturers


class DetailAircraftManufacturerView(generic.DetailView):
    """Detail view on aircraft manufacturer"""

    model = AircraftManufacturer
    template_name = "flight_log/detail_aircraft_manufacturer.html"


def create_aircraft_manufacturer_view(request):
    """create a new aircraft manufacturer"""

    if not request.user.is_pilot:
        return HttpResponseRedirect(reverse("flight_log:index_aircraft_manufacturer"))

    if request.method == "POST":
        try:
            aircraft_manufacturer_form = AircraftManufacturerForm(request.POST)

            if aircraft_manufacturer_form.is_valid():
                aircraft_manufacturer = aircraft_manufacturer_form.save()

                if "create" in request.POST:
                    return HttpResponseRedirect(
                        reverse(
                            "flight_log:detail_aircraft_manufacturer",
                            args=(aircraft_manufacturer.id,),
                        )
                    )

        except ValidationError:
            aircraft_manufacturer_form.clean()
    else:
        aircraft_manufacturer_form = AircraftManufacturerForm()

    return render(
        request,
        "flight_log/create_aircraft_manufacturer.html",
        {"form": aircraft_manufacturer_form},
    )
