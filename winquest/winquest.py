import logging
from tkinter import Menu, Label, YES, BOTH
import _thread, queue
from pathlib import Path
from datetime import datetime
from typing import Mapping, Dict, Any, List, Union

from parameter import param_parser
from utility import exception_printer
from guimixin import MainWindow
import quest2pdf

from version import __version__


LOGNAME = "winquest"
LOGGER = logging.getLogger(LOGNAME)


def main():
    """Reads parameter and start loop.
    """
    param: Dict[str, Any] = param_parser()
    LOGGER.debug(str(param))

    c = ContentMix(param)
    c.mainloop()


class ContentMix(MainWindow):
    def __init__(self, app_parameters: Mapping[str, Union[str, int, bool]]):
        """Get application parameters and show the main window.
        """
        self.parameters = app_parameters
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
        file.add_command(label="Configura", command=self.notdone)
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
        exam = quest2pdf.Exam()

        if self.parameters["csv_heading_keys"] is not None:
            exam.attribute_selector = self.parameters["csv_heading_keys"].split(",")
        try:
            exam.from_csv(input_file)
        except Exception as err:
            LOGGER.critical("CSVReader failed: %s %s", err.__class__, err)
            self.errorbox(exception_printer(err))
            raise
        exam.add_path_parent(input_file)
        logging.info("Parameter: %s", self.parameters)

        for number in range(self.parameters["number"]):
            if self.parameters["not_shuffle"] is False:
                exam.shuffle()

            output_file_name_exam = Path(f"{self.parameters['exam']}_{number}.pdf")
            output_file_name_correction = Path(
                f"{self.parameters['correction']}_{number}.pdf"
            )

            if isinstance(self.parameters["page_heading"], str):
                exam_heading = self.parameters["page_heading"]
            elif self.parameters["page_heading"]:
                exam_heading = output_file_name_exam
            else:
                exam_heading = ""

            if isinstance(self.parameters["page_footer"], str):
                exam_footer = self.parameters["page_footer"]
            elif self.parameters["page_footer"]:
                exam_footer = datetime.now().isoformat()
            else:
                exam_footer = ""

            exam.print(
                output_folder / output_file_name_exam,
                correction_file_name=output_folder / output_file_name_correction,
                heading=exam_heading,
                footer=exam_footer
            )

        self.infobox("Avviso", "Conversione effettuata")

        self.data_queue.put("end")

    def _get_rows(self, input_file: Path) -> List[Dict[str, str]]:
        try:
            file_content = CSVReader(
                str(input_file),
                self.parameters["encoding"],
                self.parameters["delimiter"],
            )

            rows = file_content.to_dictlist()
        except Exception as err:
            LOGGER.critical("CSVReader failed: %s %s", err.__class__, err)
            self.errorbox(exception_printer(err))
            raise

        return rows

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
            LOGGER.critical("Handbook opening failed: %s %s", err.__class__, err)
            self.errorbox(exception_printer(err))
            raise


if __name__ == "__main__":
    main()
