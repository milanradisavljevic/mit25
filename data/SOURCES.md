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
3. **Methodenbrüche** müssen im Frontend erwähnt werden: gerundete Werte vor 2004, Erweiterung der Sterbe- und Geburtenzählung 2009/2015, Basiswechsel im VPI (verkettet, unkritisch). Bei der Wahlbeteiligung sind Änderungen von Wahlalter und Wahlpflicht in einzelnen Ländern **zu prüfen**, nicht aus dem Gedächtnis eintragen.
4. **VPI-Umrechnung in Euro** (Phase 5): Für Schilling-Preise ist zusätzlich der fixe Umrechnungskurs ATS/EUR nötig. Dafür braucht es eine Quelle in SOURCES.md.
5. **AK-Reihe nach 2009:** Die AK hat das Heft auch für spätere Jahre herausgegeben. Ob es eine neuere Ausgabe mit derselben Tabelle gibt, ist nicht geprüft.

## Alltagspreise (Phase 5, Recherche 2026-10-23, noch keine Daten übernommen)

Bei Statistik Austria gibt es keine aktuelle Tabelle mit Durchschnittspreisen einzelner Produkte, nur Indizes.

**Kandidat 1: Statistisches Jahrbuch der Stadt Wien, Kapitel „Preise, Lebenshaltung und Löhne“**
- **Tabelle:** „Durchschnittspreise ausgewählter Waren und Dienstleistungen“, Jahresdurchschnitte in Schilling. Laut Fußnote „Angaben des Österreichischen Statistischen Zentralamtes aufgrund der Meldungen für die Preisstatistik (Wiener Preise)“.
- **Digitalisate (Wienbibliothek, Scans mit OCR):**
  - https://www.digital.wienbibliothek.at/download/pdf/2277171.pdf: Jahrbuch-Auszug, Tab. 18.03, Jahresdurchschnitte 1988–1991 und Monatswerte 1992, gedruckte Seiten 328–329. Visuell geprüft.
  - https://www.digital.wienbibliothek.at/download/pdf/2266115.pdf: laut Websuche Tab. 19.02, etwa 1980–1983. Nicht geprüft.
  - https://www.digital.wienbibliothek.at/download/pdf/2276793.pdf: laut Websuche Tab. 19.05, etwa 1984–1987. Nicht geprüft.
  - https://www.digital.wienbibliothek.at/download/pdf/2283261.pdf: laut Websuche Tab. 18.03, etwa 1989–1992. Nicht geprüft.
- **Enthaltene Positionen:** Semmel (Stück, maschingeformt), Vollmilch (1 l, abgepackt), Kinokarte (Stück), Benzin (normal, bleifrei, Liter), Extrawurst (fein, 100 g) und weitere.
- **Keine Wurstsemmel.** Eine Wurstsemmel aus Semmel und Extrawurst zusammenzurechnen wäre eine Konstruktion, also nicht zulässig.
- **Einschränkungen:**
  - Es sind nur Wiener Preise.
  - Jede Ausgabe deckt nur wenige Jahre ab, also braucht es viele Ausgaben.
  - Die Texterkennung der Scans ist fehlerhaft. Jede Zahl muss am Bild geprüft werden.
  - Die Produktdefinitionen ändern sich über die Zeit, etwa Benzin verbleit gegenüber bleifrei.
- **Offen:** Wie weit die Reihe zurückreicht und ob es sie nach den 1990ern noch gibt.

**Kandidat 2: Benzin österreichweit, EU Weekly Oil Bulletin (Europäische Kommission)**
- **Datei:** historische Datei `Weekly_Oil_Bulletin_Prices_History_maticni_4web.xlsx`, laut Newsletter ab 2005.
- **Link:** https://energy.ec.europa.eu/document/download/906e60ca-8b6a-44e7-8589-652854d2fd3f_en?filename=Weekly_Oil_Bulletin_Prices_History_maticni_4web.xlsx
- **Nicht geprüft:** Inhalt und ob es eine Spalte für Österreich mit Euro-Super 95 gibt.
