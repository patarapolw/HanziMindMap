from PyQt5.QtCore import QObject, pyqtSignal, QEvent
from PyQt5.QtWidgets import QApplication
import sys

from HanziMindMap.qt.main import MainWindow


def clickable(widget):
    class Filter(QObject):
        clicked = pyqtSignal()

        def eventFilter(self, obj, event):
            if obj == widget:
                if event.type() == QEvent.MouseButtonRelease:
                    if obj.rect().contains(event.pos()):
                        self.clicked.emit()
                        return True
            return False

    filter = Filter(widget)
    widget.installEventFilter(filter)
    return filter.clicked


def main():
    app = QApplication(sys.argv)

    w = MainWindow()
    w.showUI()

    sys.exit(app.exec_())
