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
                    self.cedict.setdefault(simp, [])
                    self.cedict.setdefault(trad, [])
                    self.cedict[simp].append({
                        'traditional': trad,
                        'simplified': simp,
                        'pinyin': pinyin,
                        'english': eng
                    })
                    if trad != simp:
                        self.cedict[trad].append(self.cedict[simp][-1])
