import sqlite3
from time import time

from HanziMindMap.dir import database_path


class Database:
    def __init__(self):
        self.db = sqlite3.connect(database_path("user.db"))
        self.db.execute('''CREATE TABLE IF NOT EXISTS user (
                id          INT PRIMARY KEY NOT NULL,
                char_vocab          TEXT    NOT NULL,
                associated_sounds   TEXT,
                associated_meanings TEXT
            );''')

    def submit(self, char_vocab, ass_sound, ass_meaning):
        self.db.execute('''INSERT INTO user (id, char_vocab, associated_sounds, associated_meanings) 
                           VALUES (?, ?, ?, ?)''',
                        (int(time()*1000), char_vocab, ass_sound, ass_meaning))
        self.db.commit()

    def lookup(self, char_vocab):
        cursor = self.db.execute('''SELECT associated_sounds, associated_meanings 
                                    FROM user WHERE char_vocab=?;''', (char_vocab, ))
        return cursor.fetchone()

    def delete(self, char_vocab):
        cursor = self.db.execute('''SELECT id
                                    FROM user WHERE char_vocab=?;''', (char_vocab, ))
        id_tuple = cursor.fetchone()
        if id_tuple is not None:
            self.db.execute('''DELETE FROM user WHERE id=?;''', id_tuple)
            self.db.commit()
