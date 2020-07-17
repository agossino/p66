import gettext
from pathlib import Path


def set_i18n():
    this_script_path = Path(__file__)
    locales = this_script_path.parent / "locales"
    trans = gettext.translation("exam2pdf", localedir=str(locales), fallback=True)
    return trans

