import sys
from PyQt5.QtWidgets import QApplication

from HanziMindMap.gui.main import MainWindow


def main():
    app = QApplication(sys.argv)

    w = MainWindow()
    w.showUI()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
