import logging
import gettext
from tkinter import Menu, Label, YES, BOTH
import _thread, queue
from pathlib import Path
from typing import Dict, Any

import exam2pdf

from p66.parameter import Parameter
from p66.utility import set_i18n
from p66.guimixin import MainWindow
from p66 import __version__

Parameters = Dict[str, Any]

_ = set_i18n().gettext


def main():
    """Reads parameter and start loop.
    """
    this_script_path = Path(__file__)
    locale = this_script_path.parent / "locale"
    gettext.bindtextdomain("exam2pdf", localedir=locale)

    app_conf_file = Path("conf.ini")

    c = ContentMix(app_conf_file)
    c.mainloop()


def load_parameters(app_conf_file: Path) -> Parameters:
    integer_options = ("n copies",)
    boolean_options = ("questions shuffle", "answers shuffle")

    param: Parameter = Parameter(integers=integer_options, booleans=boolean_options)
    param.load_from_ini(app_conf_file)

    return param.dictionary


class ContentMix(MainWindow):
    def __init__(self, app_conf_file: Path = Path("conf.ini")):
        """Get application parameters and show the main window.
        """
        self.app_conf_file: Path = app_conf_file
        self._exam_default_param: Parameters = {
            "csv heading keys": None,
            "exam file name": "Exam.pdf",
            "correction file name": "Checker.pdf",
            "answers shuffle": True,
            "questions shuffle": False,
            "n copies": 1,
            "heading": "",
            "footer": "",
        }
        self._DictReader_default_param: Parameters = {}
        self.parameters: Parameters = load_parameters(app_conf_file)
        MainWindow.__init__(self, Path(__file__).stem)
        self.data_queue = queue.Queue()
        self.geometry("500x500")
        welcome = _(
            """From table to PDF: print into a PDF file, a set of
multi choice questions, from a Comma Separated Value file."""
        )
        Label(self, text=welcome, wraplength=500).pack(expand=YES, fill=BOTH)

        menu = Menu(self)
        self.config(menu=menu)
        file = Menu(menu)

        convert_label = _("Convert")
        configure_lable = _("Configure")
        exit_label = _("Exit")
        file_label = _("File")
        file.add_command(label=convert_label, command=self.read_input_file)
        file.add_command(label=configure_lable, command=self.reload_params)
        file.add_command(label=exit_label, command=self.quit)
        menu.add_cascade(label=file_label, menu=file)

        info = Menu(menu)
        help_label = _("Help")
        handbook_label = _("Handbook")
        version_label = _("Version")
        info.add_command(label=handbook_label, command=self.show_handbook)
        info.add_command(label=version_label, command=self.show_version)
        menu.add_cascade(label=help_label, menu=info)

        self._info_label = _("Info")

    def read_input_file(self):
        while True:
            input_file, output_folder = self.enter_openfile()
            if input_file and output_folder:
                _thread.start_new_thread(self.to_pdf, (input_file, output_folder))
                break
            source_dest_label = _("Select source file and destination folder")
            self.errorbox(source_dest_label)

    def to_pdf(self, input_file: Path, output_folder: Path):
        exam = exam2pdf.Exam()

        self._exam_default_param.update(self.parameters.get("exam", {}))
        self._DictReader_default_param.update(self.parameters.get("DictReader", {}))

        if self._exam_default_param.get("csv heading keys", None) is not None:
            exam.attribute_selector = self._exam_default_param[
                "csv heading keys"
            ].split(",")
        try:
            exam.from_csv(input_file, **self._DictReader_default_param)
        except exam2pdf.Exam2pdfException as err:
            logging.critical("Exam reading from csv failed: %s", err)
            self.errorbox(err)
            raise
        exam.add_path_parent(input_file)

        try:
            exam.print(
                Path(self._exam_default_param["exam file name"]),
                Path(self._exam_default_param["correction file name"]),
                self._exam_default_param["answers shuffle"],
                self._exam_default_param["questions shuffle"],
                output_folder,
                self._exam_default_param["n copies"],
                self._exam_default_param["heading"],
                self._exam_default_param["footer"],
            )
        except exam2pdf.Exam2pdfException as err:
            logging.critical("Exam printing failed: %s", err)
            self.errorbox(err)
            raise

        conv_done_label = _("Conversion done")
        self.infobox(self._info_label, conv_done_label)

        self.data_queue.put("end")

    def reload_params(self) -> None:
        self.parameters = load_parameters(self.app_conf_file)
        read_label = _("Configuration file read")
        self.infobox(self._info_label, read_label)

    def show_version(self) -> None:
        """Show application version
        """
        version_label = _("Version")
        self.infobox(
            version_label,
            "{app_name}: {version}".format(
                app_name=Path(__file__).stem, version=__version__
            ),
        )

    def show_handbook(self) -> None:
        """Show handbook/how-to (long text).
        """
        help_file_name: str = "help.txt"
        script_path: Path = Path(__file__).resolve().parent
        try:
            self.handbook(str(script_path.joinpath(help_file_name)))
        except Exception as err:
            logging.critical("Handbook opening failed: %s", err)
            self.errorbox(err)
            raise


if __name__ == "__main__":
    main()
