# Datenquellen

Alle Dateien liegen unverändert in `data/raw/`. Abrufdatum aller Dateien: **2026-10-23**.
Abdeckung wurde direkt aus den heruntergeladenen Dateien ermittelt, nicht aus Sekundärquellen.

## Übersicht

| ID | Quelle | Jahre | Lücken |
|---|---|---|---|
| life_expectancy_birth | Statistik Austria | 1961–2025 (gesamt), 1951–2025 (nach Geschlecht) | keine innerhalb der Spanne |
| share_65plus | Statistik Austria | 1961–2025 | keine innerhalb der Spanne |
| median_age | Statistik Austria | 1961–2025 | keine innerhalb der Spanne |
| fertility_rate | Statistik Austria | 1961–2025 | keine innerhalb der Spanne |
| turnout_nrw | BMI | 1945–2024 (24 Wahlen), zusätzlich 1919–1930 | Ereignisreihe |
| cpi | Statistik Austria (OGD) | 1946–2025 (Jahresdurchschnitt) | 1946 nur April bis Dezember |

---

## Statistik Austria: Demographische Zeitreihenindikatoren

- **Datei:** `statistik_austria_OEsterreich_Zeitreihenindikatoren_1961_2025.ods`
- **URL:** https://www.statistik.at/fileadmin/pages/411/OEsterreich_Zeitreihenindikatoren_1961_2025.ods
- **Seite:** https://www.statistik.at/statistiken/bevoelkerung-und-soziales/bevoelkerung/demographische-indikatoren-und-tafeln/demographische-zeitreihenindikatoren
- **Quellvermerk in der Datei:** „Q: STATISTIK AUSTRIA, Demographische Indikatoren. Erstellt am 14.09.2026.“
- **Abdeckung:** 1961–2025, jährlich, alle benötigten Zeilen vollständig numerisch (65 Werte je Zeile).

Verwendete Zeilen:

| ID | Blatt | Zeile |
|---|---|---|
| life_expectancy_birth | I | „Lebenserwartung bei der Geburt“ → „Männer und Frauen (Unisex-Werte)“ (auch „Männer“, „Frauen“) |
| fertility_rate | I | „Gesamtfertilitätsrate (Kinderzahl pro Frau)“ |
| share_65plus | 18 | Block „Männer und Frauen“ → „65 Jahre und älter“ (Bevölkerung im Jahresdurchschnitt, %) |
| median_age | 18 | Block „Männer und Frauen“ → „Medianalter“ (Bevölkerung im Jahresdurchschnitt) |

Methodische Hinweise aus der Datei:
- Blatt 18: „Ab 2004 ungerundete Werte.“ Davor sind die Werte gerundet.
- Blatt I: „Ab 2009 inklusive nicht in Österreich verstorbene Personen mit Hauptwohnsitz in Österreich. Ab 2015 inklusive nicht in Österreich Geborene von Müttern mit Wohnsitz in Österreich.“ Betrifft Lebenserwartung und Fertilität.
- Blatt II enthält dieselben Altersanteile auch für den Bevölkerungsstand am Jahresende. Gewählt: Jahresdurchschnitt (Blatt 18), weil das Medianalter nur dort steht.

## Statistik Austria: Lebenserwartung lange Reihe

- **Datei:** `statistik_austria_Lebenserwartung_fuer_ausgewaehlte_Altersjahre_1868_71_bis_2020_22_sowie_1951_2025.ods`
- **URL:** https://www.statistik.at/fileadmin/pages/413/Lebenserwartung_fuer_ausgewaehlte_Altersjahre_1868_71_bis_2020_22_sowie_1951_2025.ods
- **Seite:** https://www.statistik.at/statistiken/bevoelkerung-und-soziales/bevoelkerung/demographische-indikatoren-und-tafeln/sterbetafeln
- **Abdeckung:** jährlich 1951–2025, alle 75 Jahre vorhanden, **nur getrennt nach Männern und Frauen** (kein Gesamtwert). Davor nur Periodentafeln um Volkszählungen (1868/71, …, 1930/33, 1949/51), die keinem Einzeljahr zugeordnet werden dürfen.
- **Abgleich:** 1961 Männer 66,47 (hier) vs. 66,474… (Zeitreihenindikatoren). Stimmt überein, hier gerundet.

## BMI: Wahlbeteiligung Nationalratswahlen

Wahlbeteiligung = abgegebene Stimmen (inkl. ungültige) in % der Wahlberechtigten. Das ist die Definition aus der BMI-Tabelle.

### 1919–2008

- **Datei:** `bmi_nrw_08_wbseit1919.pdf` (Tabelle „6.a. Wahlberechtigte seit 1919“, Seite 333)
- **URL:** https://www.bmi.gv.at/412/Nationalratswahlen/Nationalratswahl_2008/files/history/nrw_08_wbseit1919.pdf
- **Inhalt:** je Wahl Wahlberechtigte, abgegebene Stimmen absolut und in %.
- **Wahlen ab 1945:** 1945, 1949, 1953, 1956, 1959, 1962, 1966, 1970, 1971, 1975, 1979, 1983, 1986, 1990, 1994, 1995, 1999, 2002, 2006, 2008.
- **Quellfehler:** Die 1970er-Zeile ist als „1. März 1966“ beschriftet. Fußnote 3 („Wiederholungswahl vom 4. Oktober 1970“) und die Differenzzeile „1970“ zeigen, dass die Wahl 1970 gemeint ist. Ich behandle sie als 1970 und vermerke das im Indikator.
- **Fußnoten:** 1970 inkl. Wiederholungswahl in Wiener Wahlkreisen. 1995 inkl. Wiederholungswahl vom 13.10.1996.

### 2013–2024

| Wahl | Datei | URL |
|---|---|---|
| 2013 | `bmi_nrw13_endgueltiges_gesamtergebnis.xlsx` | https://www.bmi.gv.at/412/Nationalratswahlen/Nationalratswahl_2013/files/nrw13_endgueltiges_gesamtergebnis.xlsx |
| 2017 | `bmi_nrw17_endgueltiges_gesamtergebnis.xlsx` | https://www.bmi.gv.at/412/Nationalratswahlen/Nationalratswahl_2017/files/nrw17_endgueltiges_gesamtergebnis.xlsx |
| 2019 | `bmi_nrw19_endgultiges_gesamtergebnis_16102019.xlsx` | https://www.bmi.gv.at/412/Nationalratswahlen/Nationalratswahl_2019/files/endgultiges_gesamtergebnis_nrw19_16102019.xlsx |
| 2024 | `bmi_nrw24_endgueltiges_ergebnis_16102024.xlsx` | https://www.bmi.gv.at/412/Nationalratswahlen/Nationalratswahl_2024/files/endgueltiges_ergebnis_beschluss_bundeswahlbehoerde_16102024.xlsx |

Jeweils Zeile `GKZ = G00000` („Österreich“). 2013 enthält eine fertige Spalte „Wahlbeteiligung in %“. 2017, 2019 und 2024 enthalten nur „Wahlberechtigte“ und „Abgegebene“ (siehe offene Frage 2).

## Statistik Austria: Verbraucherpreisindex

### Hauptreihe: Lebenshaltungskostenindex 1938 (verkettet), OGD

- **Datei:** `statistik_austria_OGD_vpilhki38_VPI_LHKI38_1.csv` plus Metadaten `…_HEADER.csv`, `…_C-VPIZR-0.csv`, `…_C-VPI1-0.csv`
- **URL:** https://data.statistik.gv.at/data/OGD_vpilhki38_VPI_LHKI38_1.csv
- **Katalog:** https://data.statistik.gv.at/web/catalog.jsp (Datensatz `OGD_vpilhki38_VPI_LHKI38_1`)
- **Inhalt:** Gesamtindex (VPI-0), Basis März 1938 = 100. Monatswerte April 1946 bis September 2026 und offizielle Jahresdurchschnitte (Codes `VPIZR-JJJJ`, Metadaten: „Jahresdurchschnitt JJJJ“).
- **Abdeckung Jahresdurchschnitt:** 1946–2025, keine Lücke. 1946 beruht nur auf April bis Dezember (9 Monate).
- **Format:** Semikolon-getrennt, Dezimalkomma.

### Kontrollreihe

- **Datei:** `statistik_austria_2_Verbraucherpreisindizes_ab_1990.ods`
- **URL:** https://www.statistik.at/fileadmin/pages/214/2_Verbraucherpreisindizes_ab_1990.ods
- **Zweck:** Abgleich. Jahresdurchschnitte ab 1990 für alle Basen. Spalte „LHKI (38)“: 1990 = 2839,9, 2025 = 6633,4. Stimmt mit der OGD-Datei überein.

---

## Geprüft und verworfen

| Quelle | Grund |
|---|---|
| Statistik Austria `AEST_Bev_Alter_Geschl_Bundesl_seit_1869.ods` | Nur Volkszählungsjahre (vor 1961 nur 1951), kein Medianalter. 65+-Anteil müsste berechnet werden. |
| Eurostat `demo_find`, `demo_pjanind` (AT) | Beginnt 1960, nur ein Jahr Gewinn. Werte gerundet, Medianalter 1960–1962 identisch 35,5. |
| WKO/Landes-PDFs | Sekundärquellen, Original von Statistik Austria vorhanden. |

## Offene Probleme und Fragen

1. **Großeltern-Spalte reicht weiter zurück als die Daten.** Bei Standardabstand 60 Jahre gilt für Geburtsjahre 1960–2005 bei den Großeltern das Stichjahr 1925–1970. Bei den Eltern ist es 1955–2000. Datenlage vor 1961:
   - Anteil 65+, Medianalter, Fertilität: **keine Jahreswerte vor 1961** bei Statistik Austria gefunden. Großeltern-Spalte bleibt bis Geburtsjahr ~1995 dort leer.
   - Lebenserwartung: ab 1951, aber nur nach Geschlecht.
   - VPI: ab 1946.
   - Wahlen: ab 1945. 1919–1930 ebenfalls in der Datei (siehe Punkt 4).
   - Die Annahme „Daten ab etwa 1950“ im Plan reicht also nicht für Geburtsjahre vor ~1985.
2. **Wahlbeteiligung 2017/2019/2024 berechnen?** Die BMI-Dateien enthalten keine Prozentzahl, nur Wahlberechtigte und abgegebene Stimmen. Vorschlag: in der Pipeline `abgegeben / wahlberechtigt × 100` rechnen. Das ist eine Division von Quellwerten, keine Schätzung. Test gegen 2008 (PDF: 78,8 %) und 2013 (Excel: 74,9 %).
3. **Lebenserwartung 1951–1960 nur nach Geschlecht.** Möglichkeiten:
   - (a) Frontend zeigt Männer/Frauen getrennt, für alle Jahre. Dann lückenlos 1951–2025.
   - (b) Nur Gesamtwert ab 1961.
   Einen Gesamtwert selbst zu berechnen ist nicht zulässig, weil das kein einfacher Mittelwert ist.
4. **Wahlen der Ersten Republik (1919–1930)** sind in derselben BMI-Datei. Sollen sie für Stichjahre 1925–1933 (±3 Jahre) verwendet werden? Datenlage 1931–1944 sonst leer.
5. **Fertilität 1951–1960:** Kandidat ist die Human Fertility Database (humanfertility.org). Sie enthält laut Dokumentation Geburten nach Alter der Mutter ab 1951 für Österreich. Download erfordert eine kostenlose Registrierung, also manuellen Download. Noch nicht geprüft.
6. **PDF-Auslesen:** Für die BMI-Tabelle 1919–2008 ist kein PDF-Werkzeug installiert (kein `pdftotext`). Optionen:
   - (a) neue Abhängigkeit `pypdf`
   - (b) die 24 Zeilen einmalig als `data/manual/bmi_wahlbeteiligung_1919_2008.csv` abtippen, mit Verweis auf PDF-Seite 333 und Test gegen die absoluten Zahlen (Prozent = abgegeben / wahlberechtigt).
7. **Methodenbrüche** müssen im Frontend erwähnt werden: gerundete Werte vor 2004, Erweiterung der Sterbe- und Geburtenzählung 2009/2015, Basiswechsel im VPI (verkettet, unkritisch). Bei der Wahlbeteiligung sind Änderungen von Wahlalter und Wahlpflicht in einzelnen Ländern **zu prüfen**, nicht aus dem Gedächtnis eintragen.
8. **VPI-Umrechnung in Euro** (Phase 5): Für Schilling-Preise ist zusätzlich der fixe Umrechnungskurs ATS/EUR nötig. Dafür braucht es eine Quelle in SOURCES.md.
