from admin import add_question

science_questions = [
    {
        "category": "Science",
        "difficulty": "Easy",
        "question_type": "MCQ",
        "question_text": "What planet is known as the Red Planet?",
        "options": ["Earth", "Mars", "Jupiter", "Saturn"],
        "correct_answer": "Mars"
    },
    {
        "category": "Science",
        "difficulty": "Easy",
        "question_type": "MCQ",
        "question_text": "Water freezes at what temperature (Celsius)?",
        "options": ["0", "32", "100", "-10"],
        "correct_answer": "0"
    },
    {
        "category": "Science",
        "difficulty": "Medium",
        "question_type": "MCQ",
        "question_text": "What gas do plants absorb from the atmosphere?",
        "options": ["Oxygen", "Nitrogen", "Carbon Dioxide", "Helium"],
        "correct_answer": "Carbon Dioxide"
    },
    {
        "category": "Science",
        "difficulty": "Hard",
        "question_type": "MCQ",
        "question_text": "What is the chemical symbol for gold?",
        "options": ["Au", "Ag", "Gd", "Go"],
        "correct_answer": "Au"
    },
    {
        "category": "Science",
        "difficulty": "Medium",
        "question_type": "MCQ",
        "question_text": "Which organ in the human body produces insulin?",
        "options": ["Liver", "Pancreas", "Kidney", "Heart"],
        "correct_answer": "Pancreas"
    }
]

math_questions = [
    {
        "category": "Math",
        "difficulty": "Easy",
        "question_type": "MCQ",
        "question_text": "What is 5 + 7?",
        "options": ["10", "12", "13", "11"],
        "correct_answer": "12"
    },
    {
        "category": "Math",
        "difficulty": "Easy",
        "question_type": "MCQ",
        "question_text": "What is the square root of 81?",
        "options": ["7", "8", "9", "10"],
        "correct_answer": "9"
    },
    {
        "category": "Math",
        "difficulty": "Medium",
        "question_type": "MCQ",
        "question_text": "What is the value of pi (approx)?",
        "options": ["3.14", "2.71", "1.61", "1.41"],
        "correct_answer": "3.14"
    },
    {
        "category": "Math",
        "difficulty": "Hard",
        "question_type": "MCQ",
        "question_text": "What is the derivative of sin(x)?",
        "options": ["cos(x)", "-sin(x)", "-cos(x)", "sin(x)"],
        "correct_answer": "cos(x)"
    },
    {
        "category": "Math",
        "difficulty": "Medium",
        "question_type": "MCQ",
        "question_text": "What is 7 factorial (7!)?",
        "options": ["5040", "720", "120", "40320"],
        "correct_answer": "5040"
    }
]

history_questions = [
    {
        "category": "History",
        "difficulty": "Easy",
        "question_type": "MCQ",
        "question_text": "Who was the first President of the United States?",
        "options": ["Abraham Lincoln", "George Washington", "John Adams", "Thomas Jefferson"],
        "correct_answer": "George Washington"
    },
    {
        "category": "History",
        "difficulty": "Easy",
        "question_type": "MCQ",
        "question_text": "In which year did World War II end?",
        "options": ["1944", "1945", "1946", "1947"],
        "correct_answer": "1945"
    },
    {
        "category": "History",
        "difficulty": "Medium",
        "question_type": "MCQ",
        "question_text": "Which empire was ruled by Genghis Khan?",
        "options": ["Roman Empire", "Mongol Empire", "Ottoman Empire", "Persian Empire"],
        "correct_answer": "Mongol Empire"
    },
    {
        "category": "History",
        "difficulty": "Hard",
        "question_type": "MCQ",
        "question_text": "The Renaissance began in which country?",
        "options": ["France", "England", "Italy", "Germany"],
        "correct_answer": "Italy"
    },
    {
        "category": "History",
        "difficulty": "Medium",
        "question_type": "MCQ",
        "question_text": "Who was the British Prime Minister during World War II?",
        "options": ["Winston Churchill", "Neville Chamberlain", "Margaret Thatcher", "Tony Blair"],
        "correct_answer": "Winston Churchill"
    }
]

def add_all_questions():
    for q in science_questions + math_questions + history_questions:
        add_question(
            q["category"],
            q["difficulty"],
            q["question_type"],
            q["question_text"],
            q["options"],
            q["correct_answer"]
        )
    print("All questions added successfully!")

if __name__ == "__main__":
    add_all_questions()
