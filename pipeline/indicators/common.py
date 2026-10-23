"""Gemeinsame Hilfen für Indikator-Module."""

from readers import ods_year_row, read_ods
from sources import SOURCES


def to_series(pairs, fill_gaps=True):
    """[(Jahr, Wert), ...] -> {"Jahr": Wert}. Doppelte Jahre sind ein Fehler.

    fill_gaps: fehlende Jahre zwischen erstem und letztem Jahr als None eintragen.
    Ereignisreihen (Wahlen) nutzen fill_gaps=False.
    """
    values = {}
    for year, value in pairs:
        if year in values:
            raise ValueError(f"Jahr {year} doppelt")
        values[year] = value
    if not values:
        return {}
    years = range(min(values), max(values) + 1) if fill_gaps else sorted(values)
    return {str(year): values.get(year) for year in years}


def indicator(id, label, unit, description, sources, series, notes=(), **extra):
    """Indikator im Format aus PLAN.md Abschnitt 4. `sources`: Schlüssel aus SOURCES."""
    used = [SOURCES[key] for key in sources]
    return {
        "id": id,
        "label": label,
        "unit": unit,
        "description": description,
        "source": "; ".join(s.label for s in used),
        "source_url": used[0].url,
        "sources": [{"label": s.label, "url": s.url} for s in used],
        "retrieved": max(s.retrieved for s in used),
        "notes": list(notes),
        **extra,
        "series": series,
    }


def zeitreihe(sheet, label, after=None):
    """Zeile aus den Demographischen Zeitreihenindikatoren 1961 bis 2025."""
    return ods_year_row(read_ods(SOURCES["zeitreihen"].path)[sheet], label, after)
