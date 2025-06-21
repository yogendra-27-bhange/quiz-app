import tkinter as tk
from tkinter import messagebox
from user import register_user, login_user
from quiz import get_questions, save_score

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Quiz Application")
        self.user_id = None
        self.create_login_screen()

    def create_login_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Username").pack()
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack()
        tk.Label(self.root, text="Password").pack()
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack()

        tk.Button(self.root, text="Login", command=self.login).pack()
        tk.Button(self.root, text="Register", command=self.register).pack()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        user_id = login_user(username, password)
        if user_id:
            self.user_id = user_id
            self.create_quiz_selection_screen()
        else:
            messagebox.showerror("Error", "Invalid username or password")

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if register_user(username, password):
            messagebox.showinfo("Success", "Registration successful! Please login.")
        else:
            messagebox.showerror("Error", "Username already exists")

    def create_quiz_selection_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Select Category").pack()
        self.category_var = tk.StringVar(value="Science")
        tk.OptionMenu(self.root, self.category_var, "Science", "Math", "History").pack()

        tk.Label(self.root, text="Select Difficulty").pack()
        self.difficulty_var = tk.StringVar(value="Easy")
        tk.OptionMenu(self.root, self.difficulty_var, "Easy", "Medium", "Hard").pack()

        tk.Button(self.root, text="Start Quiz", command=self.start_quiz).pack()

    def start_quiz(self):
        category = self.category_var.get()
        difficulty = self.difficulty_var.get()
        self.questions = get_questions(category, difficulty)
        if not self.questions:
            messagebox.showinfo("Info", "No questions available for selected category/difficulty.")
            return
        self.score = 0
        self.current_question_index = 0
        self.category = category
        self.show_question()

    def show_question(self):
        self.clear_screen()
        if self.current_question_index >= len(self.questions):
            self.end_quiz()
            return
        q = self.questions[self.current_question_index]
        tk.Label(self.root, text=f"Q{self.current_question_index+1}: {q['text']}").pack()
        self.answer_var = tk.StringVar()
        for option in q['options']:
            tk.Radiobutton(self.root, text=option, variable=self.answer_var, value=option).pack()
        tk.Button(self.root, text="Submit", command=self.submit_answer).pack()

    def submit_answer(self):
        selected = self.answer_var.get()
        if not selected:
            messagebox.showwarning("Warning", "Please select an answer")
            return
        correct = self.questions[self.current_question_index]['correct']
        if selected == correct:
            self.score += 1
        self.current_question_index += 1
        self.show_question()

    def end_quiz(self):
        save_score(self.user_id, self.category, self.score)
        self.clear_screen()
        tk.Label(self.root, text=f"Quiz Finished! Your Score: {self.score}").pack()
        tk.Button(self.root, text="Logout", command=self.create_login_screen).pack()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == '__main__':
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
