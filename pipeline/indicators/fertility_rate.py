"""Gesamtfertilitätsrate, 1961 bis 2025."""

from .common import indicator, to_series, zeitreihe


def build():
    return indicator(
        "fertility_rate",
        "Kinder pro Frau",
        "Kinder je Frau",
        "Gesamtfertilitätsrate: durchschnittliche Kinderzahl einer Frau, wenn die Geburtenhäufigkeit "
        "des jeweiligen Jahres ein Leben lang gälte",
        ["zeitreihen"],
        to_series(zeitreihe("I", "Gesamtfertilitätsrate (Kinderzahl pro Frau)")),
        notes=["Ab 2015 inklusive nicht in Österreich Geborener von Müttern mit Wohnsitz in Österreich."],
    )
