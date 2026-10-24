# mit25

Wie sah Österreich aus, als du, deine Eltern und deine Großeltern 25 waren? Geburtsjahr eingeben, und die Seite zeigt amtliche Zahlen für die drei Stichjahre nebeneinander, dazu den Verlauf über die Jahrzehnte.

**Leitprinzip:** Jede angezeigte Zahl stammt aus einer abgelegten Quelldatei. Lücken bleiben sichtbar; nichts wird geschätzt oder interpoliert.

## Was die Seite zeigt

| Thema | Kennzahlen | Jahre |
|---|---|---|
| Leben und Bevölkerung | Lebenserwartung (Männer, Frauen), Anteil 65+, Medianalter, Kinder pro Frau | 1951 bzw. 1961 bis 2025 |
| Einkommen | Median-Bruttojahreseinkommen; Monatseinkommen Arbeiter und Angestellte; Stundenlohn Industriearbeiter Wien | 1997–2024; 1953–2009; 1987–2005 |
| Preise in Wien | Semmel, Vollmilch, Kinokarte, Benzin; jeweils auch in Arbeitsminuten | 1966–2005; Minuten 1987–2005 |
| Wohnen | Mietanteil am Haushaltseinkommen; Durchschnittsmiete | 2003–2025; 2005–2025 |
| Politik | Wahlbeteiligung Nationalratswahl | 1919–2024 |

Geldbeträge erscheinen nominal und in Preisen von 2025 (umgerechnet mit dem Verbraucherpreisindex). Quellen, Methodenbrüche und Einschränkungen stehen je Zeile unter „Quelle und Hinweise“ und ausführlich in [data/SOURCES.md](data/SOURCES.md).

## Starten

```bash
python3 -m http.server -d site 8765
```

Dann http://localhost:8765 öffnen. Die Seite ist statisch (HTML, CSS, JavaScript ohne Framework und ohne externe Abhängigkeiten) und lässt sich auf jedem statischen Hosting veröffentlichen, z. B. GitHub Pages mit dem Ordner `site/`.

## Daten neu erzeugen und testen

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python pipeline/fetch.py   # fehlende Rohdaten laden (--force: alle neu)
.venv/bin/python pipeline/build.py   # site/data.json erzeugen
.venv/bin/pytest                     # Tests der Datenpipeline
node --test tests/*.test.mjs         # Tests der Frontend-Logik
```

## Aufbau

```
data/raw/        Originaldateien, unverändert (ODS, XLSX, CSV, PDF, HTML)
data/manual/     Abschriften aus PDFs/Scans, durch Tests gegen die Quelle geprüft
data/SOURCES.md  Quelle, URL, Abrufdatum, Abdeckung und Grenzen je Kennzahl
pipeline/        sources.py (Register), readers.py, indicators/ (ein Modul je Kennzahl), build.py
site/            index.html, app.js, logic.js, chart.js, chart-logic.js, style.css, data.json (generiert)
tests/           pytest (Pipeline) und node:test (Frontend-Logik)
```

Projektregeln: [CLAUDE.md](CLAUDE.md). Ursprünglicher Plan und Datenformat: [PLAN.md](PLAN.md).
