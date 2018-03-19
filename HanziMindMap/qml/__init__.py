import sys
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtCore import QObject


class Main(QObject):
    pass


def main():
    sys.argv += ['--style', 'fusion']
    app = QGuiApplication(sys.argv)

    engine = QQmlApplicationEngine()
    engine.load("qml/main.qml")
    engine.quit.connect(app.quit)

    sys.exit(app.exec_())
