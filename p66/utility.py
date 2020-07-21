import gettext
from pathlib import Path


def set_i18n():
    this_script_path = Path(__file__)
    locale = this_script_path.parent / "locale"

    trans = gettext.translation("p66", localedir=locale)
    return trans
