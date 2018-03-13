import re

from HanziMindMap.dir import database_path


class Cedict:
    def __init__(self):
        self.cedict = dict()
        with open(database_path('cedict.txt'), encoding='utf8') as f:
            for row in f.readlines():
                result = re.search(r'(\w+) (\w+) \[(.+)\] /(.+)/\n', row)
                if result is not None:
                    trad, simp, pinyin, eng = result.groups()
                    self.cedict[simp] = {
                        'traditional': trad,
                        'simplified': simp,
                        'pinyin': pinyin,
                        'english': eng
                    }
                    self.cedict[trad] = self.cedict[simp].copy()
