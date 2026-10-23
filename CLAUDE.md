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

## Befehle

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python pipeline/build.py     # erzeugt site/data.json
.venv/bin/pytest                       # Tests
python3 -m http.server -d site 8000    # Seite lokal ansehen
```
