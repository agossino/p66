import re
import logging
from typing import List


LOGNAME = "p66"
LOGGER = logging.getLogger(LOGNAME)


def exception_printer(exception_instance: Exception) -> str:
    """Format an exception class and instance in string
    """
    pattern: str = "\W+"
    exc_list: List[str] = re.split(pattern, str(exception_instance.__class__))
    try:
        return exc_list[2] + ": " + str(exception_instance)
    except IndexError:
        return str(exception_instance)
