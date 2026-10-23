"""Erzeugt site/data.json aus den Indikator-Modulen."""

import json
from datetime import date
from pathlib import Path

from indicators import INDICATORS

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "site" / "data.json"


def build_data():
    return {
        "generated_at": date.today().isoformat(),
        "indicators": [module.build() for module in INDICATORS],
    }


def main(output=OUTPUT):
    data = build_data()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{output.relative_to(ROOT)}: {len(data['indicators'])} Indikatoren")


if __name__ == "__main__":
    main()
