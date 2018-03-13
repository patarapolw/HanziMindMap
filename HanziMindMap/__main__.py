import sys
from PyQt5.QtWidgets import QApplication

from HanziMindMap.gui import MainWindow


def main():
    app = QApplication(sys.argv)

    w = MainWindow()
    w.showUI()

    sys.exit(app.exec_())
