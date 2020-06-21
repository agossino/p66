import pathlib

from parameter import Parameter


def test_no_values():
    param = Parameter()

    values = param.dictionary

    assert values == {}


def test_load_from_ini_failed(setup_dirs):
    file_path = pathlib.Path("conf.ini")

    param = Parameter()

    param.load_from_ini(file_path)

    values = param.dictionary

    assert values == {}


def test_load_from_ini(conf_contents, setup_in_current):
    file_path = pathlib.Path("conf.ini")

    param = Parameter(integers=("integer",), booleans=("boolean",))

    param.load_from_ini(file_path)

    assert param.dictionary == conf_contents


def test_load_from_json(conf_contents, setup_in_current):
    file_path = pathlib.Path("conf.json")

    param = Parameter()

    param.load_from_json(file_path)

    assert param.dictionary == conf_contents

