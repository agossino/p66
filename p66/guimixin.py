"""
###############################################################################
a "mixin" class for other frames: common methods for canned dialogs,
spawning programs, simple text viewers, etc; this class must be mixed
with a Frame (or a subclass derived from Frame) for its quit method
###############################################################################
"""

import glob
from pathlib import Path
from typing import Tuple

import tkinter.scrolledtext as tk_st
from tkinter.messagebox import *
from tkinter.filedialog import *

from p66.utility import set_i18n

_ = set_i18n().gettext


class GuiMixin:
    def infobox(self, title, text, *args):
        return showinfo(title, text)

    def errorbox(self, text):
        showerror(_("Error!"), text)

    def question(self, title, text, *args):
        return askyesno(title, text)  # return True or False

    def notdone(self):
        showerror(_("Not implemented"), _("Option not avilable"))

    def quit(self):
        ans = self.question(_("Verify quit"), _("Are you sure you want to quit?"))
        if ans:
            Frame.quit(self)  # quit not recursive!

    def help(self):
        self.infobox(_("RTFM"), _("See figure 1..."))

    def handbook(self, file_name: str) -> None:
        title: str = _("Handbook")
        self.browser(file_name, title)

    def select_openfile(self, file="", dir=".") -> str:
        return askopenfilename(initialdir=dir, initialfile=file)

    def select_savefile(self, file="", dir="."):
        return asksaveasfilename(initialfile=file, initialdir=dir)

    def select_folder(self, title=_("Select a folder"), initialdir=os.getcwd()):
        return askdirectory(title=title, initialdir=initialdir)

    def clone(self, args=()):  # optional constructor args
        new = Toplevel()  # make new in-process version of me
        myclass = self.__class__  # instance's (lowest) class object
        myclass(new, *args)  # attach/run instance to new window

    def browser(self, filename: str, title: str) -> None:
        new = Toplevel()
        new.title(title)
        text = tk_st.ScrolledText(new, wrap=WORD, height=30, width=85)
        # text.config(font=14)
        text.pack(expand=YES, fill=BOTH)
        new.iconname(_("browser"))
        text.insert("0.0", open(filename, "r", encoding="utf-8").read())
        text.config(state=DISABLED)

    def enter_openfile(self) -> Tuple[Path, Path]:
        win = Toplevel()
        win.title(_("Select source file and destination folder"))
        file_label = _("text file in CVS format")
        folder_label = _("destination folder")
        label_width = max(len(file_label), len(folder_label))
        file_selection = self._form_row(
            win, label=file_label, open_function=self.select_openfile, width=label_width
        )
        folder_selection = self._form_row(
            win, label=folder_label, open_function=self.select_folder, width=label_width
        )
        Button(win, text="OK", command=win.destroy).pack()
        # TODO addo Abort button
        win.grab_set()
        win.focus_set()  # go modal: mouse grab, keyboard focus, wait
        win.wait_window()  # wait till destroy; else returns now
        return Path(file_selection.get()), Path(folder_selection.get())

    def _form_row(
        self, parent, label, open_function, width=15, browse=True, extend=False
    ):
        var = StringVar()
        row = Frame(parent)
        lab = Label(row, text=label, relief=RIDGE, width=width)
        ent = Entry(row, relief=SUNKEN, textvariable=var)
        row.pack(fill=X)  # uses packed row frames
        lab.pack(side=LEFT)  # and fixed-width labels
        ent.pack(side=LEFT, expand=YES, fill=X)  # or use grid(row, col)
        if browse:
            btn = Button(row, text=_("browse ..."))
            btn.pack(side=RIGHT)
            if not extend:
                btn.config(command=lambda: var.set(open_function() or var.get()))
            else:
                btn.config(command=lambda: var.set(var.get() + " " + open_function()))
        return var


"""
###############################################################################
Classes that encapsulate top-level interfaces.
Allows same GUI to be main, pop-up, or attached; content classes may inherit
from these directly, or be mixed together with them per usage mode; may also
be called directly without a subclass; designed to be mixed in after (further
to the right than) app-specific classes: else, subclass gets methods here
(destroy, okayToQuit), instead of from app-specific classes--can't redefine.
###############################################################################
"""


class _window:
    """
    mixin shared by main and pop-up windows
    """

    foundicon = None
    iconpatt = "*.ico"
    iconmine = "py.ico"

    def configBorders(self, app, kind, iconfile):
        if not iconfile:  # no icon passed?
            iconfile = self.findIcon()  # try curr,tool dirs
        title = app
        if kind:
            title += " - " + kind
        self.title(title)  # on window border
        self.iconname(app)  # when minimized
        if iconfile:
            try:
                self.iconbitmap(iconfile)  # window icon image
            except:  # bad py or platform
                pass
        self.protocol("WM_DELETE_WINDOW", self.quit)  # don't close silent

    def findIcon(self):
        if _window.foundicon:  # already found one?
            return _window.foundicon
        iconfile = None  # try curr dir first
        iconshere = glob.glob(self.iconpatt)  # assume just one
        if iconshere:  # del icon for red Tk
            iconfile = iconshere[0]
        else:  # try tools dir icon
            mymod = __import__(__name__)  # import self for dir
            path = __name__.split(".")  # poss a package path
            for mod in path[1:]:  # follow path to end
                mymod = getattr(mymod, mod)  # only have leftmost
            mydir = os.path.dirname(mymod.__file__)
            myicon = os.path.join(mydir, self.iconmine)  # use myicon, not tk
            if os.path.exists(myicon):
                iconfile = myicon
        _window.foundicon = iconfile  # don't search again
        return iconfile


class MainWindow(Tk, _window, GuiMixin):
    """
    when run in main top-level window
    """

    def __init__(self, app, kind="", iconfile=None):
        self.findIcon()
        Tk.__init__(self)
        self.__app = app
        self.configBorders(app, kind, iconfile)

    def quit(self):
        if self.okayToQuit():  # threads running?
            ans = self.question(_("Exit"), _("Are you sure you want to leave?"))
            if ans:
                self.destroy()  # quit whole app
        else:
            self.showinfo(self.__app, _("Exit not possible"))

    def destroy(self):
        Tk.quit(self)  # redef if exit ops

    def okayToQuit(self):  # redef me if used
        return True  # e.g., thread busy
