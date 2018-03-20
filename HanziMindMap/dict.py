import re
import json

from PyQt5.QtCore import QObject, pyqtSlot, pyqtProperty

from HanziMindMap.dir import database_path


class Cedict(QObject):
    def __init__(self):
        super().__init__()
        self.dictionary = dict()
        with open(database_path('cedict.txt'), encoding='utf8') as f:
            for row in f.readlines():
                result = re.search(r'(\w+) (\w+) \[(.+)\] /(.+)/\n', row)
                if result is not None:
                    trad, simp, pinyin, eng = result.groups()
                    self.dictionary.setdefault(simp, [])
                    self.dictionary.setdefault(trad, [])
                    self.dictionary[simp].append({
                        'traditional': trad,
                        'simplified': simp,
                        'reading': pinyin,
                        'english': eng
                    })
                    if trad != simp:
                        self.dictionary[trad].append(self.dictionary[simp][-1])

        self._lookup = []

    @pyqtSlot(str)
    def do_lookup(self, vocab):
        if vocab in self.dictionary:
            self._lookup = self.dictionary[vocab]
        else:
            self._lookup = []

    @pyqtProperty(str)
    def get_lookup(self):
        return json.dumps(self._lookup)


class SpoonFed(QObject):
    def __init__(self):
        super().__init__()
        self.dictionary = dict()
        with open(database_path('SpoonFed.tsv'), encoding='utf8') as f:
            for row in f.readlines():
                eng, reading, sentence, _, sentence_id = row.strip().split('\t')
                self.dictionary[sentence_id] = {
                    'id': sentence_id,
                    'sentence': sentence,
                    'reading': reading,
                    'english': eng
                }

        self._lookup = []

    def iter_lookup(self, vocab):
        if vocab:
            for entry in self.dictionary.values():
                if vocab in entry['sentence']:
                    yield entry

    @pyqtSlot(str)
    def do_lookup(self, vocab):
        self._lookup = list(self.iter_lookup(vocab))

    @pyqtProperty(str)
    def get_lookup(self):
        return json.dumps(self._lookup)
