import sqlite3

def connect_db():
    conn = sqlite3.connect('quiz_app.db')
    return conn

def create_tables():
    conn = connect_db()
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL)''')

    c.execute('''CREATE TABLE IF NOT EXISTS questions (
                    question_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category TEXT NOT NULL,
                    difficulty TEXT NOT NULL,
                    question_type TEXT NOT NULL,
                    question_text TEXT NOT NULL,
                    options TEXT,
                    correct_answer TEXT NOT NULL)''')

    c.execute('''CREATE TABLE IF NOT EXISTS scores (
                    score_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    category TEXT NOT NULL,
                    score INTEGER NOT NULL,
                    date_taken TEXT NOT NULL,
                    FOREIGN KEY(user_id) REFERENCES users(user_id))''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_tables()
