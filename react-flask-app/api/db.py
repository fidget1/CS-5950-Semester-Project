import sqlite3
from tweepy import StreamListener

DATABASE = 'data.db'


def open_db():

    with sqlite3.connect(DATABASE) as con:
        cur = con.cursor()
        cur.execute("DROP table IF EXISTS tweets;")
        cur.execute(
            "CREATE table tweets ("
                "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                "user TEXT NOT NULL,"
                "text TEXT NOT NULL,"
            "retweeted TEXT NOT NULL"
            ");"
        )
        return con
