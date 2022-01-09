"""
Aircraft type model
"""

from django.utils.translation import gettext

AIRPLANE = "A"
HELICOPTER = "H"
SAILPLANE = "S"
BALLOON = "B"
UNKNOWN = "U"

AircraftTypeList = [
    (AIRPLANE, gettext("Airplane")),
    (HELICOPTER, gettext("Helicopter")),
    (SAILPLANE, gettext("Sailplane")),
    (BALLOON, gettext("Balloon")),
    (UNKNOWN, gettext("Unknown")),
]

AircraftCompleteList = {
    AIRPLANE: (
        ("GA", gettext("Generic Airplane")),
        ("UA", gettext("Unknown Airplane")),
    ),
    HELICOPTER: (
        ("GH", gettext("Generic Helicopter")),
        ("UH", gettext("Unknown Helicopter")),
    ),
    SAILPLANE: (
        ("GS", gettext("Generic Sailplane")),
        ("US", gettext("Unknown Sailplane")),
    ),
    BALLOON: (
        ("GB", gettext("Generic Balloon")),
        ("GHAB", gettext("Generic Hot-Air Balloon")),
        ("AHAB", gettext("Hot-Air Balloon, class A")),
        ("BHAB", gettext("Hot-Air Balloon, class B")),
        ("CHAB", gettext("Hot-Air Balloon, class C")),
        ("DHAB", gettext("Hot-Air Balloon, class D")),
        ("GGB", gettext("Generic Gas Balloon")),
        ("GMB", gettext("Generic Mixed Balloon")),
        ("GHAAB", gettext("Generic Hot-Air Airship")),
        ("UB", gettext("Unknown Balloon")),
    ),
    UNKNOWN: ("UNK", gettext("Unknown type")),
}

AircraftLicenceList = {
    AIRPLANE: (
        ("GLA", gettext("Generic Airplane licence")),
        ("PPLA", gettext("European airplane private pilot licence")),
        ("ULA", gettext("Unknown Airplane licence")),
    ),
    HELICOPTER: (
        ("GLH", gettext("Generic Helicopter licence")),
        ("PPLH", gettext("European helicopter private pilot licence")),
        ("ULH", gettext("Unknown Helicopter licence")),
    ),
    SAILPLANE: (
        ("GLS", gettext("Generic Sailplane licence")),
        ("SPL", gettext("European sailplane pilot licence")),
        ("ULS", gettext("Unknown Sailplane licence")),
    ),
    BALLOON: (
        ("GLB", gettext("Generic Balloon licence")),
        ("GHAB", gettext("Generic Hot-Air Balloon")),
        ("BPL", gettext("European balloon pilot licence")),
        ("ULB", gettext("Unknown Balloon licence")),
    ),
    UNKNOWN: ("UNK", gettext("Unknown licence type")),
}


def aircraft_text(aircraft_type, abreviation):
    """give text given type and abreviation"""

    return dict(AircraftCompleteList[aircraft_type])[abreviation]


def aircraft_licence_text(aircraft_type, abreviation):
    """give text given type and abreviation"""

    return dict(AircraftLicenceList[aircraft_type])[abreviation]
