"""Medianalter der Bevölkerung, Jahresdurchschnitt, 1961 bis 2025."""

from .common import indicator, to_series, zeitreihe


def build():
    return indicator(
        "median_age",
        "Medianalter der Bevölkerung",
        "Jahre",
        "Alter, das die Bevölkerung in eine jüngere und eine ältere Hälfte teilt (Jahresdurchschnitt)",
        ["zeitreihen"],
        to_series(zeitreihe("18", "Medianalter", after="Männer und Frauen")),
    )
