import pytest
from pygit2.repository import Repository

from pyvc.cli import main, validate_args


class MockCommit:
    def __init__(self, message):
        self.message = message


def test_main_invalid_path():
    with pytest.raises(Exception):
        main("/(7", "1.0.0")


def test_main_invalid_semver():
    with pytest.raises(Exception):
        main(".", "1.0.0.2")


def test_validate_version():
    assert validate_args(".", "1.0.a") is False


def test_validate_path():
    assert validate_args("/(??", "1.1.1") is False


def test_validate_true():
    assert validate_args(".", "1.2.3") is True


def test_single_commit(monkeypatch):
    def mock_walk(*args, **kwargs):  # noqa
        return [MockCommit("feat: x")]

    monkeypatch.setattr(Repository, "walk", mock_walk)

    assert main(".", "1.0.0") == "1.1.0"
