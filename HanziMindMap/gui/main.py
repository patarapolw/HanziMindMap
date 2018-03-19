from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QAction,
                             QLabel, QLineEdit, QPushButton,
                             QHBoxLayout, QVBoxLayout, QGridLayout)
from PyQt5.Qt import Qt

from HanziMindMap.db import Database
from HanziMindMap.dict import Cedict, SpoonFed
from HanziMindMap.gui import clickable, know_char, dump
from HanziMindMap.util import speak


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.dict = {
            'dict': Cedict(),
            'sentence': SpoonFed(),
        }
        self.meaning_id = 0
        self.dict_entry = []
        self.menubar_action = {
            'dump': QAction('Dump database', self),
            'know_char': QAction('Do you know this character?', self)
        }
        self.subwindow = None

        self.setGeometry(300, 300, 600, 200)
        self.setWindowTitle('Hanzi Mind Map')
        self.create_menubar()

    def create_menubar(self):
        bar = self.menuBar()
        file = bar.addMenu("&File")
        file.addAction(self.menubar_action['dump'])
        file.addAction(self.menubar_action['know_char'])
        file.triggered[QAction].connect(self.do_menubar)

    def do_menubar(self, action):
        if action is self.menubar_action['dump']:
            self.subwindow = dump.load(self.db)
        elif action is self.menubar_action['know_char']:
            self.subwindow = know_char.load(self.db, self.dict)

    def closeEvent(self, QCloseEvent):
        self.db.db.commit()
        self.db.db.close()
        super().closeEvent(QCloseEvent)

    def showUI(self):
        self.char_vocab = QLineEdit()
        self.char_vocab.textChanged.connect(self.text_changed)
        self.associated_sounds = QLineEdit()
        self.associated_meanings = QLineEdit()
        self.pinyin = QLabel()
        self.pinyin.linkActivated.connect(speak)
        self.meanings = QLabel()
        self.meanings.setWordWrap(True)
        self.meanings.setAlignment(Qt.AlignTop)
        self.meanings.setFixedHeight(50)
        clickable(self.meanings).connect(self.next_meaning)

        self.sen = []
        for i in range(2):
            self.sen.append(QLabel())
            self.sen[i].setWordWrap(True)
            self.sen[i].setAlignment(Qt.AlignTop)
            self.sen[i].linkActivated.connect(speak)

        submit = QPushButton("Submit")
        submit.clicked.connect(self.do_submit)
        delete = QPushButton("Delete")
        delete.clicked.connect(self.do_delete)
        clear = QPushButton("Clear")
        clear.clicked.connect(self.do_clear)

        self.char_vocab.returnPressed.connect(self.associated_sounds.setFocus)
        self.associated_sounds.returnPressed.connect(self.associated_meanings.setFocus)
        self.associated_meanings.returnPressed.connect(submit.click)

        top = QGridLayout()
        top.setColumnStretch(1, 4)

        top.addWidget(QLabel("Char/Vocab："), 0, 0)
        top.addWidget(self.char_vocab, 0, 1)
        top.addWidget(QLabel("Associated sounds："), 1, 0)
        top.addWidget(self.associated_sounds, 1, 1)
        top.addWidget(QLabel("Associated meaning："), 2, 0)
        top.addWidget(self.associated_meanings, 2, 1)
        top.addWidget(QLabel('Reading：'), 3, 0)
        top.addWidget(self.pinyin, 3, 1)
        label_meanings = QLabel("Meanings：")
        label_meanings.setAlignment(Qt.AlignTop)
        top.addWidget(label_meanings, 4, 0)
        top.addWidget(self.meanings, 4, 1)
        top.addWidget(QLabel('Sentences :'), 5, 0)
        top.addWidget(self.sen[0], 5, 1)
        top.addWidget(self.sen[1], 6, 1)

        bottom = QHBoxLayout()
        bottom.addStretch()
        bottom.addWidget(submit)
        bottom.addWidget(delete)
        bottom.addWidget(clear)

        layout = QVBoxLayout()
        layout.addLayout(top)
        layout.addLayout(bottom)

        central = QWidget()
        central.setLayout(layout)
        self.setCentralWidget(central)
        self.show()

        self.move(QApplication.desktop().screen().rect().center() - self.rect().center())

    def text_changed(self, text):
        lookup = self.db.lookup(text)
        if lookup is not None:
            ass_sound, ass_meaning = lookup
            self.associated_sounds.setText(ass_sound)
            self.associated_meanings.setText(ass_meaning)

            color = '#badc58'
            self.char_vocab.setStyleSheet("background-color: {}".format(color))
            self.associated_sounds.setStyleSheet("background-color: {}".format(color))
            self.associated_meanings.setStyleSheet("background-color: {}".format(color))
        else:
            self.associated_sounds.setText('')
            self.associated_meanings.setText('')

            color = '#ffffff'
            self.char_vocab.setStyleSheet("background-color: {}".format(color))
            self.associated_sounds.setStyleSheet("background-color: {}".format(color))
            self.associated_meanings.setStyleSheet("background-color: {}".format(color))

        self.dict_entry = self.dict['dict'].dictionary.setdefault(text)
        if self.dict_entry is not None:
            self.meaning_id = 0
            self.pinyin.setText(
                '<a href="{}">{}</a>'
                    .format(self.dict_entry[self.meaning_id]['simplified'],
                            self.dict_entry[self.meaning_id]['reading'])
            )
            self.meanings.setText(self.dict_entry[self.meaning_id]['english'])
            try:
                for i, s in enumerate(self.dict['sentence'].search(text)):
                    if i >=2:
                        break
                    self.sen[i].setText('<a href="{0}">{0}</a>'.format(s['sentence']))
                    self.sen[i].setToolTip(s['english'])
            except StopIteration:
                pass
        else:
            self.pinyin.setText('')
            self.meanings.setText('')

            for i in range(2):
                self.sen[i].setText('')
                self.sen[i].setToolTip('')

    def next_meaning(self):
        self.meaning_id = (self.meaning_id + 1) % len(self.dict_entry)
        self.pinyin.setText(
            '<a href="{}">{}</a>'
                .format(self.dict_entry[self.meaning_id]['simplified'],
                        self.dict_entry[self.meaning_id]['reading'])
        )
        self.meanings.setText(self.dict_entry[self.meaning_id]['english'])

    def do_submit(self):
        self.do_delete()
        self.db.submit(self.char_vocab.text(),
                       self.associated_sounds.text(),
                       self.associated_meanings.text())
        self.text_changed(self.char_vocab.text())

    def do_delete(self):
        self.db.delete(self.char_vocab.text())

    def do_clear(self):
        self.char_vocab.setText('')
        self.associated_sounds.setText('')
        self.associated_meanings.setText('')
        self.pinyin.setText('')
        self.meanings.setText('')
        for i in range(2):
            self.sen[i].setText('')
        self.char_vocab.setFocus()
