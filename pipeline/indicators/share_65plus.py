"""Anteil der Bevölkerung ab 65 Jahren, Jahresdurchschnitt.

1961 bis 2025 Statistik Austria; 1947 bis 1960 aus der Human Mortality Database
(Personenjahre je Altersjahr, siehe pipeline/extract_hmd_hfd.py).
"""

from .common import extract_pairs, indicator, to_series, with_earlier, zeitreihe

HMD_NOTE = (
    "1947 bis 1960 aus der Human Mortality Database berechnet (Personenjahre je Altersjahr); "
    "für 1961 bis 2023 weicht diese Berechnung höchstens 0,07 Prozentpunkte von Statistik Austria ab."
)


def build():
    pairs, breaks = with_earlier(
        zeitreihe("18", "65 Jahre und älter", after="Männer und Frauen"),
        extract_pairs("share_65plus"),
        "Human Mortality Database",
    )
    return indicator(
        "share_65plus",
        "Anteil der Bevölkerung ab 65",
        "%",
        "Anteil der Menschen ab 65 Jahren an der Bevölkerung im Jahresdurchschnitt",
        ["zeitreihen", "hmd"],
        to_series(pairs),
        notes=[HMD_NOTE],
        breaks=breaks,
    )
