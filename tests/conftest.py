import pathlib
import configparser
import json

import pytest


@pytest.fixture
def conf_contents():
    return {"general": {"a text": "string", "b text": "999", "integer": 1, "boolean": False}}


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
