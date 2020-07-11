import logging
from tkinter import Menu, Label, YES, BOTH
import _thread, queue
from pathlib import Path
from typing import Dict, Any

import exam2pdf

from parameter import Parameter
from utility import exception_printer
from guimixin import MainWindow
from _version import __version__

Parameters = Dict[str, Any]


def main():
    """Reads parameter and start loop.
    """
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
    def __init__(self, app_conf_file: Path = "conf.ini"):
        """Get application parameters and show the main window.
        """
        self.app_conf_file: Path = app_conf_file
        self.parameters: Parameters = load_parameters(app_conf_file)
        MainWindow.__init__(self, Path(__file__).stem)
        self.data_queue = queue.Queue()
        self.geometry("500x500")
        welcome = "Da tabella a PDF: genera un file di domande "
        welcome += "a scelta multipla in formato PDF, a partire "
        welcome += "da un file in formato Comma Separated Value."
        Label(self, text=welcome, wraplength=500).pack(expand=YES, fill=BOTH)

        menu = Menu(self)
        self.config(menu=menu)
        file = Menu(menu)

        file.add_command(label="Converti", command=self.read_input_file)
        file.add_command(label="Configura", command=self.reload_params)
        file.add_command(label="Termina", command=self.quit)
        menu.add_cascade(label="File", menu=file)

        info = Menu(menu)
        info.add_command(label="Guida", command=self.show_handbook)
        info.add_command(label="Versione", command=self.show_version)
        menu.add_cascade(label="Info", menu=info)

    def read_input_file(self):
        while True:
            input_file, output_folder = self.enter_openfile()
            if input_file and output_folder:
                _thread.start_new_thread(self.to_pdf, (input_file, output_folder))
                break
            # TODO in case of abort, exit from this dialog
            self.errorbox("Indicare sorgente e destinazione")

    def to_pdf(self, input_file: Path, output_folder: Path):
        exam = exam2pdf.Exam()

        if self.parameters["exam"].get("csv heading keys", None) is not None:
            exam.attribute_selector = self.parameters["exam"]["csv heading keys"].split(",")
        try:
            exam.from_csv(input_file, **self.parameters["DictReader"])
        except exam2pdf.Exam2pdfException as err:
            logging.critical("CSVReader failed: %s %s", err.__class__, err)
            self.errorbox(exception_printer(err))
            raise
        exam.add_path_parent(input_file)
        logging.info("Parameter: %s", self.parameters)

        exam.print(Path(self.parameters["exam"]["exam file name"]),
                   Path(self.parameters["exam"]["correction file name"]),
                   self.parameters["exam"]["answers shuffle"],
                   self.parameters["exam"]["questions shuffle"],
                   output_folder,
                   self.parameters["exam"]["n copies"],
                   self.parameters["exam"]["heading"],
                   self.parameters["exam"]["footer"])

        self.infobox("Avviso", "Conversione effettuata")

        self.data_queue.put("end")

    def reload_params(self) -> None:
        self.parameters = load_parameters(self.app_conf_file)
        self.infobox("Avviso", "Riletto file di configurazione")

    def show_version(self) -> None:
        """Show application version
        """
        self.infobox(
            "Versione",
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
            logging.critical("Handbook opening failed: %s %s", err.__class__, err)
            self.errorbox(exception_printer(err))
            raise


if __name__ == "__main__":
    main()
