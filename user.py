import sqlite3
from database import connect_db
from utils import hash_password

def register_user(username, password):
    """Register a new user with username and password"""
    if not username or not password:
        return False
    
    if len(username) < 3:
        return False
    
    conn = connect_db()
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", 
                  (username, hash_password(password)))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False  # Username already exists
    except Exception as e:
        print(f"Error registering user: {e}")
        return False
    finally:
        conn.close()

def login_user(username, password):
    """Authenticate user login"""
    if not username or not password:
        return None
    
    conn = connect_db()
    c = conn.cursor()
    try:
        c.execute("SELECT user_id, password_hash FROM users WHERE username=?", (username,))
        result = c.fetchone()
        if result and hash_password(password) == result[1]:
            return result[0]  # Return user_id on success
        return None
    except Exception as e:
        print(f"Error during login: {e}")
        return None
    finally:
        conn.close()

def get_user_stats(user_id):
    """Get user statistics for dashboard"""
    if not user_id:
        return []
    
    conn = connect_db()
    c = conn.cursor()
    try:
        # Get best scores and attempt counts by category and difficulty
        c.execute("""
            SELECT category, difficulty, 
                   MAX(score) as best_score, 
                   COUNT(*) as attempts
            FROM scores 
            WHERE user_id = ? 
            GROUP BY category, difficulty
            ORDER BY category, difficulty
        """, (user_id,))
        
        rows = c.fetchall()
        stats = []
        for row in rows:
            category, difficulty, best_score, attempts = row
            stats.append({
                'category': category,
                'difficulty': difficulty,
                'best_score': best_score,
                'attempts': attempts
            })
        return stats
    except Exception as e:
        print(f"Error getting user stats: {e}")
        return []
    finally:
        conn.close()

def get_username_by_id(user_id):
    """Get username by user ID"""
    if not user_id:
        return None
    
    conn = connect_db()
    c = conn.cursor()
    try:
        c.execute("SELECT username FROM users WHERE user_id = ?", (user_id,))
        result = c.fetchone()
        return result[0] if result else None
    except Exception as e:
        print(f"Error getting username: {e}")
        return None
    finally:
        conn.close()
