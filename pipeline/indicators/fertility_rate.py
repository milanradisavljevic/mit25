"""Gesamtfertilitätsrate. 1961 bis 2025 Statistik Austria; 1951 bis 1960 Human Fertility Database."""

from .common import extract_pairs, indicator, to_series, with_earlier, zeitreihe


def build():
    pairs, breaks = with_earlier(
        zeitreihe("I", "Gesamtfertilitätsrate (Kinderzahl pro Frau)"),
        extract_pairs("tfr"),
        "Human Fertility Database",
    )
    return indicator(
        "fertility_rate",
        "Kinder pro Frau",
        "Kinder je Frau",
        "Gesamtfertilitätsrate: durchschnittliche Kinderzahl einer Frau, wenn die Geburtenhäufigkeit "
        "des jeweiligen Jahres ein Leben lang gälte",
        ["zeitreihen", "hfd"],
        to_series(pairs),
        notes=[
            "Ab 2015 inklusive nicht in Österreich Geborener von Müttern mit Wohnsitz in Österreich.",
            "1951 bis 1960 aus der Human Fertility Database (Periodenfertilität); für 1961 bis 2023 "
            "weicht sie höchstens 0,004 von Statistik Austria ab.",
        ],
        breaks=breaks,
    )
