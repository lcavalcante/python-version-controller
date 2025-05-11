import pytest
from pyvc.cli import main


def test_main_invalid_path():
    with pytest.raises(Exception) as excinfo:
        main("/(7", "1.0.0")
    assert "invalid path" in str(excinfo).lower()


def test_main_invalid_semver():
    with pytest.raises(Exception):
        main(".", "1.0.0.2")
