import sqlite3
import os

def connect_db():
    """Create and return database connection"""
    try:
        conn = sqlite3.connect('quiz_app.db')
        conn.row_factory = sqlite3.Row  # Enable row factory for dict-like access
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

def create_tables():
    """Create all necessary database tables"""
    conn = connect_db()
    if not conn:
        return False
    
    c = conn.cursor()
    try:
        # Users table
        c.execute('''CREATE TABLE IF NOT EXISTS users (
                        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        password_hash TEXT NOT NULL,
                        created_date TEXT DEFAULT CURRENT_TIMESTAMP)''')

        # Questions table
        c.execute('''CREATE TABLE IF NOT EXISTS questions (
                        question_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        category TEXT NOT NULL,
                        difficulty TEXT NOT NULL,
                        question_type TEXT NOT NULL,
                        question_text TEXT NOT NULL,
                        options TEXT,
                        correct_answer TEXT NOT NULL,
                        created_date TEXT DEFAULT CURRENT_TIMESTAMP)''')

        # Scores table with difficulty field
        c.execute('''CREATE TABLE IF NOT EXISTS scores (
                        score_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL,
                        category TEXT NOT NULL,
                        difficulty TEXT NOT NULL,
                        score INTEGER NOT NULL,
                        date_taken TEXT NOT NULL,
                        FOREIGN KEY(user_id) REFERENCES users(user_id))''')

        # Add difficulty column to scores if it doesn't exist
        try:
            c.execute("ALTER TABLE scores ADD COLUMN difficulty TEXT DEFAULT 'Easy'")
        except sqlite3.OperationalError:
            # Column already exists
            pass

        conn.commit()
        return True
    except Exception as e:
        print(f"Error creating tables: {e}")
        return False
    finally:
        conn.close()

def reset_database():
    """Reset the entire database (for testing)"""
    try:
        if os.path.exists('quiz_app.db'):
            os.remove('quiz_app.db')
        return create_tables()
    except Exception as e:
        print(f"Error resetting database: {e}")
        return False

def backup_database():
    """Create a backup of the database"""
    try:
        import shutil
        from datetime import datetime
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_name = f'quiz_app_backup_{timestamp}.db'
        shutil.copy2('quiz_app.db', backup_name)
        return backup_name
    except Exception as e:
        print(f"Error backing up database: {e}")
        return None

if __name__ == '__main__':
    create_tables()
