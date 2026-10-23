# Projektregeln mit25 (Generationen-Spiegel)

Statische Webseite: Geburtsjahr eingeben, sehen wie Österreich aussah, als man selbst, die Eltern und die Großeltern jeweils 25 Jahre alt waren. Vollständiger Plan: PLAN.md.

## Regeln

- Antworte auf Deutsch, sachlich und knapp.
- Niemals Datenwerte erfinden, schätzen oder interpolieren. Jede Zahl stammt aus einer Datei in data/raw/ oder data/manual/.
- Jede Quelle wird in data/SOURCES.md mit URL, Abrufdatum und Abdeckung dokumentiert.
- site/data.json wird nur von pipeline/build.py erzeugt, nie händisch bearbeitet.
- Neue Abhängigkeiten nur nach Rückfrage.
- Nach jeder Phase: Zusammenfassung, offene Punkte, dann auf Freigabe warten.
- Ein Git-Commit pro abgeschlossenem Arbeitsschritt, aussagekräftige Commit-Nachricht auf Deutsch.
- Keine Em-Dashes in Texten auf der Webseite.

## Aufbau Pipeline

- `pipeline/sources.py`: Register aller Rohdateien (URL, Abrufdatum). Muss zu data/SOURCES.md passen.
- `pipeline/readers.py`: ODS-, XLSX- und OGD-CSV-Leser, nur Standardbibliothek.
- `pipeline/indicators/<id>.py`: je Indikator `build()`. Registrierung in `indicators/__init__.py`.

## Aufbau Frontend

- `site/logic.js`: reine Logik ohne DOM (Stichjahre, Wertauswahl, Lücken, Format). Getestet.
- `site/app.js`: DOM-Aufbau; `site/style.css`: Farbtoken je Generation (`--grandparents`, `--parents`, `--you`), Hell/Dunkel.
- `site/chart.js`: SVG-Liniendiagramme ohne Bibliothek (Stichjahr-Markierungen, Tooltip, Tastatur, Wertetabelle); `site/chart-logic.js`: Achsen, Linienabschnitte, Leerbereiche. Getestet.
- Diagrammregeln: Linien enden an Lücken (nie verbinden), X-Achse reicht bis zu allen Stichjahren, Bereiche ohne Daten grau. Generationsfarben nur für Stichjahre, Datenlinien neutral.
- Farbänderungen an Generationstoken mit dem dataviz-Validator prüfen (hell gegen `#f4f6f7`, dunkel gegen `#141a21`).
- Wahl: nächste innerhalb ±3 Jahre, bei Gleichstand die frühere.
- Kaufkraft: Indikatoren mit `deflate: "cpi"` bekommen im Frontend (`withPriceAdjusted`) eine zweite Reihe in Preisen des letzten VPI-Jahres. data.json bleibt nominal.
- Methodenbruch: Feld `breaks: [{year, before}]` trennt die Linie im Diagramm und kennzeichnet Werte davor in der Tabelle. Feld `ended: true`: eingestellte Reihe, nach dem letzten Jahr Lücke statt "aktuellster Wert".
- Schilling-Reihen: Feld `eur_factor` (1/13,7603). Das Frontend zeigt Schilling und Euro in Preisen des letzten VPI-Jahres; das Diagramm nur die Euro-Reihe (`chart: false` an der Schilling-Reihe). `ended_note` ersetzt den Text "Reihe endet" (z. B. Pilot nur bis 1992 erfasst).
- Zahlenformat `de-DE` (Punkt als Tausendertrenner), weil `de-AT` in CLDR Leerzeichen nutzt.
- Zustände je Zelle: ok, future (noch nicht erreicht), pending (Jahr erreicht, Daten noch nicht veröffentlicht), missing.

## Befehle

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python pipeline/fetch.py     # lädt fehlende Rohdaten (--force: alle neu)
.venv/bin/python pipeline/build.py     # erzeugt site/data.json
.venv/bin/pytest                       # Tests Pipeline
node --test tests/*.test.mjs           # Tests Frontend-Logik (site/logic.js), nur Node eingebaut
python3 -m http.server -d site 8000    # Seite lokal ansehen
```
