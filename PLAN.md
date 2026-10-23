# mit25: Umsetzungsplan

Arbeitstitel: Generationen-Spiegel. Projektname: **mit25**.

## 1. Ziel

Eine statische Webseite: Nutzer gibt sein Geburtsjahr ein und sieht, wie Österreich aussah, als er selbst, seine Eltern und seine Großeltern jeweils 25 Jahre alt waren. Drei Spalten nebeneinander, darunter Zeitreihen-Diagramme mit markierten Jahren.

Leitprinzip: Jede angezeigte Zahl ist belegt. Lieber eine sichtbare Lücke als eine erfundene oder interpolierte Zahl.

### Nicht-Ziele (vorerst)

- Kein Server, keine Datenbank, keine Nutzerkonten
- Keine Länder außer Österreich
- Keine politischen Bewertungen in den Texten, nur Daten und neutrale Beschreibung

## 2. Technischer Rahmen

| Bereich | Entscheidung |
|---|---|
| Datenaufbereitung | Python 3 (Skripte, reproduzierbar, lokal auf Fedora) |
| Frontend | Eine statische Seite: HTML, CSS, Vanilla JavaScript (ohne Framework) |
| Diagramme | Eigenes SVG ohne Bibliothek (Entscheidung Phase 4, statt Observable Plot oder Chart.js): keine Abhängigkeit, Lücken exakt darstellbar |
| Datenformat | Eine generierte Datei site/data.json |
| Tests | pytest für die Datenpipeline |
| Hosting | Beliebig statisch (z. B. GitHub Pages), später |

Neue Abhängigkeiten nur nach Rückfrage.

## 3. Ordnerstruktur

```
mit25/
├── CLAUDE.md
├── PLAN.md
├── data/
│   ├── raw/            # Originaldownloads, unverändert
│   ├── manual/         # händisch gepflegte CSV-Dateien (z. B. Alltagspreise)
│   └── SOURCES.md      # Quelle, URL, Abrufdatum, Abdeckung je Indikator
├── pipeline/
│   ├── fetch.py        # lädt Rohdaten
│   ├── build.py        # erzeugt site/data.json
│   └── indicators/     # ein Modul pro Indikator
├── tests/
└── site/
    ├── index.html
    ├── app.js
    ├── style.css
    └── data.json       # generiert, nicht händisch bearbeiten
```

## 4. Datenmodell (site/data.json)

```json
{
  "generated_at": "2026-10-23",
  "indicators": [
    {
      "id": "life_expectancy_birth",
      "label": "Lebenserwartung bei Geburt",
      "unit": "Jahre",
      "description": "Durchschnittliche Lebenserwartung eines Neugeborenen im jeweiligen Jahr",
      "source": "Statistik Austria, ...",
      "source_url": "...",
      "retrieved": "2026-10-23",
      "series": { "1950": 65.7, "1951": null }
    }
  ]
}
```

Regeln:

- Fehlende Jahre als `null`, nicht weglassen und nicht interpolieren.
- Werte mit Nachkommastellen wie in der Quelle, Rundung erst im Frontend.
- Indikatoren mit Ereignischarakter (Wahlen) bekommen `"type": "event"` und nur die Jahre mit Ereignis.

Zusätzliche Felder (seit Phase 2):

- `notes`: Liste methodischer Hinweise (Rundung, Methodenbrüche, Quellfehler), im Frontend anzeigen.
- `sources`: Liste `{label, url}` je Quelldatei (`source` und `source_url` fassen sie zusammen bzw. nennen die erste).
- `group`: verbindet zusammengehörige Reihen (`life_expectancy_birth` für Männer und Frauen).
- `display: false`: Hilfsreihe, nicht direkt anzeigen (VPI).
- `deflate: "cpi"`: Frontend ergänzt eine Reihe in Preisen des letzten VPI-Jahres (Phase 5).
- `breaks: [{year, before}]`: Methodenbruch; Linie wird getrennt, Werte davor gekennzeichnet (Phase 5).
- `ended: true`: Reihe eingestellt; nach dem letzten Jahr keine Fortschreibung (Phase 5).

## 5. Indikatoren

### MVP

| ID | Indikator | Erwartete Quelle (zu prüfen) |
|---|---|---|
| life_expectancy_birth | Lebenserwartung bei Geburt | Statistik Austria |
| share_65plus | Anteil der Bevölkerung 65+ | Statistik Austria |
| median_age | Medianalter der Bevölkerung | Statistik Austria |
| fertility_rate | Gesamtfertilitätsrate (Kinder pro Frau) | Statistik Austria |
| turnout_nrw | Wahlbeteiligung Nationalratswahl | Bundesministerium für Inneres |
| cpi | Verbraucherpreisindex (VPI) | Statistik Austria |

Der VPI wird nicht direkt angezeigt, sondern dient zur Umrechnung historischer Preise in heutige Euro.

### Erweiterung (nach MVP)

- Einkommen (Median der Bruttojahreseinkommen, Methodikwechsel dokumentieren)
- Mieten im Verhältnis zum Einkommen (vermutlich erst ab den 2000ern lückenlos)
- Alltagspreise als händisch gepflegte CSV: Wurstsemmel, Liter Milch, Kinokarte, Liter Benzin, jeweils mit Einzelquelle
- Kaufkraft-Darstellung: „So viele Arbeitsminuten kostete eine Wurstsemmel“

## 6. Logik der Generationen

- Eingabe: eigenes Geburtsjahr (Pflicht), Geburtsjahr Mutter oder Vater und Großeltern (optional).
- Standard ohne Angabe: Eltern = Geburtsjahr minus 30, Großeltern = Geburtsjahr minus 60. Annahme sichtbar anzeigen und änderbar machen.
- Stichjahr je Person: Geburtsjahr plus 25.
- Liegt das Stichjahr in der Zukunft: Hinweis „noch nicht erreicht“, stattdessen aktuellster Wert mit Jahresangabe.
- Wahlen: die Nationalratswahl, die dem Stichjahr am nächsten liegt (maximal plus/minus 3 Jahre), mit Angabe des tatsächlichen Wahljahres.
- Fehlt ein Wert: „keine Daten für [Jahr]“ anzeigen.

## 7. Phasen mit Abnahmekriterien

### Phase 0: Setup
Repository, Ordnerstruktur, CLAUDE.md, Python-Umgebung (venv), requirements.txt.
**Fertig, wenn:** `python pipeline/build.py` läuft und eine leere, gültige data.json erzeugt.

### Phase 1: Datenrecherche
Für jeden MVP-Indikator die tatsächliche Quelle finden, Abdeckung prüfen (frühestes und letztes Jahr, Lücken). Ergebnis in data/SOURCES.md dokumentieren. Keine Daten aus dem Gedächtnis eintragen, nur aus heruntergeladenen Dateien.
**Fertig, wenn:** für jeden Indikator Quelle, URL, Abrufdatum und Abdeckung dokumentiert sind und offene Probleme benannt sind. Danach Stopp und Rückmeldung.

### Phase 2: Pipeline
fetch.py lädt Rohdaten nach data/raw/ (oder dokumentiert manuellen Download, falls kein direkter Download möglich). Je Indikator ein Modul, das Rohdaten in das Format aus Abschnitt 4 umwandelt. Tests: Plausibilitätsgrenzen (z. B. Lebenserwartung zwischen 40 und 95), keine doppelten Jahre, Stichproben gegen Quellwerte.
**Fertig, wenn:** pytest grün ist und data.json alle MVP-Indikatoren enthält.

### Phase 3: Frontend MVP
Eingabefeld Geburtsjahr, optionale Felder für Eltern und Großeltern. Drei Spalten (Großeltern, Eltern, Du) mit den Werten zum jeweiligen Stichjahr. Quellenangabe pro Indikator aufklappbar.
**Fertig, wenn:** die Seite lokal mit `python -m http.server` funktioniert, für Geburtsjahre 1960 bis 2005 sinnvolle Ergebnisse liefert und Lücken korrekt anzeigt.

### Phase 4: Visualisierung
Pro Indikator ein Liniendiagramm über die gesamte Zeitreihe, Stichjahre der drei Generationen markiert. Responsiv für Smartphone, Hell- und Dunkelmodus.
**Fertig, wenn:** Diagramme auf Desktop und Smartphone lesbar sind.

### Phase 5: Erweiterungen
Einkommen, Mieten, Alltagspreise wie in Abschnitt 5. Jede Erweiterung einzeln, mit eigenem Eintrag in SOURCES.md.

## 8. Arbeitsregeln

Siehe CLAUDE.md.

## 9. Offene Annahmen

- Fokus nur auf Österreich.
- Stichalter 25 Jahre, Generationenabstand 30 Jahre als Standard.
- Daten ab etwa 1950 werden für die Großeltern-Spalte benötigt; reicht eine Quelle nicht so weit zurück, wird das offen angezeigt.
- Diagrammbibliothek: entschieden in Phase 4, eigenes SVG (siehe Abschnitt 2).
