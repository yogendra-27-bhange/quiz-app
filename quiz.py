import sqlite3
import json
import random
from database import connect_db
import datetime

def get_questions(category, difficulty):
    conn = connect_db()
    c = conn.cursor()
    c.execute("SELECT question_id, question_type, question_text, options, correct_answer FROM questions WHERE category=? AND difficulty=?", (category, difficulty))
    rows = c.fetchall()
    conn.close()

    questions = []
    for row in rows:
        q_id, q_type, q_text, opts_json, correct = row
        options = json.loads(opts_json) if opts_json else []
        questions.append({
            'id': q_id,
            'type': q_type,
            'text': q_text,
            'options': options,
            'correct': correct
        })

    random.shuffle(questions)
    return questions

def save_score(user_id, category, score):
    conn = connect_db()
    c = conn.cursor()
    date_taken = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    c.execute("INSERT INTO scores (user_id, category, score, date_taken) VALUES (?, ?, ?, ?)",
              (user_id, category, score, date_taken))
    conn.commit()
    conn.close()
