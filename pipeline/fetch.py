"""Lädt Rohdaten nach data/raw/.

Wird in Phase 2 umgesetzt, sobald die Quellen in data/SOURCES.md feststehen.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"


def main():
    print("Noch keine Quellen definiert, siehe data/SOURCES.md.")


if __name__ == "__main__":
    main()
