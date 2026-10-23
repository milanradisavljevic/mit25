"""Median der Bruttomonatseinkommen von Arbeitern und Angestellten, 1953 bis 2009.

Daten des Hauptverbands der Sozialversicherungsträger, veröffentlicht von der AK Wien.
Abschrift: data/manual/ak_bruttomonatseinkommen_1953_2009.csv (gedruckte Seite 28 des PDFs).

Methodenbruch 1987: bis 1987 Juli-Wert einschließlich Lehrlinge, ab 1987
Jahresdurchschnitt ohne Lehrlinge. Für 1987 gibt die Quelle beide Werte an; die Reihe
nimmt ab 1987 den Jahresdurchschnitt und führt den Bruch im Feld `breaks`, damit das
Frontend die Linie dort trennt. Nicht mit den Lohnsteuerdaten (income_median) vergleichbar.
"""

import csv

from sources import MANUAL

from .common import indicator, to_series

MANUAL_CSV = MANUAL / "ak_bruttomonatseinkommen_1953_2009.csv"
BREAK_YEAR = 1987
BEFORE = "juli_mit_lehrlingen"
AFTER = "jahresdurchschnitt_ohne_lehrlinge"

GROUPS = {
    "arbeiter": ("Arbeiter", "Arbeiterinnen und Arbeiter"),
    "angestellte": ("Angestellte", "weiblichen und männlichen Angestellten"),
}


def manual_rows():
    with open(MANUAL_CSV, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def _pairs(group):
    pairs = []
    for r in manual_rows():
        year = int(r["jahr"])
        expected = BEFORE if year < BREAK_YEAR else AFTER
        if r["basis"] == expected:
            pairs.append((year, int(r[f"median_{group}"])))
    return pairs


def _juli_1987(group):
    return next(int(r[f"median_{group}"]) for r in manual_rows() if r["jahr"] == "1987" and r["basis"] == BEFORE)


def build():
    result = []
    for group, (label, who) in GROUPS.items():
        result.append(
            indicator(
                f"income_monthly_{group}",
                f"Monatseinkommen {label} (Median)",
                "Euro pro Monat",
                f"Die Hälfte der {who} verdiente brutto im Monat weniger als diesen Betrag "
                "(ohne Urlaubs- und Weihnachtsgeld, inklusive Teilzeit, ohne Beamte)",
                ["ak_einkommen_2009"],
                to_series(_pairs(group)),
                notes=[
                    "Daten des Hauptverbands der Sozialversicherungsträger, veröffentlicht von der AK Wien; Reihe endet 2009.",
                    "Beitragspflichtiges Monatseinkommen ohne Sonderzahlungen (1/14 des Jahreseinkommens).",
                    f"Methodenwechsel {BREAK_YEAR}: davor Wert für Juli, einschließlich Lehrlinge; "
                    f"ab {BREAK_YEAR} Jahresdurchschnitt ohne Lehrlinge. "
                    f"Der Juli-Wert {BREAK_YEAR} beträgt laut Quelle {_juli_1987(group)} Euro.",
                    "Alle Jahre in der Quelle mit 13,7603 Schilling je Euro umgerechnet.",
                    "Andere Quelle und andere Abgrenzung als das Bruttojahreseinkommen der Lohnsteuerdaten; nicht direkt vergleichbar.",
                ],
                breaks=[{"year": BREAK_YEAR, "before": "Juli-Wert, mit Lehrlingen"}],
                deflate="cpi",
                ended=True,
            )
        )
    return result
