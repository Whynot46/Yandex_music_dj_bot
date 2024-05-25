import sqlite3 as sql
import pandas as pd
from src.config import DB_PATH


def add_new_user(user_id, username):
    connection = sql.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute('''
            INSERT INTO Users (username, user_id)
            VALUES (?, ?)
        ''', (username, user_id))
    connection.commit()
    

def is_old(user_id):
    connection = sql.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute("SELECT 1 FROM Users WHERE user_id = ?", (user_id,))
    result  = cursor.fetchone()
    connection.commit()
    return bool(result)


def get_playlist(user_id):
    connection = sql.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute("SELECT playlist FROM Users WHERE user_id = ?", (user_id,))
    result  = cursor.fetchone()
    connection.commit()
    if result[0]!=None:
        playlist_string = result[0]
        playlist = playlist_string.split("|")
        return playlist
    else: return []
    
    
def put_track_to_playlist(user_id, track_name):
    connection = sql.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute("SELECT playlist FROM Users WHERE user_id = ?", (user_id,))
    result  = cursor.fetchone()
    connection.commit()
    if result[0]:
        playlist = result[0]
        playlist = playlist.split('|')
        playlist.append(track_name)
        playlist = '|'.join(playlist)
        cursor.execute("UPDATE Users SET playlist = ? WHERE user_id = ?", (playlist, user_id))
        connection.commit()
    else:
        playlist = f"{track_name}"
        cursor.execute("UPDATE Users SET playlist = ? WHERE user_id = ?", (str(playlist), user_id))
        connection.commit()   


def get_xlsx():
    connection = sql.connect(DB_PATH) 
    xlsx_file = pd.read_sql_query('SELECT username, user_id FROM User', connection) 
    xlsx_file.to_excel("./db/data.xlsx", index=False)  
    connection.close() 
    
