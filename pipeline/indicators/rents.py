"""Mieten: Anteil am Haushaltseinkommen (Eurostat, ab 2003) und Durchschnittsmiete (Mikrozensus, ab 2005)."""

import json
import re

from readers import read_ods
from sources import SOURCES

from .common import indicator, to_series

MZ_SHEET = "Tabelle_2"
MZ_BLOCK = "Durchschnittliche Miete inkl. Betriebskosten pro Wohnung in Euro"
MZ_COLUMN = "Öster-\nreich"


def eurostat_share():
    """{Jahr: (Wert, Flag)} aus der Eurostat-JSON-Antwort (nur eine Zeitreihe abgefragt)."""
    with open(SOURCES["eurostat_mietanteil"].path, encoding="utf-8") as f:
        data = json.load(f)
    others = [d for d in data["id"] if d != "time"]
    if any(data["size"][data["id"].index(d)] != 1 for d in others):
        raise ValueError("Eurostat-Antwort enthält mehr als eine Zeitreihe")
    values, flags = data["value"], data.get("status", {})
    result = {}
    for year, index in data["dimension"]["time"]["category"]["index"].items():
        key = str(index)
        if key in values:
            result[int(year)] = (values[key], flags.get(key))
    return result


def _year(cell):
    """Jahresspalte: 2005.0, "2023" oder "20212" (Jahr mit angehängter Fußnote 2)."""
    m = re.fullmatch(r"(\d{4})(\d?)(?:\.0)?", str(cell).strip())
    if not m:
        return None
    return int(m.group(1)), m.group(2) or None


def mikrozensus_rent():
    """{Jahr: Miete} für Österreich aus dem Block 'pro Wohnung' von Tabelle 2."""
    rows = read_ods(SOURCES["mikrozensus_wohnkosten"].path)[MZ_SHEET]
    header = next(r for r in rows if MZ_COLUMN in r)
    col = header.index(MZ_COLUMN)
    start = next(i for i, r in enumerate(rows) if len(r) > 1 and r[0] == "" and r[1] == MZ_BLOCK)
    result = {}
    for r in rows[start + 1 :]:
        parsed = _year(r[0]) if r else None
        if parsed is None:
            break
        year, _footnote = parsed
        if year in result:
            raise ValueError(f"Jahr {year} doppelt")
        result[year] = r[col]
    return result


def build():
    share = eurostat_share()
    unexpected = {y: f for y, (_, f) in share.items() if f not in (None, "b")}
    if unexpected:
        raise ValueError(f"Unbekannte Eurostat-Flags: {unexpected}")
    break_years = sorted(y for y, (_, f) in share.items() if f == "b")
    return [
        indicator(
            "rent_share_income",
            "Mietanteil am Haushaltseinkommen",
            "%",
            "Durchschnittlicher Anteil der Miete am verfügbaren Haushaltseinkommen von Haushalten mit Mietzahlung "
            "(ohne Betriebs-, Strom- und Heizkosten)",
            ["eurostat_mietanteil"],
            to_series((y, v) for y, (v, _) in sorted(share.items())),
            notes=[
                "EU-SILC: gewichteter Mittelwert von Monatsmiete × 12 / verfügbarem Haushaltseinkommen; "
                "Haushalte ohne Mietangabe sind ausgeschlossen.",
                "Nebenkosten wie Strom, Heizung, Instandhaltung und Dienstleistungen sind nicht enthalten.",
            ]
            + [f"Zeitreihenbruch {y} laut Eurostat (Umstellung von EU-SILC)." for y in break_years],
            breaks=[{"year": y, "before": "vor Zeitreihenbruch"} for y in break_years],
        ),
        indicator(
            "rent_avg",
            "Miete einer Hauptmietwohnung",
            "Euro pro Monat",
            "Durchschnittliche Monatsmiete einschließlich Betriebskosten je Hauptmietwohnung",
            ["mikrozensus_wohnkosten"],
            to_series(sorted(mikrozensus_rent().items())),
            notes=[
                "Mikrozensus Wohnen; nur Hauptmietwohnungen mit Nettomiete über 0 Euro.",
                "Zeitreihenbruch 2021 laut Quelle wegen Erhebungsumstellung.",
                "Durchschnitt (arithmetisches Mittel), nicht Median.",
            ],
            breaks=[{"year": 2021, "before": "vor Erhebungsumstellung 2021"}],
            deflate="cpi",
        ),
    ]
