"""This file starts Application."""
import sys

from PyQt5 import QtWidgets

from pymap.ui.welcome_page_logic import Window


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())
