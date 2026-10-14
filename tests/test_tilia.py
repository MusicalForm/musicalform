import json

import pytest

from musicalform.tilia import iter_timeline_components


@pytest.mark.parametrize("kind", ["HIERARCHY_TIMELINE", "Hierarchy"])
def test_kind_filter_matches_both_spellings(kind, tmp_path):
    path = tmp_path / "piece.json"
    data = {
        "timelines": [
            {"kind": kind, "name": "Form", "components": [{"label": "bi", "start": 0.0, "end": 1.0}]},
            {"kind": "Beat", "name": "Measures", "components": [{"time": 0.0}]},
        ]
    }
    path.write_text(json.dumps(data), encoding="utf-8")
    result = list(iter_timeline_components(path, kinds=["HIERARCHY_TIMELINE"]))
    assert [tl_props["name"] for tl_props, _, _ in result] == ["Form"]
