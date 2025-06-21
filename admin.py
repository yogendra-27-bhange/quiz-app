import json
from database import connect_db

def add_question(category, difficulty, question_type, question_text, options, correct_answer):
    conn = connect_db()
    c = conn.cursor()
    options_json = json.dumps(options) if options else None
    c.execute('''INSERT INTO questions (category, difficulty, question_type, question_text, options, correct_answer)
                 VALUES (?, ?, ?, ?, ?, ?)''',
                 (category, difficulty, question_type, question_text, options_json, correct_answer))
    conn.commit()
    conn.close()

def get_all_questions():
    conn = connect_db()
    c = conn.cursor()
    c.execute("SELECT * FROM questions")
    questions = c.fetchall()
    conn.close()
    return questions

# You can add more admin functions (edit, delete) as needed.

