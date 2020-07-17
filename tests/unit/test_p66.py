import pathlib

import pytest

from p66 import p66
from exam2pdf import Exam2pdfException


def test_contentmix_no_ini_file():
    """GIVEN ContentMix call without argument
    THEN no exception is raised
    """
    p66.ContentMix()
    assert True


def test_contentmix_parameter(conf_contents, setup_in_current):
    """GIVEN an ini file to ContentMix
    THEN parameter are set
    """
    file_path = pathlib.Path("conf.ini")

    cont = p66.ContentMix(file_path)

    assert cont.parameters == conf_contents


def test_contentmix_no_cvs_file(tmp_path, monkeypatch):
    """GIVEN a cvs file
    WHEN an image path is not found
    THEN Exam2pdf exception is raised
    """
    class MonkeyWin(p66.ContentMix):
        def errorbox(self, _):
            pass

    monkeypatch.setattr(p66, "ContentMix", MonkeyWin)

    cont = p66.ContentMix()
    with pytest.raises(Exam2pdfException):
        cont.to_pdf(tmp_path / "no_file", tmp_path)


def test_contentmix_cvs_image_not_found(
    tmp_path, setup_dirs, exam_with_wrong_picture, monkeypatch
):
    """GIVEN a cvs file
    WHEN an image path is not found
    THEN Exam2pdf exception is raised
    """
    class MonkeyWin(p66.ContentMix):
        def errorbox(self, _):
            pass

    monkeypatch.setattr(p66, "ContentMix", MonkeyWin)

    cont = p66.ContentMix()
    with pytest.raises(Exam2pdfException):
        cont.to_pdf(exam_with_wrong_picture, tmp_path)
