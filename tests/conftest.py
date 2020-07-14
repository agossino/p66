import pathlib
import configparser
import json
from itertools import chain
import csv

import pytest

import exam2pdf


@pytest.fixture
def conf_contents():
    return {"general": {"a text": "string", "b text": "999", "n copies": 1, "questions shuffle": False}}


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


@pytest.fixture
def save_pictures(tmp_path):
    image_folder = pathlib.Path("tests/unit/resources")
    image_tmp_folder = tmp_path / image_folder.name
    image_tmp_folder.mkdir()

    for file in chain(image_folder.glob("*.png"), image_folder.glob("*.jpg")):
        data = file.read_bytes()
        copied_file = tmp_path / image_folder.name / file.name
        copied_file.write_bytes(data)

    yield


@pytest.fixture
def exam_with_wrong_picture(tmp_path, save_pictures):
    csv_file = tmp_path / "exam.csv"
    with csv_file.open("w") as fh:
        fieldnames = ("question", "subject", "image", "level", "answer 1", "image 1", "answer 2", "image 2")
        writer = csv.DictWriter(fh, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerow({"question": "text",
                         "subject": "math",
                         "image": "resources/a.png",
                         "level": "2",
                         "answer 1": "text",
                         "image 1": "resources/not_existing.png",
                         "answer 2": "text",
                         "image 2": "resources/b.png"})

    return csv_file
