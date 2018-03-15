from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget,
                             QLabel, QLineEdit, QPushButton,
                             QHBoxLayout, QVBoxLayout, QGridLayout)
from PyQt5.Qt import Qt
from PyQt5.QtCore import QObject, pyqtSignal, QEvent
import subprocess

from HanziMindMap.db import Database
from HanziMindMap.dict import Cedict, SpoonFed


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(300, 300, 600, 200)
        self.setWindowTitle('Hanzi Mind Map')
        self.db = Database()
        self.dict = Cedict()
        self.sentence = SpoonFed()
        self.meaning_id = 0
        self.dict_entry = []

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
        clickable(self.pinyin).connect(self.speak)
        self.meanings = QLabel()
        self.meanings.setWordWrap(True)
        self.meanings.setAlignment(Qt.AlignTop)
        self.meanings.setFixedHeight(50)
        clickable(self.meanings).connect(self.next_meaning)
        self.sen1 = QLabel()
        self.sen1.setWordWrap(True)
        self.sen1.setAlignment(Qt.AlignTop)
        clickable(self.sen1).connect(self.speak_sen1)
        self.sen2 = QLabel()
        self.sen2.setWordWrap(True)
        self.sen2.setAlignment(Qt.AlignTop)
        clickable(self.sen2).connect(self.speak_sen2)

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
        top.addWidget(self.sen1, 5, 1)
        top.addWidget(self.sen2, 6, 1)

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

        self.dict_entry = self.dict.dictionary.setdefault(text)
        sentence_iter = self.sentence.search(text)
        if self.dict_entry is not None:
            self.meaning_id = 0
            self.pinyin.setText(self.dict_entry[self.meaning_id]['reading'])
            self.meanings.setText(self.dict_entry[self.meaning_id]['english'])
            try:
                s1 = next(sentence_iter)
                self.sen1.setText(s1['sentence'])
                self.sen1.setToolTip(s1['english'])

                s2 = next(sentence_iter)
                self.sen2.setText(s2['sentence'])
                self.sen2.setToolTip(s2['english'])
            except StopIteration:
                pass
        else:
            self.pinyin.setText('')
            self.meanings.setText('')

            self.sen1.setText('')
            self.sen1.setToolTip('')
            self.sen2.setText('')
            self.sen2.setToolTip('')

    def next_meaning(self):
        self.meaning_id = (self.meaning_id + 1) % len(self.dict_entry)
        self.pinyin.setText(self.dict_entry[self.meaning_id]['reading'])
        self.meanings.setText(self.dict_entry[self.meaning_id]['english'])

    def speak(self):
        subprocess.call(['say', '-v', 'ting-ting', self.char_vocab.text()])

    def speak_sen1(self):
        subprocess.call(['say', '-v', 'ting-ting', self.sen1.text()])

    def speak_sen2(self):
        subprocess.call(['say', '-v', 'ting-ting', self.sen2.text()])

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
        self.sen1.setText('')
        self.sen2.setText('')
        self.char_vocab.setFocus()


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
