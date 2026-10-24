# Datenquellen

Alle Dateien liegen unverändert in `data/raw/`. Abrufdatum aller Dateien: **2026-10-23**.
Abdeckung wurde direkt aus den heruntergeladenen Dateien ermittelt, nicht aus Sekundärquellen.

## Übersicht

| ID | Quelle | Jahre | Lücken |
|---|---|---|---|
| life_expectancy_birth_male, life_expectancy_birth_female | Statistik Austria | 1951–2025 | keine innerhalb der Spanne |
| share_65plus | Statistik Austria | 1961–2025 | keine innerhalb der Spanne |
| median_age | Statistik Austria | 1961–2025 | keine innerhalb der Spanne |
| fertility_rate | Statistik Austria | 1961–2025 | keine innerhalb der Spanne |
| turnout_nrw | BMI | 1945–2024 (24 Wahlen), zusätzlich 1919–1930 | Ereignisreihe |
| cpi | Statistik Austria (OGD) | 1946–2025 (Jahresdurchschnitt) | 1946 nur April bis Dezember |
| income_median_gross (Phase 5) | Statistik Austria | 1997–2024 | keine innerhalb der Spanne |
| income_monthly_arbeiter, income_monthly_angestellte (Phase 5) | AK Wien / Hauptverband | 1953–2009 | Methodenbruch 1987, Reihe eingestellt |
| price_semmel, price_vollmilch, price_kinokarte, price_benzin (Phase 5) | Statistisches Jahrbuch der Stadt Wien (ÖSTAT, Wiener Preise) | 1966–2005 | keine; Brüche Milch 1974, Benzin 1987; Tabelle eingestellt |
| rent_share_income (Phase 5) | Eurostat EU-SILC | 2003–2025 | Bruch 2008 |
| rent_avg (Phase 5) | Statistik Austria, Mikrozensus | 2005–2025 | Bruch 2021 |
| wage_industry_vienna (Phase 5) | Statistisches Jahrbuch der Stadt Wien (Wirtschaftskammer) | 1987–2005 | Bruch 2004; Grundlage der Arbeitsminuten |

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
| (nur Kontrolle) | I | „Lebenserwartung bei der Geburt“ → „Männer“, „Frauen“: Test gegen die lange Reihe ab 1961 |
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
- **Verwendet für:** `life_expectancy_birth_male`, `life_expectancy_birth_female` (Blatt t420, Spalten „Männer“/„Frauen“ → „0 (bei der Geburt)“, Zeilen mit Einzeljahr).
- **Abdeckung:** jährlich 1951–2025, alle 75 Jahre vorhanden, **nur getrennt nach Männern und Frauen** (kein Gesamtwert). Davor nur Periodentafeln um Volkszählungen (1868/71, …, 1930/33, 1949/51), die keinem Einzeljahr zugeordnet werden dürfen.
- **Rundung:** bis 2001 zwei Nachkommastellen, ab 2002 ungerundet.
- **Abgleich:** 1961–2025 gegen Blatt I der Zeitreihenindikatoren, Abweichung höchstens 0,006 (Rundung). Wird getestet.

## BMI: Wahlbeteiligung Nationalratswahlen

Wahlbeteiligung = abgegebene Stimmen (inkl. ungültige) in % der Wahlberechtigten. Das ist die Definition aus der BMI-Tabelle.

### 1919–2008

- **Datei:** `bmi_nrw_08_wbseit1919.pdf` (Tabelle „6.a. Wahlberechtigte seit 1919“, Seite 333)
- **Abschrift:** `data/manual/bmi_wahlbeteiligung_1919_2008.csv`, am 2026-10-23 aus der Textebene des PDFs abgetippt. Enthält Wahlberechtigte, abgegeben (absolut und %), ungültig, gültig sowie die beiden Veränderungsspalten. Tests prüfen: ungültig + gültig = abgegeben; Prozent = abgegeben / wahlberechtigt (±0,05); Differenzen zur Vorwahl = Veränderungstabelle.
- **Zweiter Quellfehler:** Die Veränderung der Wahlberechtigten 2008 beträgt laut Tabelle 225.217. Aus den Absolutwerten ergibt sich 6.333.109 − 6.107.686 = 225.423. Der Absolutwert 2008 ist konsistent (Männer + Frauen). Die Wahlbeteiligung ist nicht betroffen. Im Test als bekannte Ausnahme geführt.
- **URL:** https://www.bmi.gv.at/412/Nationalratswahlen/Nationalratswahl_2008/files/history/nrw_08_wbseit1919.pdf
- **Inhalt:** je Wahl Wahlberechtigte, abgegebene Stimmen absolut und in %.
- **Wahlen ab 1945:** 1945, 1949, 1953, 1956, 1959, 1962, 1966, 1970, 1971, 1975, 1979, 1983, 1986, 1990, 1994, 1995, 1999, 2002, 2006, 2008.
- **Quellfehler:** Die 1970er-Zeile ist als „1. März 1966“ beschriftet. Fußnote 3 („Wiederholungswahl vom 4. Oktober 1970“) und die Differenzzeile „1970“ zeigen, dass die Wahl 1970 gemeint ist. Ich behandle sie als 1970 und vermerke das im Indikator.
- **Fußnoten:** 1970 inkl. Wiederholungswahl in Wiener Wahlkreisen. 1995 inkl. Wiederholungswahl vom 13.10.1996.

### Wahlrecht: Hinweise zu Wahlalter und Wahlpflicht

- `parlament_news_2024-09-12_wahlsystem_entwicklung.html` (https://www.parlament.gv.at/aktuelles/news/Wie-sich-das-oesterreichische-Wahlsystem-entwickelte/): Tabelle mit dem aktiven Wahlalter 1970: 19, 1992: 18, 2007: 16.
- `parlament_pk_2024-0874_wahlrecht_ueberholte_regelungen.html` (Parlamentskorrespondenz Nr. 874/2024): Wahlpflicht in Tirol und Vorarlberg ab 1919, Steiermark ab 1949, Kärnten ab 1986; 1992 bei Nationalratswahlen für alle Bundesländer aufgehoben.
- Erscheint als Hinweis im Quellen-Panel der Wahlbeteiligung. Ab wann genau welches Wahlalter galt (Gesetzesdatum), ist nicht belegt und deshalb nicht angegeben.

### 2013–2024

| Wahl | Datei | URL |
|---|---|---|
| 2013 | `bmi_nrw13_endgueltiges_gesamtergebnis.xlsx` | https://www.bmi.gv.at/412/Nationalratswahlen/Nationalratswahl_2013/files/nrw13_endgueltiges_gesamtergebnis.xlsx |
| 2017 | `bmi_nrw17_endgueltiges_gesamtergebnis.xlsx` | https://www.bmi.gv.at/412/Nationalratswahlen/Nationalratswahl_2017/files/nrw17_endgueltiges_gesamtergebnis.xlsx |
| 2019 | `bmi_nrw19_endgultiges_gesamtergebnis_16102019.xlsx` | https://www.bmi.gv.at/412/Nationalratswahlen/Nationalratswahl_2019/files/endgultiges_gesamtergebnis_nrw19_16102019.xlsx |
| 2024 | `bmi_nrw24_endgueltiges_ergebnis_16102024.xlsx` | https://www.bmi.gv.at/412/Nationalratswahlen/Nationalratswahl_2024/files/endgueltiges_ergebnis_beschluss_bundeswahlbehoerde_16102024.xlsx |

Jeweils Zeile `GKZ = G00000` („Österreich“). 2013 enthält eine fertige Spalte „Wahlbeteiligung in %“ (verwendet). 2017, 2019 und 2024 enthalten nur „Wahlberechtigte“ und „Abgegebene“. Dort rechnet die Pipeline abgegeben / wahlberechtigt × 100. Für 2013 liefert diese Rechnung exakt den veröffentlichten Wert (Test).

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

## Statistik Austria: Einkommen (Phase 5)

- **Datei:** `statistik_austria_1_brutto-_und_nettojahreseinkommen_der_unselbstaendig_erwerbstaetigen_1997_bis_2024_020054.ods`
- **URL:** https://www.statistik.at/fileadmin/pages/333/1_brutto-_und_nettojahreseinkommen_der_unselbstaendig_erwerbstaetigen_1997_bis_2024_020054.ods
- **Seite:** https://www.statistik.at/statistiken/bevoelkerung-und-soziales/einkommen-und-soziale-lage/jaehrliche-personeneinkommen
- **Quellvermerk:** „Q: STATISTIK AUSTRIA, Lohnsteuerdaten - Sozialstatistische Auswertungen. Erstellt am 12.12.2025.“
- **Verwendet:** Blatt Tabelle1, Block „Insgesamt“, Bruttojahreseinkommen → „Median“.
- **Abdeckung:** 1997–2024, jährlich, ohne Lücken.
- **Definition laut Fußnoten:** ohne Lehrlinge. Bruttojahresbezüge gemäß § 25 EStG. Enthält Teilzeit und nicht ganzjährig Beschäftigte.
- **Währung:** Der Spaltenkopf lautet „EUR-ATS bzw. Euro“. 1997–2001 sind also Schilling-Werte, in der Quelle in Euro umgerechnet.
- **Kaufkraft:** Das Frontend rechnet zusätzlich in Preise des letzten VPI-Jahres um: Wert × VPI(2025) / VPI(Jahr), mit den Jahresdurchschnitten aus `cpi`. data.json enthält nur die Nominalwerte.
- **Stichprobe:** 2013 = 25.767 €. Derselbe Wert steht im Einkommensbericht 2016 des Rechnungshofs, laut Websuche, nicht als Datei geprüft.
- **Nicht verwendet:** Tabelle 2 (ganzjährig Vollzeitbeschäftigte, 2004–2024) wurde geprüft und wieder entfernt, weil sie erst 2004 beginnt.

### AK Wien: Monatseinkommen 1953–2009 (Phase 5)

- **Datei:** `ak_wien_bruttoeinkommen_arbeiter_angestellte_2009.pdf`
- **URL:** https://www.arbeiterkammer.at/infopool/akportal/Studie_Einkommen_2009.pdf
- **Titel:** AK Wien, „Die Bruttoeinkommen von Arbeitern und Angestellten im Jahr 2009“ (Statistische Informationen, September 2010)
- **Abschrift:** `data/manual/ak_bruttomonatseinkommen_1953_2009.csv`. Stammt aus der Tabelle „Bruttoeinkommen der unselbständig Beschäftigten“, gedruckte Seite 28 (PDF-Seite 31), mit 1. Quartil, Median und 3. Quartil für Arbeiter und Angestellte. 1987 steht zweimal drin, Spalte `basis` unterscheidet die beiden Erhebungsarten.
- **Prüfung der Abschrift (Tests):**
  - In jeder Zeile gilt Q1 ≤ Median ≤ Q3.
  - Die Mediane für 1995, 2000 und 2006–2009 stimmen mit S. 16 überein (Bundesländer, Zeile Österreich).
  - Die Quartile 2009 stimmen mit S. 4 überein (Verteilung 2009).
- **Indikatoren:** `income_monthly_arbeiter` und `income_monthly_angestellte`, jeweils 1953–2009. Bis 1986 gilt der Juli-Wert, ab 1987 der Jahresdurchschnitt. Der Bruch steht im Feld `breaks`, dort wird die Linie getrennt. Die Reihe endet 2009 (Feld `ended`); spätere Stichjahre zeigen „Reihe endet 2009“.
- **Kaufkraft:** Wie beim Jahreseinkommen rechnet das Frontend in Preise von 2025 um.

Eigenschaften der Quelle:
- **Inhalt:** Median der Bruttomonatseinkommen 1953–2009 nach Daten des Hauptverbands der Sozialversicherungsträger.
- **Kein Gesamtwert:** nur getrennt nach Arbeitern und Angestellten. Ein Gesamt-Median lässt sich daraus nicht bilden.
- **Methodenbruch 1987:** bis 1987 jeweils Juli, einschließlich Lehrlinge; ab 1987 Jahresdurchschnitt ohne Lehrlinge. 1987 ist in beiden Varianten angegeben.
- **Begrenzung:** Werte ohne Sonderzahlungen (1/14 des Jahreseinkommens). Einkommen über der Höchstbeitragsgrundlage nicht ausgewiesen. Alle Jahre mit 13,7603 ATS/EUR umgerechnet.
- **Nicht mit den Lohnsteuerdaten vergleichbar:** Monats- statt Jahreseinkommen, Sozialversicherungs- statt Steuerdaten. Darf nicht zu einer Linie verbunden werden.
- **Quelle selbst:** Sekundärquelle. Die AK veröffentlicht die Daten des Hauptverbands.

---

## Geprüft und verworfen

| Quelle | Grund |
|---|---|
| Statistik Austria `AEST_Bev_Alter_Geschl_Bundesl_seit_1869.ods` | Nur Volkszählungsjahre (vor 1961 nur 1951), kein Medianalter. 65+-Anteil müsste berechnet werden. |
| Eurostat `demo_find`, `demo_pjanind` (AT) | Beginnt 1960, nur ein Jahr Gewinn. Werte gerundet, Medianalter 1960–1962 identisch 35,5. |
| WKO/Landes-PDFs | Sekundärquellen, Original von Statistik Austria vorhanden. |

## Entscheidungen (2026-10-23)

- Wahlbeteiligung 2017, 2019 und 2024 wird aus den Absolutzahlen berechnet.
- Lebenserwartung wird getrennt nach Männern und Frauen geführt, 1951–2025.
- Wahlen 1919–1930 werden aufgenommen.
- Fertilität 1951–1960 (Human Fertility Database) ist zurückgestellt.
- Die BMI-Tabelle 1919–2008 wird als CSV in `data/manual/` geführt. Keine PDF-Abhängigkeit.
- Die AK-Reihe (Monatseinkommen 1953–2009) wird als eigener Indikator aufgenommen, Arbeiter und Angestellte getrennt, mit markiertem Bruch 1987.

## Offene Probleme und Fragen

1. **Großeltern-Spalte reicht weiter zurück als die Daten.** Bei Standardabstand 60 Jahre gilt für Geburtsjahre 1960–2005 bei den Großeltern das Stichjahr 1925–1970. Bei den Eltern ist es 1955–2000. Datenlage vor 1961:
   - Anteil 65+, Medianalter, Fertilität: **keine Jahreswerte vor 1961** bei Statistik Austria gefunden. Großeltern-Spalte bleibt bis Geburtsjahr ~1995 dort leer.
   - Lebenserwartung: ab 1951, aber nur nach Geschlecht.
   - VPI: ab 1946.
   - Wahlen: ab 1945. 1919–1930 ebenfalls in der Datei (siehe Punkt 4).
   - Die Annahme „Daten ab etwa 1950“ im Plan reicht also nicht für Geburtsjahre vor ~1985.
2. **Fertilität 1951–1960** (zurückgestellt): Kandidat ist die Human Fertility Database (humanfertility.org). Download nur nach kostenloser Registrierung, also manuell. Noch nicht geprüft.
3. **Methodenbrüche** müssen im Frontend erwähnt werden: gerundete Werte vor 2004, Erweiterung der Sterbe- und Geburtenzählung 2009/2015, Basiswechsel im VPI (verkettet, unkritisch). Wahlalter und Wahlpflicht: erledigt (2026-10-24), siehe Abschnitt BMI.
4. **Umrechnung Schilling in Euro:** erledigt. Kurs 13,7603, belegt durch die EZB (`ezb_euro_umrechnungskurse.html`, https://www.ecb.europa.eu/euro/intro/html/index.de.html, Abruf 2026-10-24). EUR-Lex (Verordnung 2866/98) liefert für automatisierte Abrufe keinen Inhalt (HTTP 202).
5. **AK-Reihe nach 2009:** Die AK hat das Heft auch für spätere Jahre herausgegeben. Ob es eine neuere Ausgabe mit derselben Tabelle gibt, ist nicht geprüft.

## Alltagspreise Wien 1966–2005 (Phase 5)

Bei Statistik Austria gibt es keine aktuelle Tabelle mit Durchschnittspreisen einzelner Produkte, nur Indizes. Verwendet wird die Tabelle „Durchschnittspreise ausgewählter Waren und Dienstleistungen“ aus dem Statistischen Jahrbuch der Stadt Wien. Laut Fußnote sind es „Angaben des Österreichischen Statistischen Zentralamtes aufgrund der Meldungen für die Preisstatistik (Wiener Preise)“. Jahrgang N enthält die Jahresdurchschnitte N−4 bis N, bis Jahrgang 2003 auch die Monatswerte von N.

| Quelle (sources.py) | Datei in data/raw/ (Wienbibliothek-ID) | Tabelle, Seiten | Jahre | Einheit |
|---|---|---|---|---|
| wien_preise_jb1970 | `wienbibliothek_2263179_jahrbuch_wien_1970_preise.pdf` | 18.02, S. 270–273 | 1966–1970 | ATS |
| wien_preise_jb1974 | `wienbibliothek_2263394_jahrbuch_wien_1974_preise.pdf` | 18.02, S. 298–301 | 1970–1974 | ATS |
| wien_preise_jb1979 | `wienbibliothek_2263699_jahrbuch_wien_1979_preise.pdf` | 18.07, S. 324–327 | 1975–1979 | ATS |
| wien_preise_jb1984 | `wienbibliothek_2266115_jahrbuch_wien_preise_1980_1984.pdf` | 19.02, S. 360–363 | 1980–1984 | ATS |
| wien_preise_jb1988 | `wienbibliothek_2276793_jahrbuch_wien_preise_1984_1988.pdf` | 19.05, S. 370–373 | 1984–1988 | ATS |
| wien_preise_jb1992 | `wienbibliothek_2277171_jahrbuch_wien_preise_1988_1992.pdf` | 18.03, S. 328–329 | 1988–1992 | ATS |
| wien_preise_jb1996 | `wienbibliothek_2283729_jahrbuch_wien_1996_preise.pdf` | 18.02, S. 292–293 | 1992–1996 | ATS |
| wien_preise_jb1999 | `wienbibliothek_2283911_jahrbuch_wien_1999_preise.pdf` | 18.02, S. 250–253 | 1995–1999 | ATS |
| wien_preise_jb2003 | `wienbibliothek_2284088_jahrbuch_wien_2003_preise.pdf` | 18.2, S. 210–215 | 1998–2002 | EUR |
| wien_preise_jb2006 | `wienbibliothek_2221944_jahrbuch_wien_2006_preise.pdf` (Gesamtausgabe, born-digital) | 17.3, S. 195–197 | 2001–2005 | EUR |

URL jeweils `https://www.digital.wienbibliothek.at/download/pdf/<ID>.pdf`. Abruf 2026-10-23 (1984, 1988, 1992) und 2026-10-24 (übrige).

- **Abschrift:** `data/manual/wien_durchschnittspreise.csv`, Spalten `quelle, seite, ware, jahr, monat, wert, einheit`. Die Scans 1970–2003 sind am Bild abgelesen, die Texterkennung diente nur als Hilfe. Jahrgang 2006 stammt aus der Textebene des born-digital-PDFs (keine Texterkennung).
- **Positionen:** Semmel (Stück), Vollmilch (1 l), Kinokarte (Stück), Benzin normal (1 l).
- **Regeln für die Reihe** (Entscheidung 2026-10-24):
  - Die Reihe läuft durchgehend in Euro.
  - Gibt es für ein Jahr einen Schillingwert, gilt Schilling ÷ 13,7603. Der Schillingwert steht zusätzlich in `series_ats` und erscheint im Frontend als Hinweis („damals 1,07 S“).
  - Ohne Schillingwert gilt der Euro-Wert der Quelle. Das betrifft 2000–2005. Für 2000 und 2001 liegen keine Schillingwerte vor, weil die Jahrgänge 2001/2002 nicht erfasst sind.
  - Bei mehreren Angaben in derselben Währung gilt der neueste Jahrgang.
- **Prüfung (Tests):**
  - Je Jahrgang gibt es fünf aufeinanderfolgende Jahre je Ware und eine einheitliche Währung.
  - Das Monatsmittel ergibt den Jahresdurchschnitt (±0,006), für 36 Fälle.
  - Die Überlappungsjahre stimmen zwischen den Jahrgängen überein.
  - Für 1998/1999 (in Schilling und in Euro gedruckt) gilt: Euro = Schilling ÷ 13,7603, innerhalb der Rundung.
- **Quellinkonsistenzen** (am Scan geprüft, in den Tests als bekannte Ausnahmen geführt):
  - **Vollmilch 1970:** Jahrgang 1970 nennt 4,60 S, die Jahrgänge 1971, 1973 und 1974 nennen 4,20 S. Verwendet wird der revidierte Wert 4,20 S. Die Abweichung steht im Quellen-Panel.
  - **Vollmilch 1974 (Jahrgang 1974):** Die Monatswerte (3 × 5,15, 8 × 5,99, 1 × 5,97) ergeben im Mittel 5,78. Gedruckt ist der Jahresdurchschnitt 5,76, verwendet wird er unverändert.
- **Methodenbrüche:**
  - **Vollmilch 1974:** Bis 1973 offene Milch. Laut Fußnote Jahrgang 1974 gilt ab 1974 der Durchschnittspreis für Milch in Flaschen und Verpackung. Jahrgang 1979 nennt dafür 1975. Markiert ist 1974.
  - **Benzin 1987:** bleifrei laut Fußnote, markiert.
  - **Ohne Markierung, nur als Hinweis:** Die Bezeichnung der Semmel wechselt zwischen den Jahrgängen 1974 und 1979 von „Stück“ zu „Stück, maschingeformt“. Für 1979 kommen laut Jahrgang 1979 neue Geschäftstypen (Diskontläden) dazu, Vergleiche mit den Vorjahren sind nur eingeschränkt möglich. Ab 1987 laut Quelle wegen geänderter Warenbeschreibungen ebenso.
- **Keine Wurstsemmel:** Die Quelle führt Semmel und Extrawurst nur einzeln. Zusammenrechnen wäre eine Konstruktion.
- **Euro-Kurs:** 13,7603 Schilling je Euro. Primärquelle: EZB, `ezb_euro_umrechnungskurse.html`. Bestätigt durch das AK-Heft, S. 2 („1 EURO = ÖS 13,7603“).
- **Kaufkraft:** Das Frontend rechnet in Preise von 2025 um (VPI), wie beim Einkommen.
- **Grenzen:** nur Wien. Ende 2005 (Feld `ended`, Hinweis „Tabelle erscheint nach 2005 nicht mehr“). Vor 1966 keine vergleichbare Reihe (siehe unten).

### Reichweite der Tabelle (Recherche 2026-10-23)

**Bestand der Wienbibliothek:**
- Digitalisierte Jahrgänge 1883–1914, 1929–1951 und 1970–2003 (ohne 2000), Sammlung `wbrobv`. Volltext-OCR je Jahrgang unter `/wbrobv/download/ftpack/plain/<id>`.
- Ab 2004 born-digital in der Sammlung `wbrup`, ohne Volltext.
- Für 1952–1969 gibt es kein Jahrbuch im Bestand.
- **Zugang:** Die Viewer-Seiten haben eine automatische Browserprüfung. Die PDF- und Volltext-Downloads sind direkt abrufbar.

**„Durchschnittspreise ausgewählter Waren und Dienstleistungen“ (ÖSTAT/ST.AT, Wiener Preise):**
- **Ab Jahrgang 1970:** Jahrgang N enthält die Jahresdurchschnitte N−4 bis N und die Monatswerte von N. Der früheste Wert stammt aus Jahrgang 1970 und ist 1966. Laut Volltext ist die Tabelle in jedem Jahrgang 1970–2003 enthalten.
- **Jahrgang 2003:** Tab. 18.2, Daten 1998–2002, alle Werte in Euro. Die Werte 1998–2001 hat die Quelle aus Schilling umgerechnet. Visuell geprüft.
- **Jahrgänge 2004–2006 (born-digital, Textsuche in den Content-Streams):**
  - 2004: Tab. 17.2, Werte bis 2003
  - 2005: Tab. 17.4, 2000–2004
  - 2006: Tab. 17.3, 2001–2005, letzter Wert Semmel 2005: 0,28 €
- **Jahrgänge 2007 und 2008:** Die Tabelle fehlt (Textsuche nach Durchschnittspreis, Semmel, Vollmilch: keine Treffer). Die Reihe endet also mit dem Datenjahr 2005.
- **Positionen und Definitionswechsel:**
  - Vollmilch heißt 1970 „1 l, offen“, später „1 l, abgepackt“.
  - Benzin heißt bis 1986 „normal, inländ.“, ab 1987 „bleifrei“.
  - Semmel heißt 1970 „Stück“, später „Stück, maschingeformt“.
- **Umgesetzt:** 1966–2005 lückenlos mit zehn Jahrgängen (siehe Tabelle oben). Statt 1978/1980 wurde Jahrgang 1979 verwendet, der 1975–1979 abdeckt.

**Vor 1966 (Jahrgänge 1929–1951):** Dort gibt es nur „Kleinhandelspreise und Kleinhandelsindex“. Das sind Preise je Mengeneinheit für den Index, zum Beispiel 1949–1951 Milch und „Brot, weiß (Kleingebäck), Stk.“. Kinokarte und Benzin fehlen. Es ist ein anderes Konzept und eine andere Warenbeschreibung. Dazu kommen Währungswechsel: Reichsmark 1938–1945, Schilling ab Ende 1945. Nicht mit der Reihe ab 1966 verbinden.

### Noch nicht verwendet

- https://www.digital.wienbibliothek.at/download/pdf/2283261.pdf: Jahrgang 1993, Tab. 18.03 mit Daten bis 1993. Würde ein Jahr ergänzen.
- **EU Weekly Oil Bulletin (Benzin österreichweit ab 2005):** https://energy.ec.europa.eu/document/download/906e60ca-8b6a-44e7-8589-652854d2fd3f_en?filename=Weekly_Oil_Bulletin_Prices_History_maticni_4web.xlsx. Nicht geprüft.

## Mieten (Phase 5)

### rent_share_income: Mietanteil am Haushaltseinkommen

- **Datei:** `eurostat_ilc_mded02_AT.json`, Antwort der Eurostat-API, unverändert gespeichert.
- **URL:** https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/ilc_mded02?geo=AT&hhcomp=TOTAL&rskpovth=TOTAL&format=JSON&lang=EN
- **Abruf:** 2026-10-24. Datenstand laut Antwort: 2026-10-20.
- **Inhalt:** „Share of rent related to occupied dwelling in disposable household income“, Österreich, alle Haushaltstypen und Einkommensgruppen.
- **Abdeckung:** 2003–2025, ohne Lücken. Flag `b` (Zeitreihenbruch) bei 2008, keine weiteren Flags. Der Build bricht bei unbekannten Flags ab.
- **Definition** (Eurostat, Statistics Explained, „EU-SILC methodology – economic strain linked to dwelling“, gelesen am 2026-10-24):
  - Gewichteter Mittelwert (Gewicht RB050a) von HH060 × 12 / HY020 × 100, also Monatsmiete mal 12 durch verfügbares Haushaltseinkommen.
  - Strom, Heizung, Instandhaltung und Dienstleistungen sind nicht enthalten.
  - Haushalte ohne Wert für HH060 sind ausgeschlossen.
- **Nicht geprüft:** ob HH060 vor oder nach Abzug der Wohnbeihilfe erfasst ist.

### rent_avg: Durchschnittsmiete je Hauptmietwohnung

- **Datei:** `statistik_austria_ergebnisse_im_ueberblick_wohnkosten_Mikrozensus.ods`
- **URL:** https://www.statistik.at/fileadmin/pages/351/ergebnisse_im_ueberblick_wohnkosten_Mikrozensus.ods
- **Abruf:** 2026-10-24. Quellvermerk: „Q: STATISTIK AUSTRIA, Mikrozensus Wohnen. – Erstellt am 08.09.2026.“
- **Verwendet:** Tabelle 2, Block „Durchschnittliche Miete inkl. Betriebskosten pro Wohnung in Euro“, Spalte Österreich.
- **Abdeckung:** 2005–2025, ohne Lücken.
- **Fußnoten:** 1) nur Hauptmietwohnungen mit Nettomiete > 0 Euro. 2) Zeitreihenbruch 2021 aufgrund der Erhebungsumstellung. Als Bruch 2021 markiert.
- **Abgleich:** Wert 2025 (674,57 €) = Tabelle 4, Zeile „Insgesamt“, derselben Datei. Wird getestet.
- **Kaufkraft:** Das Frontend rechnet zusätzlich in Preise von 2025 um.

### Geprüft, nicht verwendet

- `ilc_mded01`: Anteil aller Wohnkosten am Einkommen, über alle Haushalte einschließlich Eigentümer, 2004–2025. Für „Miete“ ist `ilc_mded02` passender.
- Statistik Austria, EU-SILC, `ergebnisse_im_ueberblick_wohnkosten_SILC.ods`: Median der Wohnkosten je Haushalt, 2008–2025. Kein Verhältnis zum Einkommen.
- **Eigener Quotient:** Mikrozensus-Miete geteilt durch den Lohnsteuer-Median ist verworfen. Die beiden Größen haben unterschiedliche Grundgesamtheiten und Begriffe.

### Offen

- Vor 2003 gibt es keine Werte. Ob ältere Mikrozensus-Erhebungen zum Wohnungsaufwand veröffentlicht sind, etwa im Statistischen Jahrbuch für Österreich, ist nicht recherchiert.

## Kaufkraft: Arbeitsminuten je Ware (Phase 5)

Arbeitsminuten = Preis / (Stundenlohn / 60). Das Frontend rechnet sie aus (`withWorkMinutes`), data.json enthält nur Preise und Löhne. Eine angenommene Wochenarbeitszeit ist ausgeschlossen, weil sie eine Schätzung wäre.

### wage_industry_vienna: Brutto-Stundenverdienst der Industriearbeiter in Wien, 1987–2005

- **Definition:** einschließlich Akkorde und Prämien. Erhebungsmonat jeweils September. Quelle laut Tabelle: Bundeskammer bzw. Wirtschaftskammer Österreich.
- **Abschrift:** `data/manual/wien_stundenverdienste_industriearbeiter.csv`. Die Spalte `methode` gibt an, wie jeder Wert erfasst ist:

| Jahrgang | Tabelle | Jahre | Methode |
|---|---|---|---|
| 1992 (`wien_preise_jb1992`) | 18.06b, S. 335 | 1987–1991 | am Scan abgelesen |
| 1996 (`wien_preise_jb1996`) | 18.05b | 1992–1996 | OCR-Volltext der Wienbibliothek (ftpack/plain 2082519) |
| 1999 (`wien_preise_jb1999`) | 18.07a | 1995–1999 | OCR-Volltext (ftpack/plain 2083794) |
| 2003 (`wien_preise_jb2003`) | 18.6.1, S. 220 | 1998–2002, Euro | am Scan abgelesen |
| 2006 (`wien_preise_jb2006`) | 17.5.2 | 2001–2005, Euro | Textebene des PDFs |

- **Prüfung (Tests):**
  - 1995/1996 sind in den Jahrgängen 1996 und 1999 identisch.
  - 2001/2002 sind in den Jahrgängen 2003 und 2006 identisch.
  - 1998/1999: Schilling (Jahrgang 1999) ÷ 13,7603 ergibt den Euro-Wert des Jahrgangs 2003 (9,49 bzw. 9,78).
  - Zusätzlich sind die Volltexte der Jahrgänge 1993, 1994, 1997 und 1998 konsistent, sie sind aber nicht als Datei abgelegt.
- **Reihe in Euro:** Schillingwerte bis 1999 umgerechnet, ab 2000 Euro laut Quelle. Wie bei den Preisen gibt es `series_ats` und die Kaufkraftumrechnung.
- **Bruch 2004:** laut Fußnote „Ohne Elektroindustrie“. Er ist im Diagramm markiert, nicht in jeder Tabellenzelle.
- **Grenzen** (stehen im Quellen-Panel):
  - Nur Industriearbeiter. Diese verdienen eher mehr als der Durchschnitt aller Beschäftigten, die Minuten fallen daher eher zu niedrig aus.
  - Brutto.
  - Lohn vom September, Preis im Jahresdurchschnitt.
  - Nur 1987–2005.
- **Rundung:** Für 2000 und 2001 sind die Preise in der Quelle auf Cent gerundet (Semmel 0,23 €). Bei billigen Waren macht das bis zu ±2 % der Minuten aus.

### Verworfen

- **AK Wien, Bruttowochenverdienst und Wochenarbeitszeit in Industrie- und Gewerbebetrieben** (Jahrbuch 1970–1981):
  - nur nach Geschlecht und Lohnart getrennt
  - teils weniger als 10 Fälle
  - Lücke 1980–1986
- **Statistik Austria, Verdienststrukturerhebung:** nur alle vier Jahre, erst ab 2002.
- **Vorhandene Einkommensreihen** (Lohnsteuer, AK-Monatseinkommen): keine Arbeitszeit.
