"""Durchschnittspreise ausgewählter Waren in Wien, 1980 bis 1992 (Pilot).

Abschrift aus drei Ausgaben des Statistischen Jahrbuchs der Stadt Wien
(data/manual/wien_durchschnittspreise_1980_1992.csv). Jahresdurchschnitte in Schilling,
erhoben vom Österreichischen Statistischen Zentralamt (Wiener Preise).
Überlappende Jahre (1984, 1988) stehen in zwei Ausgaben und müssen übereinstimmen.

Umrechnung in Euro (Frontend, Feld `eur_factor`): fixer Kurs 13,7603 Schilling je Euro,
belegt in data/raw/ak_wien_bruttoeinkommen_arbeiter_angestellte_2009.pdf, S. 2.
"""

import csv

from sources import MANUAL

from .common import indicator, to_series

MANUAL_CSV = MANUAL / "wien_durchschnittspreise_1980_1992.csv"
ATS_PER_EUR = 13.7603
SOURCES_ALL = ["wien_preise_1980_1984", "wien_preise_1984_1988", "wien_preise_1988_1992", "ak_einkommen_2009"]

GENERAL_NOTES = [
    "Durchschnittspreise in Wien (Erhebung des Österreichischen Statistischen Zentralamts), nicht für ganz Österreich.",
    "Laut Jahrbuch sind die Preise ab 1987 wegen geänderter Warenbeschreibungen nicht streng mit den Vorjahren vergleichbar.",
    "Umrechnung in Euro mit dem fixen Kurs 13,7603 Schilling je Euro.",
]

GOODS = {
    "semmel": ("Semmel (Wien)", "Stück", "Preis einer maschingeformten Semmel", [], []),
    "vollmilch": ("Vollmilch (Wien)", "Liter", "Preis für 1 Liter Vollmilch, abgepackt", [], []),
    "kinokarte": ("Kinokarte (Wien)", "Stück", "Preis einer Kinokarte", [], []),
    "benzin": (
        "Benzin Normal (Wien)",
        "Liter",
        "Preis für 1 Liter Normalbenzin",
        ["Bis 1986 Normalbenzin (inländisch), ab 1987 bleifrei laut Fußnote des Jahrbuchs."],
        [{"year": 1987, "before": "noch nicht bleifrei"}],
    ),
}


def manual_rows():
    with open(MANUAL_CSV, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def annual_values(good):
    """{Jahr: Preis} aus den Jahresdurchschnitten; doppelte Jahre müssen gleich sein."""
    values = {}
    for r in manual_rows():
        if r["ware"] != good or r["monat"]:
            continue
        year, price = int(r["jahr"]), float(r["schilling"])
        if year in values and values[year] != price:
            raise ValueError(f"{good} {year}: Ausgaben widersprechen sich ({values[year]} / {price})")
        values[year] = price
    return values


def build():
    result = []
    for good, (label, per, description, notes, breaks) in GOODS.items():
        extra = {"breaks": breaks} if breaks else {}
        result.append(
            indicator(
                f"price_{good}",
                label,
                "Schilling",
                f"{description} in Wien, Jahresdurchschnitt (je {per})",
                SOURCES_ALL,
                to_series(sorted(annual_values(good).items())),
                notes=notes + GENERAL_NOTES,
                deflate="cpi",
                eur_factor=1 / ATS_PER_EUR,
                # Pilot: Quelle geht vermutlich weiter, erfasst ist bisher nur bis 1992
                ended=True,
                ended_note="bisher nur bis 1992 erfasst",
                **extra,
            )
        )
    return result
