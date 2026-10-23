"""Median der Bruttojahreseinkommen unselbständig Erwerbstätiger, 1997 bis 2024.

Nominal wie in der Quelle. Die Umrechnung in Preise eines Bezugsjahres macht das
Frontend mit dem VPI (Feld `deflate`), damit data.json nur Quellwerte enthält.
"""

from readers import read_ods
from sources import SOURCES

from .common import indicator, to_series

SHEET = "Tabelle1"


def _median_column(rows):
    """Spalte 'Median' im Block 'Bruttojahreseinkommen' aus dem Tabellenkopf."""
    block_row = next(r for r in rows if any(str(c).startswith("Bruttojahreseinkommen") for c in r))
    start = next(i for i, c in enumerate(block_row) if str(c).startswith("Bruttojahreseinkommen"))
    end = next(i for i, c in enumerate(block_row) if str(c).startswith("Nettojahreseinkommen"))
    measure_row = rows[rows.index(block_row) + 1]
    col = next(i for i in range(start, end) if measure_row[i] == "Median")
    unit_row = rows[rows.index(block_row) + 2]
    if "Euro" not in " ".join(map(str, unit_row)):
        raise ValueError(f"Unerwartete Einheit im Tabellenkopf: {unit_row!r}")
    return col


def _pairs():
    rows = read_ods(SOURCES["einkommen"].path)[SHEET]
    col = _median_column(rows)
    # Nur der erste Block "Insgesamt"; danach folgen Frauen und Männer.
    start = next(i for i, r in enumerate(rows) if r[1:2] == ["Insgesamt"])
    pairs = []
    for r in rows[start + 1 :]:
        if not (r and isinstance(r[0], float)):
            break
        pairs.append((int(r[0]), r[col]))
    return pairs


def build():
    return indicator(
        "income_median_gross",
        "Bruttojahreseinkommen (Median)",
        "Euro",
        "Die Hälfte der unselbständig Erwerbstätigen verdiente im Jahr weniger als diesen Betrag, "
        "die andere Hälfte mehr (brutto, inklusive Teilzeit und unterjährig Beschäftigter, ohne Lehrlinge)",
        ["einkommen"],
        to_series(_pairs()),
        notes=[
            "Bruttojahresbezüge gemäß § 25 EStG laut Lohnsteuerdaten.",
            "Enthält Teilzeit und nicht ganzjährig Beschäftigte; ein Anstieg kann auch an längerer Arbeitszeit liegen.",
            "1997 bis 2001 in der Quelle aus Schilling in Euro umgerechnet (Spaltenkopf: EUR-ATS bzw. Euro).",
            "Nominalwerte. Der Wert in heutigen Preisen ist mit dem Verbraucherpreisindex umgerechnet.",
        ],
        deflate="cpi",
    )
