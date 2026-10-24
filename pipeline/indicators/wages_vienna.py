"""Brutto-Stundenverdienste der Industriearbeiter in Wien, 1987 bis 2005.

Erhebung der Bundes- bzw. Wirtschaftskammer (September), veröffentlicht im
Statistischen Jahrbuch der Stadt Wien. Abschrift:
data/manual/wien_stundenverdienste_industriearbeiter.csv (Spalte `methode`: scan =
am Scanbild abgelesen, volltext = OCR-Volltext der Wienbibliothek, textebene = Text
des born-digital-PDFs). Gleiche Regeln wie bei den Wiener Preisen: Reihe in Euro,
Schilling / 13,7603, Schillingwert in `series_ats`, Jahrgänge müssen übereinstimmen.

Grundlage für die Arbeitsminuten je Ware (Frontend, Feld `work_minutes` der Preise).
"""

import csv

from sources import MANUAL

from .common import indicator, to_series
from .prices_vienna import ATS_PER_EUR

MANUAL_CSV = MANUAL / "wien_stundenverdienste_industriearbeiter.csv"
SOURCES_USED = [
    "wien_preise_jb1992",
    "wien_preise_jb1996",
    "wien_preise_jb1999",
    "wien_preise_jb2003",
    "wien_preise_jb2006",
    "ak_einkommen_2009",
]


def manual_rows():
    with open(MANUAL_CSV, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def by_unit():
    """{Einheit: {Jahr: {Wert, ...}}}"""
    result = {"ATS": {}, "EUR": {}}
    for r in manual_rows():
        result[r["einheit"]].setdefault(int(r["jahr"]), set()).add(float(r["wert"]))
    return result


def series():
    """(Euro-Reihe, Schilling-Reihe). Abweichungen zwischen Jahrgängen brechen den Build ab."""
    values = by_unit()
    for unit, per_year in values.items():
        conflicts = {y: v for y, v in per_year.items() if len(v) > 1}
        if conflicts:
            raise ValueError(f"Stundenverdienste {unit}: Jahrgänge widersprechen sich: {conflicts}")
    ats = {y: next(iter(v)) for y, v in values["ATS"].items()}
    eur = {y: next(iter(v)) for y, v in values["EUR"].items()}
    eur.update({y: v / ATS_PER_EUR for y, v in ats.items()})
    return dict(sorted(eur.items())), dict(sorted(ats.items()))


def build():
    eur, ats = series()
    return indicator(
        "wage_industry_vienna",
        "Stundenlohn Industriearbeiter (Wien)",
        "Euro pro Stunde",
        "Durchschnittlicher Brutto-Stundenverdienst der Industriearbeiter in Wien, einschließlich Akkorde und Prämien",
        SOURCES_USED,
        to_series(eur.items()),
        notes=[
            "Erhebung der Bundes- bzw. Wirtschaftskammer, jeweils im September; veröffentlicht im Statistischen Jahrbuch der Stadt Wien.",
            "Nur Industriearbeiter: nicht repräsentativ für alle Beschäftigten (Angestellte, Handel, Dienstleistungen fehlen).",
            "Brutto, vor Steuern und Sozialversicherung.",
            "Ab 2004 laut Quelle ohne Elektroindustrie.",
            "Bis 1999 in Schilling erhoben und mit 13,7603 Schilling je Euro umgerechnet.",
        ],
        series_ats={str(y): v for y, v in ats.items()},
        breaks=[{"year": 2004, "before": ""}],  # nur im Diagramm markieren, Hinweis im Quellen-Panel
        deflate="cpi",
        ended=True,
        ended_note="nur 1987 bis 2005 erfasst",
    )
