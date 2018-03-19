from PyQt5.QtWidgets import QPlainTextEdit


class MainWindow(QPlainTextEdit):
    def __init__(self, db):
        super().__init__()
        self.db = db

        self.setPlainText(str(self.db))
        self.setStyleSheet("font-family: monospace")
        self.setMinimumSize(500, 400)
        self.show()


def load(db):
    return MainWindow(db)
