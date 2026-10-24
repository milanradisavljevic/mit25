"""Durchschnittspreise ausgewählter Waren in Wien, 1966 bis 2005.

Abschrift aus zehn Jahrgängen des Statistischen Jahrbuchs der Stadt Wien
(data/manual/wien_durchschnittspreise.csv). Jahrgang N enthält die Jahresdurchschnitte
N-4 bis N; bis Jahrgang 1999 in Schilling (ATS), ab Jahrgang 2003 in Euro (EUR).

Regeln für die Reihe (Entscheidung 2026-10-24):
- Reihe durchgehend in Euro. Liegt für ein Jahr ein Schillingwert vor, gilt
  Schilling / 13,7603; der Schillingwert steht zusätzlich in `series_ats`.
  Sonst gilt der Euro-Wert der Quelle.
- Stehen für ein Jahr mehrere Werte in derselben Währung, gilt der neueste Jahrgang
  (die Quelle revidiert Vorjahre). Abweichungen sind in KNOWN_REVISIONS aufgeführt;
  jede weitere Abweichung bricht den Build ab.
- Umrechnungskurs belegt in data/raw/ak_wien_bruttoeinkommen_arbeiter_angestellte_2009.pdf, S. 2.
"""

import csv

from sources import MANUAL, SOURCES

from .common import indicator, to_series

MANUAL_CSV = MANUAL / "wien_durchschnittspreise.csv"
ATS_PER_EUR = 13.7603
SOURCE_PREFIX = "wien_preise_jb"

# (Ware, Jahr): Werte, die ein älterer Jahrgang anders angibt als der neuere (Revision).
KNOWN_REVISIONS = {
    ("vollmilch", 1970): "Jahrgang 1970 nennt 4,60 S; die Jahrgänge 1971, 1973 und 1974 nennen 4,20 S.",
}

GENERAL_NOTES = [
    "Durchschnittspreise in Wien (Erhebung des Österreichischen Statistischen Zentralamts), nicht für ganz Österreich.",
    "Bis 2001 in Schilling erhoben und mit dem fixen Kurs 13,7603 Schilling je Euro umgerechnet; ab 2002 Euro laut Quelle.",
    "1979 laut Quelle wegen neu einbezogener Geschäftstypen (z. B. Diskontläden) mit den Vorjahren nicht streng vergleichbar.",
    "Ab 1987 laut Quelle wegen geänderter Warenbeschreibungen mit den Vorjahren nicht streng vergleichbar.",
]

GOODS = {
    "semmel": (
        "Semmel (Wien)",
        "Preis einer Semmel (Stück)",
        ["Bis Jahrgang 1974 als „Semmel, Stück“ geführt, ab spätestens Jahrgang 1979 als „Semmel, Stück, maschingeformt“."],
        [],
    ),
    "vollmilch": (
        "Vollmilch (Wien)",
        "Preis für 1 Liter Vollmilch",
        [
            "Bis 1973 offene Milch; laut Fußnote im Jahrgang 1974 ab 1974 Durchschnittspreis für Milch in Flaschen "
            "und Verpackung (der Jahrgang 1979 nennt 1975). Später „1 l, abgepackt“.",
        ],
        [{"year": 1974, "before": "offene Milch"}],
    ),
    "kinokarte": ("Kinokarte (Wien)", "Preis einer Kinokarte", [], []),
    "benzin": (
        "Benzin Normal (Wien)",
        "Preis für 1 Liter Normalbenzin",
        ["Bis 1986 Normalbenzin (inländisch), ab 1987 bleifrei laut Fußnote des Jahrbuchs."],
        [{"year": 1987, "before": "noch nicht bleifrei"}],
    ),
}


def manual_rows():
    with open(MANUAL_CSV, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def jahrgang(quelle):
    return int(quelle.removeprefix(SOURCE_PREFIX))


def annual_by_unit(good):
    """{Einheit: {Jahr: [(Jahrgang, Wert), ...]}} aus den Jahresdurchschnitten."""
    result = {"ATS": {}, "EUR": {}}
    for r in manual_rows():
        if r["ware"] != good or r["monat"]:
            continue
        result[r["einheit"]].setdefault(int(r["jahr"]), []).append((jahrgang(r["quelle"]), float(r["wert"])))
    return result


def revisions(good):
    """{Jahr: [(Jahrgang, Wert), ...]} für Jahre mit abweichenden Angaben in derselben Währung."""
    found = {}
    for per_year in annual_by_unit(good).values():
        for year, values in per_year.items():
            if len({v for _, v in values}) > 1:
                found[year] = sorted(values)
    return found


def series(good):
    """(Euro-Reihe, Schilling-Reihe) als {Jahr: Wert}."""
    unexpected = set(revisions(good)) - {y for g, y in KNOWN_REVISIONS if g == good}
    if unexpected:
        raise ValueError(f"{good}: unerwartete Abweichungen zwischen Jahrgängen in {sorted(unexpected)}")
    newest = {unit: {y: max(vals)[1] for y, vals in per_year.items()} for unit, per_year in annual_by_unit(good).items()}
    ats = newest["ATS"]
    eur = {y: (ats[y] / ATS_PER_EUR if y in ats else v) for y, v in newest["EUR"].items()}
    eur.update({y: v / ATS_PER_EUR for y, v in ats.items()})
    return dict(sorted(eur.items())), dict(sorted(ats.items()))


def build():
    keys = sorted((k for k in SOURCES if k.startswith(SOURCE_PREFIX)), key=jahrgang)
    result = []
    for good, (label, description, notes, breaks) in GOODS.items():
        eur, ats = series(good)
        revision_notes = [f"Revision {year}: {text}" for (g, year), text in KNOWN_REVISIONS.items() if g == good]
        extra = {"breaks": breaks} if breaks else {}
        result.append(
            indicator(
                f"price_{good}",
                label,
                "Euro",
                f"{description} in Wien, Jahresdurchschnitt",
                keys + ["ak_einkommen_2009"],
                to_series(eur.items()),
                notes=notes + revision_notes + GENERAL_NOTES,
                series_ats={str(y): v for y, v in ats.items()},
                deflate="cpi",
                ended=True,
                ended_note="Tabelle erscheint nach 2005 nicht mehr",
                **extra,
            )
        )
    return result
