import json
from datetime import date

import build


def test_build_writes_valid_json(tmp_path, monkeypatch):
    output = tmp_path / "data.json"
    monkeypatch.setattr(build, "ROOT", tmp_path)
    build.main(output)

    data = json.loads(output.read_text(encoding="utf-8"))
    assert date.fromisoformat(data["generated_at"])
    assert isinstance(data["indicators"], list)


def test_indicator_ids_unique():
    ids = [ind["id"] for ind in build.build_data()["indicators"]]
    assert len(ids) == len(set(ids))
