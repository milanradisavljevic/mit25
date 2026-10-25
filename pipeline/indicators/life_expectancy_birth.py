"""Lebenserwartung bei Geburt: gesamt, Männer, Frauen, 1947 bis 2025.

Statistik Austria: Männer/Frauen ab 1951 (lange Sterbetafel-Reihe), gesamt ab 1961
(Zeitreihenindikatoren, Unisex). Frühere Jahre aus der Human Mortality Database,
die auch einen Gesamtwert liefert (eigene Berechnung wäre eine Schätzung).
"""

from readers import read_ods
from sources import SOURCES

from .common import extract_pairs, indicator, to_series, with_earlier, zeitreihe

NOTES = [
    "Werte bis 2001 in der Quelle auf zwei Nachkommastellen gerundet.",
    "Ab 2009 inklusive nicht in Österreich verstorbener Personen mit Hauptwohnsitz in Österreich.",
]


def _columns(rows):
    """Spalten für 'Männer'/'Frauen' bei Alter '0 (bei der Geburt)' aus dem Tabellenkopf."""
    sex_row = next(r for r in rows if "Männer" in r and "Frauen" in r)
    age_row = rows[rows.index(sex_row) + 1]
    columns = {}
    for sex in ("Männer", "Frauen"):
        col = sex_row.index(sex)
        if not age_row[col].startswith("0 (bei der"):
            raise ValueError(f"Unerwarteter Tabellenkopf bei {sex}: {age_row[col]!r}")
        columns[sex] = col
    return columns


def _pairs(sex):
    rows = read_ods(SOURCES["lebenserwartung"].path)["t420"]
    col = _columns(rows)[sex]
    # Einzeljahre stehen als Zahl in Spalte A; Periodentafeln ("1949/51") als Text.
    return [(int(r[0]), r[col]) for r in rows if r and isinstance(r[0], float)]


def build():
    hmd = "Human Mortality Database"
    total, total_breaks = with_earlier(zeitreihe("I", "Männer und Frauen (Unisex-Werte)"), extract_pairs("e0_total"), hmd)
    male, male_breaks = with_earlier(_pairs("Männer"), extract_pairs("e0_male"), hmd)
    female, female_breaks = with_earlier(_pairs("Frauen"), extract_pairs("e0_female"), hmd)
    common = dict(unit="Jahre", group="life_expectancy_birth")
    sex_notes = NOTES + [
        "1947 bis 1950 aus der Human Mortality Database; für 1951 bis 2023 weicht sie höchstens 0,11 Jahre "
        "von Statistik Austria ab."
    ]
    return [
        indicator(
            "life_expectancy_birth_total",
            "Lebenserwartung bei Geburt, gesamt",
            description="Durchschnittliche Lebenserwartung eines im jeweiligen Jahr Neugeborenen, "
            "berechnet aus der Sterblichkeit dieses Jahres",
            sources=["zeitreihen", "hmd"],
            series=to_series(total),
            notes=[
                "1961 bis 2025 Unisex-Werte von Statistik Austria (Demographische Indikatoren).",
                "1947 bis 1960 aus der Human Mortality Database; für 1961 bis 2023 weicht sie höchstens "
                "0,07 Jahre von Statistik Austria ab.",
            ],
            breaks=total_breaks,
            **common,
        ),
        indicator(
            "life_expectancy_birth_male",
            "Lebenserwartung bei Geburt, Männer",
            description="Durchschnittliche Lebenserwartung eines im jeweiligen Jahr neugeborenen Buben, "
            "berechnet aus der Sterblichkeit dieses Jahres",
            sources=["lebenserwartung", "hmd"],
            series=to_series(male),
            notes=sex_notes,
            breaks=male_breaks,
            **common,
        ),
        indicator(
            "life_expectancy_birth_female",
            "Lebenserwartung bei Geburt, Frauen",
            description="Durchschnittliche Lebenserwartung eines im jeweiligen Jahr neugeborenen Mädchens, "
            "berechnet aus der Sterblichkeit dieses Jahres",
            sources=["lebenserwartung", "hmd"],
            series=to_series(female),
            notes=sex_notes,
            breaks=female_breaks,
            **common,
        ),
    ]
