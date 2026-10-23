"""Lädt Rohdaten nach data/raw/.

Vorhandene Dateien werden nicht überschrieben, außer mit --force. Nach einem
Neuladen das Abrufdatum in pipeline/sources.py und data/SOURCES.md anpassen.

Manuell gepflegt (kein Download): data/manual/bmi_wahlbeteiligung_1919_2008.csv,
abgetippt aus data/raw/bmi_nrw_08_wbseit1919.pdf (siehe data/SOURCES.md).
"""

import sys
import urllib.request

from sources import RAW, SOURCES

USER_AGENT = "Mozilla/5.0 (mit25 Datenpipeline)"


def download(source):
    request = urllib.request.Request(source.url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=60) as response:
        source.path.write_bytes(response.read())


def main(force=False):
    RAW.mkdir(parents=True, exist_ok=True)
    for key, source in SOURCES.items():
        if source.path.exists() and not force:
            print(f"vorhanden  {source.file}")
            continue
        download(source)
        print(f"geladen    {source.file}")
    if force:
        print("Hinweis: Abrufdatum in pipeline/sources.py und data/SOURCES.md aktualisieren.")


if __name__ == "__main__":
    main(force="--force" in sys.argv)
