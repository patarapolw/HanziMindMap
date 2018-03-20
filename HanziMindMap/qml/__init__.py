import sys
import json
from random import choice

from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtCore import QObject, pyqtSlot, pyqtProperty

from HanziMindMap.db import Database
from HanziMindMap.dict import Cedict, SpoonFed
from HanziMindMap.util import speak


class SearchOnType(QObject):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.dict = {
            'dict': Cedict(),
            'sentence': SpoonFed(),
        }
        self.dict_entry = []

        self._lookup = dict()
        self._lookup_found = False

    @pyqtProperty(str)
    def lookup(self):
        return json.dumps(self._lookup)

    @pyqtProperty(bool)
    def found(self):
        return self._lookup_found

    @pyqtProperty(list)
    def dump_database(self):
        return [list(item) for item in self.db]

    @pyqtProperty(str)
    def rand_char(self):
        chars = ''.join([''.join([str(data) for data in item]) for item in self.db])
        return choice([char for char in chars if u'\u4e00' <= char <= u'\u9fff'])

    @pyqtSlot(str)
    def text_changed(self, text):
        self._lookup = {
            'user': self.db.lookup(text),
            'dictionary': self.dict['dict'].dictionary.setdefault(text),
            'sentence': list(self.dict['sentence'].search(text))
        }

        self._lookup_found = bool(self._lookup['user'])

    @pyqtSlot()
    def do_submit(self):
        self.do_delete()
        self.db.submit(self.char_vocab.text(),
                       self.associated_sounds.text(),
                       self.associated_meanings.text())

    @pyqtSlot()
    def do_delete(self):
        self.db.delete(self.char_vocab.text())

    @pyqtSlot(str)
    def speak(self, word):
        speak(word)


def main():
    sys.argv += ['--style', 'fusion']
    app = QGuiApplication(sys.argv)

    engine = QQmlApplicationEngine()
    engine.load("qml/main.qml")
    engine.quit.connect(app.quit)

    context = engine.rootContext()
    search = SearchOnType()
    context.setContextProperty('py', search)

    sys.exit(app.exec_())
