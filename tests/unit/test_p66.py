import pathlib

import pytest

from p66.p66 import ContentMix
import p66.guimixin
from exam2pdf import Exam2pdfException


def test_contentmix_no_ini_file():
    """GIVEN ContentMix call without argument
    THEN no exception is raised
    """
    ContentMix()
    assert True


def test_contentmix_parameter(conf_contents, setup_in_current):
    """GIVEN an ini file to ContentMix
    THEN parameter are set
    """
    file_path = pathlib.Path("conf.ini")

    cont = ContentMix(file_path)

    assert cont.parameters == conf_contents


def test_contentmix_cvs_file_reading(tmp_path, setup_dirs, exam_with_wrong_picture, monkeypatch):
    """GIVEN a cvs file
    WHEN an image path is not found
    THEN Exam2pdf exception is raised
    """
    cont = ContentMix()
    with pytest.raises(Exam2pdfException):
        cont.to_pdf(exam_with_wrong_picture, tmp_path)
