from PyQt5.QtWidgets import (QApplication, QWidget,
                             QLabel, QLineEdit, QPushButton,
                             QHBoxLayout, QVBoxLayout, QGridLayout)

from HanziMindMap.db import Database
from HanziMindMap.dict import Cedict


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(300, 300, 600, 200)
        self.setWindowTitle('Hanzi Mind Map')
        self.db = Database()
        self.dict = Cedict()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db.db.close()

    def showUI(self):
        self.char_vocab = QLineEdit()
        self.char_vocab.textChanged.connect(self.text_changed)
        self.associated_sounds = QLineEdit()
        self.associated_meanings = QLineEdit()
        self.pinyin = QLabel()
        self.meanings = QLabel()

        submit = QPushButton("Submit")
        submit.clicked.connect(self.do_submit)
        delete = QPushButton("Delete")
        delete.clicked.connect(self.do_delete)

        top = QGridLayout()
        top.setColumnStretch(1, 4)

        top.addWidget(QLabel("Char/Vocab"), 0, 0)
        top.addWidget(self.char_vocab, 0, 1)
        top.addWidget(QLabel("Associated sounds"), 1, 0)
        top.addWidget(self.associated_sounds, 1, 1)
        top.addWidget(QLabel("Associated meaning"), 2, 0)
        top.addWidget(self.associated_meanings, 2, 1)
        top.addWidget(QLabel('Pinyin'), 3, 0)
        top.addWidget(self.pinyin, 3, 1)
        top.addWidget(QLabel("Meanings"), 4, 0)
        top.addWidget(self.meanings, 4, 1)

        bottom = QHBoxLayout()
        bottom.addStretch()
        bottom.addWidget(submit)
        bottom.addWidget(delete)

        layout = QVBoxLayout()
        layout.addLayout(top)
        layout.addLayout(bottom)

        self.setLayout(layout)
        self.show()

        self.move(QApplication.desktop().screen().rect().center() - self.rect().center())

    def text_changed(self, text):
        lookup = self.db.lookup(text)
        if lookup is not None:
            ass_sound, ass_meaning = lookup
            self.associated_sound.setText(ass_sound)
            self.associated_meaning.setText(ass_meaning)

        cedict_entry = self.dict.cedict.setdefault(text)
        if cedict_entry is not None:
            self.pinyin.setText(cedict_entry['pinyin'])
            self.meanings.setText(cedict_entry['english'])
        else:
            self.pinyin.setText('')
            self.meanings.setText('')

    def do_submit(self):
        self.do_delete()
        self.db.submit(self.char_vocab.text(),
                       self.associated_sounds.text(),
                       self.associated_meanings.text())

    def do_delete(self):
        self.db.delete(self.char_vocab.text())
