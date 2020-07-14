import pathlib

from p66 import parameter


def test_no_values():
    param = parameter.Parameter()

    values = param.dictionary

    assert values == {}


def test_load_from_ini_failed(setup_dirs):
    file_path = pathlib.Path("conf.ini")

    param = parameter.Parameter()

    param.load_from_ini(file_path)

    values = param.dictionary

    assert values == {}


def test_load_from_ini(conf_contents, setup_in_current):
    file_path = pathlib.Path("conf.ini")

    param = parameter.Parameter(integers=("n copies",), booleans=("questions shuffle",))

    param.load_from_ini(file_path)

    assert param.dictionary == conf_contents


def test_load_from_json(conf_contents, setup_in_current):
    file_path = pathlib.Path("conf.json")

    param = parameter.Parameter()

    param.load_from_json(file_path)

    assert param.dictionary == conf_contents
