import sqlite3
from database import connect_db
from utils import hash_password

def register_user(username, password):
    conn = connect_db()
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", 
                  (username, hash_password(password)))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False  # Username already exists
    finally:
        conn.close()

def login_user(username, password):
    conn = connect_db()
    c = conn.cursor()
    c.execute("SELECT user_id, password_hash FROM users WHERE username=?", (username,))
    result = c.fetchone()
    conn.close()
    if result and hash_password(password) == result[1]:
        return result[0]  # Return user_id on success
    return None
