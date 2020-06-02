#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import logging
import csv
from typing import List, Dict, Optional


LOGNAME = "quest2pdf"
LOGGER = logging.getLogger(LOGNAME)


class CSVReader:
    """Convert from a Comma Separated Value file to different
    formats.
    """

    def __init__(self, file_name: str, encoding: str = "utf-8", delimiter: str = ","):
        self.file_name: str = file_name
        encoding: str = encoding
        self.delimiter: str = delimiter

        try:
            self._read(encoding)
        except UnicodeError as err:
            msg: str = "Error in reading %s encoding %s: %s"
            LOGGER.error(msg, self.file_name, encoding, err)
            raise

    def to_dictlist(self) -> List[Dict[str, str]]:
        """Return a list of dictionaries with the file contents.
        """
        return self.rows

    def _read(self, encoding: str, err: Optional[str] = None) -> None:
        """Read the file and fill self.rows.
        """
        try:
            with open(self.file_name, "r", encoding=encoding, errors=err) as csvfile:
                cvs_reader = csv.DictReader(csvfile, delimiter=self.delimiter)
                self.rows: List[Dict[str, str]]
                self.rows = [row for row in cvs_reader]
        except FileNotFoundError:
            LOGGER.critical("Input file %s not found.", self.file_name)
            raise


def exception_printer(exception_instance: Exception) -> str:
    """Format an exception class and instance in string
    """
    pattern: str = "\W+"
    exc_list: List[str] = re.split(pattern, str(exception_instance.__class__))
    try:
        return exc_list[2] + ": " + str(exception_instance)
    except IndexError:
        return str(exception_instance)


def safe_int(text: str) -> int:
    try:
        return int(text)
    except ValueError:
        return 0
