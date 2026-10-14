import pytest

from musicalform.cli.main import run


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
