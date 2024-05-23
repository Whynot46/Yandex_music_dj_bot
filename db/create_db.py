import sqlite3 as sql


connection = sql.connect('./db/User_db.db')
cursor = connection.cursor()

cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS Users (
        username TEXT NOT NULL,
        user_id INTEGER NOT NULL,
        playlist TEXT
        )
        ''')

connection.commit()