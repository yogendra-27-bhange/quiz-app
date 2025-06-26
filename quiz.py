import sqlite3
import json
import random
from database import connect_db
import datetime
from user import get_username_by_id

def get_questions(category, difficulty):
    """Get questions for specified category and difficulty"""
    if not category or not difficulty:
        return []
    
    conn = connect_db()
    c = conn.cursor()
    try:
        c.execute("""
            SELECT question_id, question_type, question_text, options, correct_answer 
            FROM questions 
            WHERE category=? AND difficulty=?
        """, (category, difficulty))
        rows = c.fetchall()
        
        questions = []
        for row in rows:
            q_id, q_type, q_text, opts_json, correct = row
            try:
                options = json.loads(opts_json) if opts_json else []
                questions.append({
                    'id': q_id,
                    'type': q_type,
                    'text': q_text,
                    'options': options,
                    'correct': correct
                })
            except json.JSONDecodeError:
                print(f"Error parsing options for question {q_id}")
                continue
        
        random.shuffle(questions)
        return questions
    except Exception as e:
        print(f"Error getting questions: {e}")
        return []
    finally:
        conn.close()

def save_score(user_id, category, score, difficulty):
    """Save quiz score to database"""
    if not user_id or not category or score is None:
        return False
    
    conn = connect_db()
    c = conn.cursor()
    try:
        date_taken = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        c.execute("""
            INSERT INTO scores (user_id, category, score, date_taken, difficulty) 
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, category, score, date_taken, difficulty))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error saving score: {e}")
        return False
    finally:
        conn.close()

def get_leaderboard(limit=20):
    """Get top scores for leaderboard"""
    conn = connect_db()
    c = conn.cursor()
    try:
        c.execute("""
            SELECT s.user_id, s.category, s.score, s.date_taken, s.difficulty
            FROM scores s
            ORDER BY s.score DESC, s.date_taken ASC
            LIMIT ?
        """, (limit,))
        
        rows = c.fetchall()
        leaderboard = []
        for row in rows:
            user_id, category, score, date_taken, difficulty = row
            username = get_username_by_id(user_id)
            if username:
                leaderboard.append({
                    'username': username,
                    'category': category,
                    'score': score,
                    'date': date_taken,
                    'difficulty': difficulty
                })
        return leaderboard
    except Exception as e:
        print(f"Error getting leaderboard: {e}")
        return []
    finally:
        conn.close()

def get_category_stats():
    """Get statistics by category"""
    conn = connect_db()
    c = conn.cursor()
    try:
        c.execute("""
            SELECT category, difficulty, 
                   COUNT(*) as total_attempts,
                   AVG(score) as avg_score,
                   MAX(score) as max_score
            FROM scores 
            GROUP BY category, difficulty
            ORDER BY category, difficulty
        """)
        
        rows = c.fetchall()
        stats = []
        for row in rows:
            category, difficulty, total_attempts, avg_score, max_score = row
            stats.append({
                'category': category,
                'difficulty': difficulty,
                'total_attempts': total_attempts,
                'avg_score': round(avg_score, 2) if avg_score else 0,
                'max_score': max_score
            })
        return stats
    except Exception as e:
        print(f"Error getting category stats: {e}")
        return []
    finally:
        conn.close()

def get_question_count(category=None, difficulty=None):
    """Get count of questions available"""
    conn = connect_db()
    c = conn.cursor()
    try:
        if category and difficulty:
            c.execute("SELECT COUNT(*) FROM questions WHERE category=? AND difficulty=?", 
                     (category, difficulty))
        elif category:
            c.execute("SELECT COUNT(*) FROM questions WHERE category=?", (category,))
        elif difficulty:
            c.execute("SELECT COUNT(*) FROM questions WHERE difficulty=?", (difficulty,))
        else:
            c.execute("SELECT COUNT(*) FROM questions")
        
        result = c.fetchone()
        return result[0] if result else 0
    except Exception as e:
        print(f"Error getting question count: {e}")
        return 0
    finally:
        conn.close()
