from pathlib import Path

import pytest

from musicalform.cli.main import build_parser, run


@pytest.mark.parametrize(
    "argv, expected",
    [
        ([], "usage: musicalform [-h]"),
        (["validate"], "usage: musicalform validate"),
        (["validate", "-v"], "usage: musicalform validate"),
        (["convert"], "usage: musicalform convert"),
        (["convert", "-a"], "usage: musicalform convert"),
    ],
)
def test_help_shown_without_input(argv, expected, capsys):
    run(argv)
    captured = capsys.readouterr()
    assert captured.out.startswith(expected)
    assert captured.err == ""


def test_tilde_expanded_in_path_options(monkeypatch, tmp_path):
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.setenv("USERPROFILE", str(tmp_path))
    args = build_parser().parse_args(["validate", "-d", "~/annotations", "-o", "~/reports"])
    assert Path(args.directory) == tmp_path / "annotations"
    assert Path(args.output) == tmp_path / "reports"
