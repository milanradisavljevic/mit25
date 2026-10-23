"""Leser für ODS, XLSX und OGD-CSV, nur Standardbibliothek.

Die Dateien stammen von Statistik Austria und dem BMI (siehe data/SOURCES.md).
"""

import csv
import re
import zipfile
import xml.etree.ElementTree as ET
from functools import lru_cache

_T = "{urn:oasis:names:tc:opendocument:xmlns:table:1.0}"
_O = "{urn:oasis:names:tc:opendocument:xmlns:office:1.0}"
_X = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
_R = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
_PR = "{http://schemas.openxmlformats.org/package/2006/relationships}"

# Leere Zellen am Zeilenende sind oft tausendfach "wiederholt"; nur so weit auffüllen.
_MAX_EMPTY_REPEAT = 1024


def _ods_cell(cell):
    if cell.get(_O + "value-type") in ("float", "percentage", "currency"):
        return float(cell.get(_O + "value"))
    return "\n".join("".join(p.itertext()) for p in cell if p.tag.endswith("}p"))


@lru_cache(maxsize=None)
def read_ods(path):
    """Liefert {Blattname: [[Zelle, ...], ...]}. Zahlen als float, sonst str."""
    with zipfile.ZipFile(path) as z:
        root = ET.fromstring(z.read("content.xml"))
    sheets = {}
    for table in root.iter(_T + "table"):
        rows = []
        for row in table.iter(_T + "table-row"):
            cells = []
            for cell in row:
                if cell.tag not in (_T + "table-cell", _T + "covered-table-cell"):
                    continue
                value = _ods_cell(cell)
                repeat = int(cell.get(_T + "number-columns-repeated", "1"))
                if value == "":
                    repeat = min(repeat, _MAX_EMPTY_REPEAT)
                cells.extend([value] * repeat)
            while cells and cells[-1] == "":
                cells.pop()
            repeat = int(row.get(_T + "number-rows-repeated", "1"))
            rows.extend([cells] * (repeat if cells else 1))
        sheets[table.get(_T + "name")] = rows
    return sheets


def _is_year(value):
    return isinstance(value, float) and value.is_integer() and 1800 <= value <= 2100


def _label(value):
    return value.strip() if isinstance(value, str) else value


def ods_year_row(rows, label, after=None):
    """Zeitreihe aus einem Blatt mit Jahren als Spalten.

    Sucht die Kopfzeile mit den Jahren, dann die erste Zeile mit Beschriftung
    `label` in Spalte A, die nach einer Zeile mit `after` (beliebige Spalte) steht.
    Liefert [(Jahr, Wert oder None), ...]; nicht-numerische Zellen ("." usw.) werden None.
    """
    header = next(
        r for r in rows if len(r) > 3 and r[0] == "" and all(_is_year(v) for v in r[1:])
    )
    start = 0
    if after is not None:
        start = next(i for i, r in enumerate(rows) if after in map(_label, r))
    row = next(r for r in rows[start:] if r and _label(r[0]) == label)
    pairs = []
    for i, year in enumerate(header[1:], start=1):
        value = row[i] if i < len(row) else ""
        pairs.append((int(year), value if isinstance(value, float) else None))
    return pairs


@lru_cache(maxsize=None)
def read_xlsx(path):
    """Liefert {Blattname: [{Spalte: Wert}, ...]} in Blattreihenfolge. Zahlen als float."""
    with zipfile.ZipFile(path) as z:
        names = set(z.namelist())
        shared = []
        if "xl/sharedStrings.xml" in names:
            for si in ET.fromstring(z.read("xl/sharedStrings.xml")).iter(_X + "si"):
                shared.append("".join(t.text or "" for t in si.iter(_X + "t")))
        rels = {
            r.get("Id"): r.get("Target")
            for r in ET.fromstring(z.read("xl/_rels/workbook.xml.rels")).iter(_PR + "Relationship")
        }
        sheets = {}
        for sheet in ET.fromstring(z.read("xl/workbook.xml")).iter(_X + "sheet"):
            target = rels[sheet.get(_R + "id")].lstrip("/")
            if not target.startswith("xl/"):
                target = "xl/" + target
            rows = []
            for row in ET.fromstring(z.read(target)).iter(_X + "row"):
                values = {}
                for c in row.iter(_X + "c"):
                    col = re.match(r"[A-Z]+", c.get("r")).group()
                    kind = c.get("t")
                    v = c.find(_X + "v")
                    if kind == "inlineStr":
                        values[col] = "".join(t.text or "" for t in c.iter(_X + "t"))
                    elif v is None:
                        continue
                    elif kind == "s":
                        values[col] = shared[int(v.text)]
                    elif kind in ("str", "e"):
                        values[col] = v.text
                    else:
                        values[col] = float(v.text)
                rows.append(values)
            sheets[sheet.get("name")] = rows
    return sheets


def read_ogd_csv(path):
    """OGD-CSV von data.statistik.gv.at: Semikolon, Dezimalkomma. Liefert Liste von dicts."""
    with open(path, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f, delimiter=";"))


def parse_decimal_comma(text):
    return float(text.replace(",", "."))
