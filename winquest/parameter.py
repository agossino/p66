import configparser
import logging
import logging.config
import json
import pathlib
from typing import Dict, Any, Tuple, Callable

logName = "quest2pdf." + __name__
logger = logging.getLogger(logName)


class Parameter:
    def __init__(self, integers: Tuple[str] = (), booleans: Tuple[str] = ()):
        self._para = {}
        self._conf_ini = configparser.ConfigParser()
        self._get_data_type: Dict[Tuple[str], Callable] = {integers: self._conf_ini.getint,
                                                           booleans: self._conf_ini.getboolean}

    @property
    def dictionary(self) -> Dict[str, Any]:
        return self._para

    def load_from_ini(self, file_path: pathlib.Path):
        script_path = pathlib.Path(__file__).parent
        home_path = pathlib.Path.home()

        files = (
                str(file_path),
                str(script_path.joinpath(file_path.name)),
                str(home_path.joinpath(file_path.name)),
            )

        self._conf_ini.read(files)

        for section in self._conf_ini.sections():
            self._para.update({section: {}})
            for option in self._conf_ini[section]:
                logging.warning("key %s", option)
                self._para[section][option] = self._get_value(section, option)

    def load_from_json(self, file_path: pathlib.Path):
        with file_path.open() as file_handler:
            self._para = json.load(file_handler)

    def _get_value(self, section: str, option: str):
        for options in self._get_data_type:
            if option in options:
                return self._get_data_type[options](section, option)

        return self._conf_ini[section][option]
