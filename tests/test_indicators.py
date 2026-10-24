import pytest

import build
from indicators.ak_monthly_income import manual_rows as ak_rows
from indicators.common import to_series
from indicators.prices_vienna import ATS_PER_EUR, KNOWN_REVISIONS
from indicators.prices_vienna import annual_by_unit as price_by_unit
from indicators.prices_vienna import manual_rows as price_rows
from indicators.prices_vienna import revisions as price_revisions
from indicators.turnout_nrw import XLSX, manual_rows, xlsx_result
from readers import read_ods
from sources import SOURCES

MVP_IDS = {
    "life_expectancy_birth_male",
    "life_expectancy_birth_female",
    "share_65plus",
    "median_age",
    "fertility_rate",
    "turnout_nrw",
    "cpi",
    "income_median_gross",  # Phase 5
    "income_monthly_arbeiter",
    "income_monthly_angestellte",
    "price_semmel",
    "price_vollmilch",
    "price_kinokarte",
    "price_benzin",
}

# Plausibilitätsgrenzen je Indikator (min, max)
BOUNDS = {
    "life_expectancy_birth_male": (40, 95),
    "life_expectancy_birth_female": (40, 95),
    "share_65plus": (5, 40),
    "median_age": (20, 60),
    "fertility_rate": (0.8, 4),
    "turnout_nrw": (50, 100),
    "cpi": (50, 100_000),
    "income_median_gross": (10_000, 80_000),
    "income_monthly_arbeiter": (30, 5_000),
    "income_monthly_angestellte": (30, 5_000),
    "price_semmel": (0.02, 1),
    "price_vollmilch": (0.1, 2),
    "price_kinokarte": (0.5, 20),
    "price_benzin": (0.1, 3),
}

# Erwartete Abdeckung (erstes, letztes Jahr) laut data/SOURCES.md
COVERAGE = {
    "life_expectancy_birth_male": ("1951", "2025"),
    "life_expectancy_birth_female": ("1951", "2025"),
    "share_65plus": ("1961", "2025"),
    "median_age": ("1961", "2025"),
    "fertility_rate": ("1961", "2025"),
    "turnout_nrw": ("1919", "2024"),
    "cpi": ("1946", "2025"),
    "income_median_gross": ("1997", "2024"),
    "income_monthly_arbeiter": ("1953", "2009"),
    "income_monthly_angestellte": ("1953", "2009"),
    "price_semmel": ("1966", "2005"),
    "price_vollmilch": ("1966", "2005"),
    "price_kinokarte": ("1966", "2005"),
    "price_benzin": ("1966", "2005"),
}


@pytest.fixture(scope="module")
def indicators():
    return {ind["id"]: ind for ind in build.build_data()["indicators"]}


def test_all_mvp_indicators_present(indicators):
    assert set(indicators) == MVP_IDS


@pytest.mark.parametrize("id", sorted(MVP_IDS))
def test_required_fields(indicators, id):
    ind = indicators[id]
    for field in ("label", "unit", "description", "source", "source_url", "sources", "retrieved", "series"):
        assert ind[field], field
    assert all(s["label"] and s["url"].startswith("https://") for s in ind["sources"])
    assert "—" not in ind["label"] + ind["description"] + " ".join(ind["notes"])


@pytest.mark.parametrize("id", sorted(MVP_IDS))
def test_values_within_bounds(indicators, id):
    low, high = BOUNDS[id]
    values = [v for v in indicators[id]["series"].values() if v is not None]
    assert values
    assert all(low <= v <= high for v in values), (min(values), max(values))


@pytest.mark.parametrize("id", sorted(MVP_IDS))
def test_coverage(indicators, id):
    years = list(indicators[id]["series"])
    assert (years[0], years[-1]) == COVERAGE[id]
    assert years == sorted(years)


@pytest.mark.parametrize("id", sorted(MVP_IDS - {"turnout_nrw"}))
def test_yearly_series_contiguous_without_gaps(indicators, id):
    years = [int(y) for y in indicators[id]["series"]]
    assert years == list(range(years[0], years[-1] + 1))
    assert None not in indicators[id]["series"].values()


def test_to_series_rejects_duplicate_years():
    with pytest.raises(ValueError, match="1990"):
        to_series([(1990, 1.0), (1990, 2.0)])


def test_to_series_fills_gaps_with_null():
    assert to_series([(2000, 1.0), (2002, 3.0)]) == {"2000": 1.0, "2001": None, "2002": 3.0}
    assert to_series([(2000, 1.0), (2002, 3.0)], fill_gaps=False) == {"2000": 1.0, "2002": 3.0}


@pytest.mark.parametrize(
    "id, year, expected",
    [
        # Lebenserwartung-ODS, Blatt t420
        ("life_expectancy_birth_male", "1951", 62.38),
        ("life_expectancy_birth_female", "1951", 67.75),
        ("life_expectancy_birth_male", "1960", 65.4),
        ("life_expectancy_birth_female", "1960", 71.93),
        ("life_expectancy_birth_male", "2025", 80.1439193),
        ("life_expectancy_birth_female", "2025", 84.5791567),
        # Zeitreihen-ODS, Blätter I und 18
        ("share_65plus", "1961", 12.41447),
        ("share_65plus", "2025", 20.47161),
        ("median_age", "1961", 35.49087),
        ("median_age", "2025", 43.93757),
        ("fertility_rate", "1961", 2.784398),
        ("fertility_rate", "2025", 1.296487),
        # BMI-PDF Tabelle 6.a. und Endergebnis 2013
        ("turnout_nrw", "1945", 94.3),
        ("turnout_nrw", "1970", 91.8),
        ("turnout_nrw", "2008", 78.8),
        ("turnout_nrw", "2013", 74.90882),
        # OGD LHKI 38
        ("cpi", "1946", 106.8),
        ("cpi", "1990", 2839.9),
        ("cpi", "2025", 6633.4),
        # Einkommens-ODS, Tabelle1, Block Insgesamt, Bruttojahreseinkommen Median
        ("income_median_gross", "1997", 19808),
        ("income_median_gross", "2013", 25767),
        ("income_median_gross", "2024", 38043),
    ],
)
def test_sample_values_match_source(indicators, id, year, expected):
    assert indicators[id]["series"][year] == pytest.approx(expected, abs=1e-5)


def test_income_is_nominal_and_marked_for_cpi_conversion(indicators):
    ind = indicators["income_median_gross"]
    assert ind["deflate"] == "cpi"
    # Umrechnung braucht für jedes Einkommensjahr einen VPI-Wert
    assert set(ind["series"]) <= set(indicators["cpi"]["series"])


@pytest.mark.parametrize("group", ["arbeiter", "angestellte"])
def test_ak_income_break_1987(indicators, group):
    ind = indicators[f"income_monthly_{group}"]
    assert ind["breaks"] == [{"year": 1987, "before": "Juli-Wert, mit Lehrlingen"}]
    assert ind["deflate"] == "cpi"
    # 1987 = Jahresdurchschnitt (nach dem Bruch), nicht der Juli-Wert
    expected_1987 = {"arbeiter": 923, "angestellte": 1132}[group]
    assert ind["series"]["1987"] == expected_1987


def test_ak_csv_quartiles_ordered_and_years_unique_per_basis():
    rows = ak_rows()
    for r in rows:
        for g in ("arbeiter", "angestellte"):
            assert int(r[f"q1_{g}"]) <= int(r[f"median_{g}"]) <= int(r[f"q3_{g}"]), (r["jahr"], g)
    keys = [(r["jahr"], r["basis"]) for r in rows]
    assert len(keys) == len(set(keys))
    assert [r["jahr"] for r in rows].count("1987") == 2


# Unabhängige Tabellen im selben PDF: S. 16 „Medianeinkommen nach Bundesländer“, Zeile
# Österreich, und S. 4 „Verteilung der beitragspflichtigen Einkommen 2009“.
AK_CROSS_CHECK = {
    "arbeiter": {"1995": 1301, "2000": 1422, "2006": 1605, "2007": 1646, "2008": 1673, "2009": 1692},
    "angestellte": {"1995": 1600, "2000": 1751, "2006": 1995, "2007": 2048, "2008": 2094, "2009": 2148},
}
AK_2009_QUARTILES = {"arbeiter": (1194, 2169), "angestellte": (1377, 3169)}


@pytest.mark.parametrize("group", ["arbeiter", "angestellte"])
def test_ak_transcription_matches_other_tables(indicators, group):
    series = indicators[f"income_monthly_{group}"]["series"]
    for year, value in AK_CROSS_CHECK[group].items():
        assert series[year] == value, year
    row_2009 = next(r for r in ak_rows() if r["jahr"] == "2009")
    assert (int(row_2009[f"q1_{group}"]), int(row_2009[f"q3_{group}"])) == AK_2009_QUARTILES[group]


GOODS = ["semmel", "vollmilch", "kinokarte", "benzin"]


def test_vienna_prices_monthly_mean_matches_annual_average():
    """Bis Jahrgang 2003 ist das letzte Jahr auch monatlich abgedruckt; das Mittel muss passen."""
    rows = price_rows()
    groups = {}
    for r in rows:
        if r["monat"]:
            groups.setdefault((r["quelle"], r["ware"], r["jahr"]), []).append(float(r["wert"]))
    assert len(groups) == 9 * 4  # neun Jahrgänge mit Monatswerten, vier Waren
    mismatches = set()
    for (quelle, ware, jahr), months in groups.items():
        assert len(months) == 12, (quelle, ware, jahr)
        annual = next(
            float(r["wert"]) for r in rows
            if (r["quelle"], r["ware"], r["jahr"]) == (quelle, ware, jahr) and not r["monat"]
        )
        # Quelle rundet den Durchschnitt aus ungerundeten Monatswerten
        if abs(sum(months) / 12 - annual) > 0.006:
            mismatches.add((quelle, ware, jahr))
    assert mismatches == KNOWN_MONTHLY_MISMATCHES


# Quellinkonsistenz, am Scan geprüft: Monatswerte 3 x 5,15, 8 x 5,99, 1 x 5,97 (Mittel 5,78),
# Jahresdurchschnitt gedruckt 5,76. Siehe data/SOURCES.md.
KNOWN_MONTHLY_MISMATCHES = {("wien_preise_jb1974", "vollmilch", "1974")}


def test_vienna_prices_each_edition_complete():
    """Jeder Jahrgang liefert fünf Jahresdurchschnitte je Ware, Einheit einheitlich je Jahrgang."""
    rows = [r for r in price_rows() if not r["monat"]]
    for quelle in {r["quelle"] for r in rows}:
        edition = [r for r in rows if r["quelle"] == quelle]
        assert len({r["einheit"] for r in edition}) == 1, quelle
        for good in GOODS:
            years = sorted(int(r["jahr"]) for r in edition if r["ware"] == good)
            assert years == list(range(years[-1] - 4, years[-1] + 1)), (quelle, good)


@pytest.mark.parametrize("good", GOODS)
def test_vienna_prices_overlaps_agree_except_known_revisions(good):
    found = set(price_revisions(good))
    known = {year for g, year in KNOWN_REVISIONS if g == good}
    assert found == known, (good, price_revisions(good))


@pytest.mark.parametrize("good", GOODS)
def test_vienna_prices_schilling_and_euro_editions_agree(good):
    """Jahre, die in Schilling und in Euro abgedruckt sind (1998, 1999): Euro-Wert = Schilling / 13,7603, gerundet."""
    per_unit = price_by_unit(good)
    common = set(per_unit["ATS"]) & set(per_unit["EUR"])
    assert common == {1998, 1999}
    for year in common:
        ats = max(per_unit["ATS"][year])[1]
        eur = max(per_unit["EUR"][year])[1]
        # Quelle rechnet aus ungerundeten Schillingwerten um: Toleranz halber Cent plus Rundung des Schillingwerts
        assert abs(ats / ATS_PER_EUR - eur) <= 0.005 + 0.005 / ATS_PER_EUR + 1e-9, (good, year)


@pytest.mark.parametrize(
    "id, year, ats",
    [
        ("price_semmel", "1966", 0.62),
        ("price_semmel", "1980", 1.07),
        ("price_semmel", "1992", 2.29),
        ("price_vollmilch", "1970", 4.20),  # revidierter Wert
        ("price_vollmilch", "1986", 11.45),
        ("price_kinokarte", "1979", 40.38),
        ("price_kinokarte", "1987", 65.95),
        ("price_benzin", "1985", 11.20),
        ("price_benzin", "1999", 10.94),
    ],
)
def test_vienna_prices_schilling_years(indicators, id, year, ats):
    ind = indicators[id]
    assert ind["series_ats"][year] == pytest.approx(ats)
    assert ind["series"][year] == pytest.approx(ats / 13.7603)


@pytest.mark.parametrize(
    "id, year, eur",
    [
        ("price_semmel", "2005", 0.28),
        ("price_vollmilch", "2003", 0.70),
        ("price_kinokarte", "2004", 8.81),
        ("price_benzin", "2005", 1.02),
        ("price_kinokarte", "2000", 7.42),
    ],
)
def test_vienna_prices_euro_years(indicators, id, year, eur):
    assert year not in indicators[id]["series_ats"]
    assert indicators[id]["series"][year] == pytest.approx(eur)


def test_vienna_prices_breaks(indicators):
    assert indicators["price_benzin"]["breaks"][0]["year"] == 1987
    assert indicators["price_vollmilch"]["breaks"][0]["year"] == 1974
    assert "breaks" not in indicators["price_semmel"]


def test_turnout_is_event_series(indicators):
    ind = indicators["turnout_nrw"]
    assert ind["type"] == "event"
    elections_since_1945 = [y for y in ind["series"] if int(y) >= 1945]
    assert len(elections_since_1945) == 24


# Veränderungszeile der BMI-Tabelle passt hier nicht zu den Absolutwerten (Quellinkonsistenz,
# siehe Anmerkung in der CSV und data/SOURCES.md).
KNOWN_ELIGIBLE_DIFF_MISMATCH = {"2008-09-28"}


def test_turnout_manual_csv_internally_consistent():
    rows = manual_rows()
    previous = None
    for r in rows:
        eligible, cast = int(r["wahlberechtigte"]), int(r["abgegeben"])
        assert int(r["ungueltig"]) + int(r["gueltig"]) == cast, r["wahltag"]
        assert cast / eligible * 100 == pytest.approx(float(r["abgegeben_pct"]), abs=0.05), r["wahltag"]
        if previous:
            diff = eligible - int(previous["wahlberechtigte"])
            if r["wahltag"] in KNOWN_ELIGIBLE_DIFF_MISMATCH:
                assert diff != int(r["veraenderung_wahlberechtigte"]), "Ausnahme nicht mehr nötig"
            else:
                assert diff == int(r["veraenderung_wahlberechtigte"]), r["wahltag"]
            assert cast - int(previous["abgegeben"]) == int(r["veraenderung_abgegeben"])
        previous = r


def test_turnout_ratio_matches_published_percentage_2013():
    eligible, cast, pct = xlsx_result(2013)
    assert cast / eligible * 100 == pytest.approx(pct, abs=1e-9)


@pytest.mark.parametrize("year", sorted(XLSX))
def test_turnout_xlsx_reads_austria_totals(year):
    eligible, cast, _ = xlsx_result(year)
    assert 6_000_000 < eligible < 7_000_000
    assert 0.7 < cast / eligible < 0.85


def test_cpi_matches_control_file_from_1990(indicators):
    rows = read_ods(SOURCES["vpi_ab_1990"].path)["VPI"]
    header = next(r for r in rows if "LHKI (38)" in r)
    col = header.index("LHKI (38)")
    control = {
        r[0].removeprefix("Ø").strip(): r[col]
        for r in rows
        if r and isinstance(r[0], str) and r[0].startswith("Ø")
    }
    series = indicators["cpi"]["series"]
    checked = 0
    for label, value in control.items():
        year = label if len(label) == 4 else "20" + label  # "Ø 25" steht für 2025
        if year in series:
            assert series[year] == pytest.approx(value, abs=1e-6), year
            checked += 1
    assert checked >= 35


def test_life_expectancy_matches_zeitreihen_from_1961(indicators):
    rows = read_ods(SOURCES["zeitreihen"].path)["I"]
    from readers import ods_year_row

    for id, label in (("life_expectancy_birth_male", "Männer"), ("life_expectancy_birth_female", "Frauen")):
        for year, value in ods_year_row(rows, label, after="Sterbefälle absolut"):
            # Lange Reihe bis 2001 auf zwei Nachkommastellen gerundet
            assert indicators[id]["series"][str(year)] == pytest.approx(value, abs=0.006), (id, year)
