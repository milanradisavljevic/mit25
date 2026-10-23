"""Verbraucherpreisindex als Jahresdurchschnitt, 1946 bis 2025.

Lebenshaltungskostenindex 1938 (verkettet), Basis März 1938 = 100. Dient nur zur
Umrechnung historischer Preise, wird nicht direkt angezeigt.
"""

from readers import parse_decimal_comma, read_ogd_csv
from sources import SOURCES

from .common import indicator, to_series

TOTAL_INDEX = "VPI-0"


def annual_rows():
    """Jahresdurchschnitte: Zeitraum-Code 'VPIZR-JJJJ' (Monate sind 'VPIZR-JJJJMM')."""
    rows = read_ogd_csv(SOURCES["vpi_lhki38"].path)
    return [
        r for r in rows if r["C-VPI1-0"] == TOTAL_INDEX and len(r["C-VPIZR-0"]) == len("VPIZR-JJJJ")
    ]


def first_month():
    rows = read_ogd_csv(SOURCES["vpi_lhki38"].path)
    return min(r["C-VPIZR-0"] for r in rows if len(r["C-VPIZR-0"]) == len("VPIZR-JJJJMM"))


def build():
    pairs = [(int(r["C-VPIZR-0"][6:]), parse_decimal_comma(r["F-VPIMZBM"])) for r in annual_rows()]
    start = first_month()
    return indicator(
        "cpi",
        "Verbraucherpreisindex",
        "Index (März 1938 = 100)",
        "Lebenshaltungskostenindex 1938, über alle späteren Verbraucherpreisindizes verkettet, Jahresdurchschnitt",
        ["vpi_lhki38"],
        to_series(pairs),
        notes=[f"Monatswerte beginnen {start[10:]}/{start[6:10]}; der Jahresdurchschnitt 1946 deckt nur diese Monate ab."],
        display=False,
    )
