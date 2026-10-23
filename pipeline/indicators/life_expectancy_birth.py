"""Lebenserwartung bei Geburt, getrennt nach Männern und Frauen, 1951 bis 2025.

Quelle hat für 1951 bis 1960 keinen Gesamtwert; einen selbst zu bilden wäre eine
Schätzung. Deshalb zwei Reihen aus der langen Sterbetafel-Reihe.
"""

from readers import read_ods
from sources import SOURCES

from .common import indicator, to_series

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
    common = dict(
        unit="Jahre",
        sources=["lebenserwartung"],
        notes=NOTES,
        group="life_expectancy_birth",
    )
    return [
        indicator(
            "life_expectancy_birth_male",
            "Lebenserwartung bei Geburt, Männer",
            description="Durchschnittliche Lebenserwartung eines im jeweiligen Jahr neugeborenen Buben, "
            "berechnet aus der Sterblichkeit dieses Jahres",
            series=to_series(_pairs("Männer")),
            **common,
        ),
        indicator(
            "life_expectancy_birth_female",
            "Lebenserwartung bei Geburt, Frauen",
            description="Durchschnittliche Lebenserwartung eines im jeweiligen Jahr neugeborenen Mädchens, "
            "berechnet aus der Sterblichkeit dieses Jahres",
            series=to_series(_pairs("Frauen")),
            **common,
        ),
    ]
