import sys
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtCore import QObject


class Main(QObject):
    pass


def main():
    global app
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()
    engine.load("qml/main.qml")
    win = engine.rootObjects()[0]
    win.show()
    engine.quit.connect(app.quit)
    sys.exit(app.exec_())
