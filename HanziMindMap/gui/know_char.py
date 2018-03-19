from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QPushButton,
                             QVBoxLayout, QHBoxLayout)
from PyQt5.Qt import Qt
from random import choice

from HanziMindMap.gui import clickable
from HanziMindMap.util import speak


class MainWindow(QWidget):
    def __init__(self, db, dictionary):
        super().__init__()
        self.db = db
        self.dict = dictionary

        right = QVBoxLayout()
        right.addWidget(QLabel('Related characters:'))
        self.related_char = QLineEdit()
        right.addWidget(self.related_char)
        right.addWidget(QLabel('Related vocabs:'))
        self.related_vocab = QLineEdit()
        right.addWidget(self.related_vocab)
        self.related_sen = []
        for i in range(2):
            self.related_sen.append(QLabel())
            self.related_sen[i].setWordWrap(True)
            self.related_sen[i].setAlignment(Qt.AlignTop)
            self.related_sen[i].linkActivated.connect(speak)
        buttons = QHBoxLayout()
        right.addWidget(buttons)

        buttons.addStretch()
        self.submit = QPushButton('Submit')
        buttons.addWidget(self.submit)

        self.char = QLabel()
        self.set_random_char()
        self.char.setStyleSheet("font-size: 200px")
        clickable(self.char).connect(self.set_random_char)

        layout = QHBoxLayout()
        layout.addWidget(self.char)
        layout.addLayout(right)

        self.setLayout(layout)
        self.show()

    def set_random_char(self):
        for i in range(5):
            self.example[i].setText('')

        self.char.setText(choice([char for char in str(self.db) if u'\u4e00' <= char <= u'\u9fff']))
        related_vocab_text = []
        for entry in self.db:
            if self.char.text() in repr(entry):
                related_vocab_text.append(entry[1])
        self.related_vocab.setText('，'.join(related_vocab_text))


def load(db, dictionary):
    return MainWindow(db, dictionary)
