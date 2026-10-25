"""Medianalter der Bevölkerung, Jahresdurchschnitt.

1961 bis 2025 Statistik Austria; 1947 bis 1960 aus der Human Mortality Database
(Personenjahre je Altersjahr, Median linear innerhalb des Altersjahres, siehe
pipeline/extract_hmd_hfd.py).
"""

from .common import extract_pairs, indicator, to_series, with_earlier, zeitreihe

HMD_NOTE = (
    "1947 bis 1960 aus der Human Mortality Database berechnet (Personenjahre je Altersjahr); "
    "für 1961 bis 2023 weicht diese Berechnung höchstens 0,04 Jahre von Statistik Austria ab."
)


def build():
    pairs, breaks = with_earlier(
        zeitreihe("18", "Medianalter", after="Männer und Frauen"),
        extract_pairs("median_age"),
        "Human Mortality Database",
    )
    return indicator(
        "median_age",
        "Medianalter der Bevölkerung",
        "Jahre",
        "Alter, das die Bevölkerung in eine jüngere und eine ältere Hälfte teilt (Jahresdurchschnitt)",
        ["zeitreihen", "hmd"],
        to_series(pairs),
        notes=[HMD_NOTE],
        breaks=breaks,
    )
