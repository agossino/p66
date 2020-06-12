import pathlib
import pytest
import configparser
import json

from parameter import Parameter


@pytest.fixture
def conf_contents():
    return {"general": {"a": "string", "b": "999", "c": "_"}}


@pytest.fixture
def setup_dirs(monkeypatch, tmp_path):
    home_path = tmp_path / "home"
    home_path.mkdir()
    monkeypatch.setenv("HOME", str(home_path))
    current_path = tmp_path / "current"
    current_path.mkdir()
    monkeypatch.chdir(current_path)
    script_path = tmp_path / "script"
    script_path.mkdir()
    monkeypatch.setattr(pathlib.Path, "parent", script_path)

    yield


@pytest.fixture
def setup_in_current(tmp_path, conf_contents, setup_dirs):
    ini_file_path = tmp_path / "current/conf.ini"
    config = configparser.ConfigParser()
    for section in conf_contents.keys():
        config[section] = conf_contents[section]
    with ini_file_path.open("w") as file_handle:
        config.write(file_handle)

    json_file_path = tmp_path / "current/conf.json"
    with json_file_path.open("w") as file_handle:
        json.dump(conf_contents, file_handle)

    yield


def test_no_values():
    param = Parameter()

    values = param.dictionary

    assert values == {}


def test_set_values(conf_contents):
    param = Parameter(conf_contents)

    values = param.dictionary

    assert values == conf_contents


def test_load_from_ini_failed(setup_dirs):
    file_path = pathlib.Path("conf.ini")

    param = Parameter()

    param.load_from_ini(file_path)

    values = param.dictionary

    assert values == {}


def test_load_from_ini(conf_contents, setup_in_current):
    file_path = pathlib.Path("conf.ini")

    param = Parameter()

    param.load_from_ini(file_path)

    assert param.dictionary == conf_contents


def test_load_from_json(conf_contents, setup_in_current):
    file_path = pathlib.Path("conf.json")

    param = Parameter()

    param.load_from_json(file_path)

    assert param.dictionary == conf_contents

