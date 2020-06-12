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
    def __init__(self, kwargs: Dict[str, Any] = None):
        if kwargs:
            self._para = kwargs
        else:
            self._para = {}
        self._conf_ini = configparser.ConfigParser()

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
            self._para.update({section: self._conf_ini[section]})

    def load_from_json(self, file_path: pathlib.Path):
        with file_path.open() as file_handler:
            self._para = json.load(file_handler)
