import sqlite3
from HanziMindMap.dir import resource_path


if __name__ == '__main__':
    db = sqlite3.connect(resource_path("user.db"))
    cursor = db.execute('SELECT * FROM user')
    for row in cursor:
        print(row)
