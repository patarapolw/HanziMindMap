import sys
import sqlite3

from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine

from HanziMindMap.user import UserVocab, UserHanzi
from HanziMindMap.db import Cedict, SpoonFed
from HanziMindMap.utils import Utils
from HanziMindMap.dir import resource_path


def main():
    sys.argv += ['--style', 'fusion']
    app = QGuiApplication(sys.argv)

    engine = QQmlApplicationEngine()
    engine.load("qml/main.qml")
    engine.quit.connect(app.quit)
    context = engine.rootContext()

    user_database = sqlite3.connect(resource_path("user.db"))
    user_vocab = UserVocab(user_database)
    context.setContextProperty('pyUserVocab', user_vocab)
    user_hanzi = UserHanzi(user_database)
    context.setContextProperty('pyUserHanzi', user_hanzi)

    dict_vocab = Cedict()
    context.setContextProperty('pyDictVocab', dict_vocab)
    dict_sentence = SpoonFed()
    context.setContextProperty('pyDictSentence', dict_sentence)

    utils = Utils()
    context.setContextProperty('py', utils)

    sys.exit(app.exec_())
