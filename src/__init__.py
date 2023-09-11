import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "vendor"))

from aqt import gui_hooks, mw
from aqt.qt import *

from .gui.dialog import Dialog


def show_startup_message() -> None:
    dialog = Dialog(mw)
    dialog.show()


gui_hooks.main_window_did_init.append(show_startup_message)
