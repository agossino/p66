import pathlib
import pytest
import configparser

from parameter import Parameter


@pytest.fixture()
def conf_contents():
    return {"a": "string", "b": "999", "c": ""}


@pytest.fixture()
def setup_ini(monkeypatch, tmp_path, conf_contents):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(pathlib.Path, "parent", tmp_path)
    monkeypatch.setenv("HOME", str(tmp_path))

    conf_file_path = tmp_path / "conf.ini"
    config = configparser.ConfigParser()
    config["General"] = conf_contents
    with conf_file_path.open("w") as file_handle:
        config.write(file_handle)

    yield


def test_no_values():
    param = Parameter()

    values = param.dictionary

    assert values == {}


def test_set_values(conf_contents):
    param = Parameter(conf_contents)

    values = param.dictionary

    assert values == conf_contents


def test_load_from_init(conf_contents, setup_ini):
    file_path = pathlib.Path("conf.ini")

    param = Parameter()

    param.load_from_ini(file_path)

    values = param.dictionary

    assert dict(values) == conf_contents
