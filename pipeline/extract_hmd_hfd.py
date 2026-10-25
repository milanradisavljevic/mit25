"""Erzeugt data/extract/hmd_hfd_oesterreich.csv aus den lokalen HMD/HFD-Dateien.

Die Rohdateien (data/raw/hmd_AUT/, data/raw/hfd_AUT/) sind nur nach Registrierung
erhältlich und nicht im Repository. Dieser Auszug enthält nur die für mit25 nötigen
Jahreswerte Österreichs und wird eingecheckt (HMD und HFD: CC BY 4.0, mit Quellenangabe).

Spalten: jahr, e0_total, e0_female, e0_male (HMD E0per), tfr (HFD tfrRR),
share_65plus und median_age (aus HMD Exposures_1x1, Personenjahre je Altersjahr,
entspricht der Bevölkerung im Jahresdurchschnitt).

Medianalter: Alter a, bei dem die kumulierte Bevölkerung 50 % erreicht, linear
innerhalb des Altersjahres: a + (N/2 - kumuliert bis a) / Bevölkerung im Alter a.
"""

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HMD = ROOT / "data" / "raw" / "hmd_AUT" / "AUT" / "STATS"
HFD = ROOT / "data" / "raw" / "hfd_AUT"
OUTPUT = ROOT / "data" / "extract" / "hmd_hfd_oesterreich.csv"


def _rows(path, skip):
    with open(path, encoding="utf-8") as f:
        lines = f.read().splitlines()[skip:]
    return [line.split() for line in lines if line.strip()]


def life_expectancy():
    return {int(r[0]): {"e0_female": r[1], "e0_male": r[2], "e0_total": r[3]} for r in _rows(HMD / "E0per.txt", 3)}


def fertility():
    return {int(r[0]): {"tfr": r[1]} for r in _rows(HFD / "AUTtfrRR.txt", 3)}


def exposures():
    """{Jahr: [(Alter, Personenjahre gesamt), ...]}; '110+' als 110."""
    result = {}
    for r in _rows(HMD / "Exposures_1x1.txt", 3):
        year, age, total = int(r[0]), int(r[1].rstrip("+")), float(r[4])
        result.setdefault(year, []).append((age, total))
    return result


def share_65plus(ages):
    total = sum(n for _, n in ages)
    return sum(n for a, n in ages if a >= 65) / total * 100


def median_age(ages):
    half = sum(n for _, n in ages) / 2
    cumulative = 0.0
    for age, n in sorted(ages):
        if cumulative + n >= half:
            return age + (half - cumulative) / n
        cumulative += n
    raise ValueError("Median nicht gefunden")


def build_rows():
    e0, tfr, exp = life_expectancy(), fertility(), exposures()
    rows = []
    for year in sorted(set(e0) | set(tfr) | set(exp)):
        row = {"jahr": year, **e0.get(year, {}), **tfr.get(year, {})}
        if year in exp:
            row["share_65plus"] = f"{share_65plus(exp[year]):.4f}"
            row["median_age"] = f"{median_age(exp[year]):.4f}"
        rows.append(row)
    return rows


def main():
    if not HMD.exists() or not HFD.exists():
        sys.exit("HMD/HFD-Rohdaten fehlen (Registrierung nötig, siehe data/SOURCES.md).")
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    fields = ["jahr", "e0_total", "e0_female", "e0_male", "tfr", "share_65plus", "median_age"]
    with open(OUTPUT, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        w.writeheader()
        w.writerows(build_rows())
    print(f"{OUTPUT.relative_to(ROOT)} geschrieben")


if __name__ == "__main__":
    main()
