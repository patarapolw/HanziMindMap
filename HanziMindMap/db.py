from time import time
from random import choice

from PyQt5.QtCore import QObject, pyqtSlot, pyqtProperty


class UserVocab(QObject):
    TABLE = 'user'

    def __init__(self, db):
        super().__init__()
        self.db = db
        self.db.execute('''CREATE TABLE IF NOT EXISTS {} (
                id          INT PRIMARY KEY NOT NULL,
                char_vocab          TEXT    NOT NULL,
                associated_sounds   TEXT,
                associated_meanings TEXT
            );'''.format(self.TABLE))
        self.db.commit()

        self._lookup = []

    def __iter__(self):
        return self.db.execute('SELECT * FROM {}'.format(self.TABLE))

    @pyqtSlot(str, str, str)
    def do_submit(self, char_vocab, ass_sound, ass_meaning):
        self.do_delete(char_vocab)
        self.db.execute('''INSERT INTO {} (id, char_vocab, associated_sounds, associated_meanings) 
                           VALUES (?, ?, ?, ?)'''.format(self.TABLE),
                        (int(time()*1000), char_vocab, ass_sound, ass_meaning))
        self.db.commit()

    @pyqtSlot(str)
    def do_lookup(self, char_vocab):
        cursor = self.db.execute('''SELECT associated_sounds, associated_meanings 
                                    FROM {} WHERE char_vocab=?;'''.format(self.TABLE), (char_vocab, ))
        self._lookup = cursor.fetchone()

    @pyqtProperty(list)
    def get_lookup(self):
        if self._lookup:
            return list(self._lookup)
        else:
            return []

    @pyqtSlot(str)
    def do_delete(self, char_vocab):
        cursor = self.db.execute('''SELECT id FROM {} WHERE char_vocab=?;'''.format(self.TABLE)
                                 , (char_vocab, ))
        id_tuple = cursor.fetchone()
        if id_tuple is not None:
            self.db.execute('''DELETE FROM {} WHERE id=?;'''.format(self.TABLE), id_tuple)
            self.db.commit()

    @pyqtProperty(list)
    def get_dump(self):
        return [list(item) for item in self]

    @pyqtProperty(str)
    def get_rand_char(self):
        chars = ''.join([''.join([str(data) for data in item]) for item in self])
        return choice([char for char in chars if u'\u4e00' <= char <= u'\u9fff'])


class UserHanzi(QObject):
    TABLE = 'user_hanzi'

    def __init__(self, db):
        super().__init__()
        self.db = db
        self.db.execute('''CREATE TABLE IF NOT EXISTS {} (
                id        INT PRIMARY KEY NOT NULL,
                char      TEXT NOT NULL,
                rel_char  TEXT,
                rel_vocab TEXT
            );'''.format(self.TABLE))
        self.db.commit()

        self._lookup = []

    def __iter__(self):
        return self.db.execute('SELECT * FROM {}'.format(self.TABLE))

    @pyqtSlot(str, str, str)
    def do_submit(self, char, rel_char, rel_vocab):
        self.do_delete(char)
        self.db.execute('''INSERT INTO {} (id, char, rel_char, rel_vocab) 
                               VALUES (?, ?, ?, ?)'''.format(self.TABLE),
                        (int(time() * 1000), char, rel_char, rel_vocab))
        self.db.commit()

    @pyqtSlot(str)
    def do_lookup(self, char):
        cursor = self.db.execute('''SELECT rel_char, rel_vocab FROM {} WHERE char=?;'''.format(self.TABLE)
                                 , (char,))
        self._lookup = cursor.fetchone()

    @pyqtProperty(list)
    def get_lookup(self):
        if self._lookup:
            return list(self._lookup)
        else:
            return []

    @pyqtSlot(str)
    def do_delete(self, char):
        cursor = self.db.execute('''SELECT id FROM {} WHERE char=?;'''.format(self.TABLE)
                                 , (char,))
        id_tuple = cursor.fetchone()
        if id_tuple is not None:
            self.db.execute('''DELETE FROM {} WHERE id=?;'''.format(self.TABLE)
                            , id_tuple)
            self.db.commit()

    @pyqtProperty(str)
    def get_dump(self):
        return [list(item) for item in self]
