from collections.abc import Callable

from aqt import *

class ConfigWindow(QMainWindow):
    def __init__(self, mw: aqt.AnkiQt) -> None:
        super().__init__(None, Qt.WindowType.Window)