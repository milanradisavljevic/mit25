"""Registry der Indikatoren.

Jedes Indikator-Modul stellt eine Funktion build() bereit, die ein dict (oder eine
Liste von dicts) im Format aus PLAN.md Abschnitt 4 liefert. Neue Module hier in
INDICATORS eintragen.
"""

from . import cpi, fertility_rate, life_expectancy_birth, median_age, share_65plus, turnout_nrw

INDICATORS = [life_expectancy_birth, share_65plus, median_age, fertility_rate, turnout_nrw, cpi]
