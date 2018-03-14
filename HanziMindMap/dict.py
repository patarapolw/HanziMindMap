import re

from HanziMindMap.dir import database_path


class Cedict:
    def __init__(self):
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


class Edict2:
    def __init__(self):
        self.dictionary = dict()
        with open(database_path('edict2'), encoding='euc-jp') as f:
            for row in f.readlines():
                jap = kana = eng = ''
                result = re.search(r'(\w+) \[(.+)\] /(.+)/\n', row)
                if result is None:
                    result = re.search(r'(\w+) /(.+)/\n', row)
                    if result is not None:
                        jap, eng = result.groups()
                        kana = jap
                else:
                    jap, kana, eng = result.groups()

                self.dictionary.setdefault(jap, [])
                self.dictionary.setdefault(kana, [])
                self.dictionary[jap].append({
                    'japanese': jap,
                    'reading': kana,
                    'english': eng
                })

                if jap != kana:
                    self.dictionary[kana].append(self.dictionary[jap][-1])
