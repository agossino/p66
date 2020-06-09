#!/usr/bin/env python
import configparser
import logging
import logging.config
import json
import pathlib
from typing import Dict, Any, List, Optional

logName = "quest2pdf." + __name__
logger = logging.getLogger(logName)


class Parameter:
    def __init__(self, kwargs: Dict[str, Any] = {}):
        self._para = kwargs
        self._conf_ini = configparser.ConfigParser()

    @property
    def dictionary(self) -> Dict[str, Any]:
        return self._para

    def load_from_ini(self, file_path: pathlib.Path):
        self._conf_ini.read(file_path.name)
        self._para = self._conf_ini["General"]


def param_parser(args: Optional[List[str]] = []) -> Dict[str, Any]:
    """Arguments from command line have precedence over the ones
    coming from configuration file.
    """
    default_values = get_default()

    log_conf_file = pathlib.Path(default_values["log_configuration_file"])

    start_logger(log_conf_file)
    app_config_file = pathlib.Path(default_values["app_configuration_file"])

    app_configuration_param = conf_file_parser(pathlib.Path(app_config_file))
    default_values.update(app_configuration_param)

    chosen_args = {}
    for index in range(0, len(args), 2):
        try:
            chosen_args[args[index]] = args[index + 1]
        except IndexError:
            pass

    default_values.update(chosen_args)

    return default_values


def get_default() -> Dict[str, Any]:
    default_args = {
        "input": "questions.csv",
        "number": 1,
        "exam": "Exam",
        "correction": "Correction",
        "app_configuration_file": "conf.ini",
        "log_configuration_file": "loggingConf.json",
        "not_shuffle": False,
        "page_heading": "",
        "page_footer": "",
        "delimiter": "comma",
        "encoding": "utf-8",
        # "version": __version__,
    }

    return default_args


def start_logger(file_name: pathlib.Path) -> None:
    script_path: pathlib.Path = pathlib.Path(__file__).parent
    home_path: pathlib.Path = pathlib.Path.home()

    for file in (
        file_name,
        script_path.joinpath(file_name),
        home_path.joinpath(file_name),
    ):
        result = try_log_conf_file(file)
        if result is True:
            return

    logger.warning(
        "logging configuration file not found in %s, %s and %s: default configuration will be used.",
        str(pathlib.Path.cwd()),
        str(script_path),
        str(home_path),
    )


def try_log_conf_file(file_path: pathlib.Path) -> bool:
    """It tries to open a log configuration file.
    filePath: filePath
    return: boolean (True is succeed, False otherwise)
    """
    global logger

    try:
        with file_path.open() as f:
            logger_conf = json.load(f)
            logging.config.dictConfig(logger_conf)
            logger = logging.getLogger(__name__)
            logger.debug("logger started from %s", str(pathlib.Path.cwd()))
            logger.info("%s found", str(file_path))
            return True
    except FileNotFoundError as e:
        logger.info("%s not found: %s", str(file_path), str(e))
        return False


def conf_file_parser(file_name: pathlib.Path) -> Dict[str, Any]:
    script_path = pathlib.Path(__file__).parent
    home_path = pathlib.Path.home()

    for file in (
        file_name,
        script_path.joinpath(file_name),
        home_path.joinpath(file_name),
    ):
        output = try_conf_file(file)
        if output is not None:
            return output

    logger.warning(
        "app configuration file not found in %s, %s and %s: default configuration will be used.",
        str(pathlib.Path.cwd()),
        str(script_path),
        str(home_path),
    )
    return dict()
    # raise FileNotFoundError


def try_conf_file(file_path: pathlib.Path) -> Optional[Dict[str, Any]]:
    output: Dict[str, Any] = {}
    config = configparser.ConfigParser()

    try:
        with file_path.open() as fh:
            config.read_file(fh)
            logger.info("%s found", file_path)
            for key, value in config["Default"].items():
                output[key] = value
    except FileNotFoundError as e:
        logger.info("%s not found: %s", file_path, str(e))
        return None

    return output