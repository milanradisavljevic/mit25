"""Wahlbeteiligung bei Nationalratswahlen (Ereignisreihe), 1919 bis 2024.

Wahlbeteiligung = abgegebene Stimmen (inkl. ungültige) in % der Wahlberechtigten,
wie in der BMI-Tabelle 6.a.
- 1919 bis 2008: data/manual/bmi_wahlbeteiligung_1919_2008.csv, abgetippt aus dem BMI-PDF.
- 2013: Prozentspalte aus dem BMI-Endergebnis.
- 2017, 2019, 2024: Endergebnis enthält keine Prozentspalte; Quotient aus den
  absoluten Zahlen der Österreich-Zeile.
"""

import csv

from readers import read_xlsx
from sources import MANUAL, SOURCES

from .common import indicator, to_series

MANUAL_CSV = MANUAL / "bmi_wahlbeteiligung_1919_2008.csv"

# Wahljahr -> (Quelle, Spalte Wahlberechtigte, Spalte abgegebene Stimmen, Spalte Prozent oder None)
XLSX = {
    2013: ("nrw_2013", "C", "E", "D"),
    2017: ("nrw_2017", "C", "D", None),
    2019: ("nrw_2019", "C", "D", None),
    2024: ("nrw_2024", "C", "D", None),
}


def manual_rows():
    with open(MANUAL_CSV, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def xlsx_result(year):
    """Österreich-Zeile eines Endergebnisses: (Wahlberechtigte, abgegeben, Prozent oder None)."""
    key, col_eligible, col_cast, col_pct = XLSX[year]
    rows = next(iter(read_xlsx(SOURCES[key].path).values()))
    head = rows[:3]

    def header(col):
        return " ".join(str(r.get(col, "")) for r in head).lower().replace("-", "").replace(" ", "")

    if "berechtigte" not in header(col_eligible) or "abge" not in header(col_cast):
        raise ValueError(f"Unerwarteter Tabellenkopf in {SOURCES[key].file}")
    if col_pct and "beteiligung" not in header(col_pct):
        raise ValueError(f"Unerwartete Prozentspalte in {SOURCES[key].file}")
    austria = next(r for r in rows if r.get("A") == "G00000")
    return austria[col_eligible], austria[col_cast], austria.get(col_pct) if col_pct else None


def _pairs():
    pairs = [(int(r["wahltag"][:4]), float(r["abgegeben_pct"])) for r in manual_rows()]
    for year in XLSX:
        eligible, cast, pct = xlsx_result(year)
        pairs.append((year, pct if pct is not None else cast / eligible * 100))
    return pairs


def build():
    return indicator(
        "turnout_nrw",
        "Wahlbeteiligung Nationalratswahl",
        "%",
        "Abgegebene Stimmen (einschließlich ungültiger) in Prozent der Wahlberechtigten",
        ["nrw_1919_2008", "nrw_2013", "nrw_2017", "nrw_2019", "nrw_2024", "parlament_wahlsystem", "parlament_pk0874"],
        to_series(_pairs(), fill_gaps=False),
        type="event",
        notes=[
            "1919: Wahl zur Konstituierenden Nationalversammlung.",
            "1919 bis 2008 mit einer Nachkommastelle laut BMI-Tabelle.",
            "1970: in der BMI-Tabelle irrtümlich als 1966 beschriftet; Fußnote und Veränderungszeile belegen 1970.",
            "1995: inklusive Wiederholungswahl vom 13. Oktober 1996.",
            "2017, 2019 und 2024: aus Wahlberechtigten und abgegebenen Stimmen des BMI-Endergebnisses berechnet.",
            "Wahlpflicht bei Nationalratswahlen gab es in einzelnen Bundesländern: Tirol und Vorarlberg ab 1919, "
            "Steiermark ab 1949, Kärnten ab 1986; 1992 für alle Bundesländer aufgehoben (Parlamentskorrespondenz Nr. 874/2024).",
            "Aktives Wahlalter laut Parlament: 19 Jahre (Stand 1970), 18 Jahre (Stand 1992), 16 Jahre seit 2007, "
            "also erstmals bei der Wahl 2008.",
        ],
    )
