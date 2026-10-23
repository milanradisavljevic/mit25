"""Anteil der Bevölkerung ab 65 Jahren, Jahresdurchschnitt, 1961 bis 2025."""

from .common import indicator, to_series, zeitreihe


def build():
    return indicator(
        "share_65plus",
        "Anteil der Bevölkerung ab 65",
        "%",
        "Anteil der Menschen ab 65 Jahren an der Bevölkerung im Jahresdurchschnitt",
        ["zeitreihen"],
        to_series(zeitreihe("18", "65 Jahre und älter", after="Männer und Frauen")),
    )
