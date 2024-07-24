import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect('spelling_game.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        level TEXT NOT NULL,
        high_score INTEGER DEFAULT 0,
        last_login TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_stats (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        correct_words INTEGER DEFAULT 0,
        wrong_words INTEGER DEFAULT 0,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    ''')

    conn.commit()
    conn.close()

def add_user(username, level):
    conn = sqlite3.connect('spelling_game.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO users (username, level, last_login)
    VALUES (?, ?, ?)
    ''', (username, level, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    user_id = cursor.lastrowid
    cursor.execute('''
    INSERT INTO user_stats (user_id)
    VALUES (?)
    ''', (user_id,))
    conn.commit()
    conn.close()

def get_user(username):
    conn = sqlite3.connect('spelling_game.db')
    cursor = conn.cursor()
    cursor.execute('''
    SELECT id, username, level, high_score, last_login
    FROM users
    WHERE username = ?
    ''', (username,))
    user = cursor.fetchone()
    conn.close()
    return user

def update_last_login(user_id):
    conn = sqlite3.connect('spelling_game.db')
    cursor = conn.cursor()
    cursor.execute('''
    UPDATE users
    SET last_login = ?
    WHERE id = ?
    ''', (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), user_id))
    conn.commit()
    conn.close()

def update_score(user_id, correct, wrong):
    conn = sqlite3.connect('spelling_game.db')
    cursor = conn.cursor()
    cursor.execute('''
    UPDATE user_stats
    SET correct_words = correct_words + ?, wrong_words = wrong_words + ?
    WHERE user_id = ?
    ''', (correct, wrong, user_id))
    conn.commit()
    conn.close()

def get_user_stats(user_id):
    conn = sqlite3.connect('spelling_game.db')
    cursor = conn.cursor()
    cursor.execute('''
    SELECT correct_words, wrong_words
    FROM user_stats
    WHERE user_id = ?
    ''', (user_id,))
    stats = cursor.fetchone()
    conn.close()
    return stats
