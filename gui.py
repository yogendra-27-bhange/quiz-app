import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from tkinter.font import Font
import time
from user import register_user, login_user, get_user_stats
from quiz import get_questions, save_score, get_leaderboard
from database import connect_db
import threading

class ModernQuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz Master Pro")
        self.root.geometry("800x600")
        self.root.configure(bg='#2c3e50')
        
        # Set window icon and make it resizable
        self.root.resizable(True, True)
        self.root.minsize(600, 400)
        
        # Application state
        self.user_id = None
        self.username = None
        self.current_frame = None
        self.quiz_timer = None
        self.time_remaining = 0
        self.questions = []
        self.current_question_index = 0
        self.score = 0
        self.category = ""
        self.difficulty = ""
        
        # Configure styles
        self.setup_styles()
        
        # Start with login screen
        self.show_login_screen()
    
    def setup_styles(self):
        """Configure modern ttk styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        style.configure('Title.TLabel', 
                       font=('Arial', 24, 'bold'), 
                       foreground='#ecf0f1',
                       background='#2c3e50')
        
        style.configure('Subtitle.TLabel', 
                       font=('Arial', 14), 
                       foreground='#bdc3c7',
                       background='#2c3e50')
        
        style.configure('Modern.TButton',
                       font=('Arial', 12, 'bold'),
                       padding=10,
                       background='#3498db',
                       foreground='white')
        
        style.configure('Success.TButton',
                       font=('Arial', 12, 'bold'),
                       padding=10,
                       background='#27ae60',
                       foreground='white')
        
        style.configure('Warning.TButton',
                       font=('Arial', 12, 'bold'),
                       padding=10,
                       background='#e74c3c',
                       foreground='white')
        
        style.configure('Card.TFrame',
                       background='#34495e',
                       relief='raised',
                       borderwidth=2)
    
    def clear_screen(self):
        """Clear all widgets from the main window"""
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = tk.Frame(self.root, bg='#2c3e50')
        self.current_frame.pack(fill='both', expand=True, padx=20, pady=20)
    
    def show_login_screen(self):
        """Display the modern login screen"""
        self.clear_screen()
        
        # Main container
        main_container = tk.Frame(self.current_frame, bg='#2c3e50')
        main_container.pack(expand=True)
        
        # Title
        title_label = ttk.Label(main_container, 
                               text="Quiz Master Pro", 
                               style='Title.TLabel')
        title_label.pack(pady=(0, 10))
        
        subtitle_label = ttk.Label(main_container, 
                                  text="Test Your Knowledge", 
                                  style='Subtitle.TLabel')
        subtitle_label.pack(pady=(0, 30))
        
        # Login card
        login_card = tk.Frame(main_container, bg='#34495e', relief='raised', bd=2)
        login_card.pack(pady=20, padx=40, fill='x')
        
        # Username field
        tk.Label(login_card, text="Username", bg='#34495e', fg='#ecf0f1', 
                font=('Arial', 12)).pack(pady=(20, 5))
        self.username_entry = tk.Entry(login_card, font=('Arial', 12), 
                                      bg='#ecf0f1', fg='#2c3e50', relief='flat')
        self.username_entry.pack(pady=(0, 15), padx=20, fill='x')
        
        # Password field
        tk.Label(login_card, text="Password", bg='#34495e', fg='#ecf0f1', 
                font=('Arial', 12)).pack(pady=(0, 5))
        self.password_entry = tk.Entry(login_card, show="*", font=('Arial', 12), 
                                      bg='#ecf0f1', fg='#2c3e50', relief='flat')
        self.password_entry.pack(pady=(0, 20), padx=20, fill='x')
        
        # Buttons
        button_frame = tk.Frame(login_card, bg='#34495e')
        button_frame.pack(pady=(0, 20))
        
        login_btn = tk.Button(button_frame, text="Login", 
                             command=self.login,
                             bg='#3498db', fg='white', font=('Arial', 12, 'bold'),
                             relief='flat', padx=30, pady=10)
        login_btn.pack(side='left', padx=5)
        
        register_btn = tk.Button(button_frame, text="Register", 
                                command=self.register,
                                bg='#27ae60', fg='white', font=('Arial', 12, 'bold'),
                                relief='flat', padx=30, pady=10)
        register_btn.pack(side='left', padx=5)
        
        # Bind Enter key to login
        self.root.bind('<Return>', lambda e: self.login())
        
        # Focus on username entry
        self.username_entry.focus()
    
    def login(self):
        """Handle user login"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showwarning("Warning", "Please enter both username and password")
            return
        
        # Show loading
        self.show_loading("Logging in...")
        
        # Simulate loading (in real app, this would be async)
        self.root.after(1000, lambda: self._complete_login(username, password))
    
    def _complete_login(self, username, password):
        """Complete the login process"""
        user_id = login_user(username, password)
        if user_id:
            self.user_id = user_id
            self.username = username
            self.show_dashboard()
        else:
            messagebox.showerror("Error", "Invalid username or password")
            self.show_login_screen()
    
    def register(self):
        """Handle user registration"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showwarning("Warning", "Please enter both username and password")
            return
        
        if len(password) < 6:
            messagebox.showwarning("Warning", "Password must be at least 6 characters long")
            return
        
        if register_user(username, password):
            messagebox.showinfo("Success", "Registration successful! Please login.")
            self.username_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Username already exists")
    
    def show_loading(self, message):
        """Show loading screen"""
        self.clear_screen()
        
        loading_frame = tk.Frame(self.current_frame, bg='#2c3e50')
        loading_frame.pack(expand=True)
        
        ttk.Label(loading_frame, text=message, style='Subtitle.TLabel').pack()
        
        # Animated loading dots
        self.loading_dots = tk.Label(loading_frame, text="", bg='#2c3e50', fg='#3498db', 
                                   font=('Arial', 16))
        self.loading_dots.pack(pady=10)
        self.animate_loading()
    
    def animate_loading(self):
        """Animate loading dots"""
        dots = self.loading_dots.cget("text")
        if len(dots) >= 3:
            dots = ""
        else:
            dots += "."
        self.loading_dots.config(text=dots)
        self.root.after(500, self.animate_loading)
    
    def show_dashboard(self):
        """Display the main dashboard"""
        self.clear_screen()
        
        # Header
        header_frame = tk.Frame(self.current_frame, bg='#34495e')
        header_frame.pack(fill='x', pady=(0, 20))
        
        welcome_label = tk.Label(header_frame, 
                               text=f"Welcome, {self.username}!", 
                               bg='#34495e', fg='#ecf0f1', 
                               font=('Arial', 18, 'bold'))
        welcome_label.pack(side='left', padx=20, pady=10)
        
        logout_btn = tk.Button(header_frame, text="Logout", 
                              command=self.logout,
                              bg='#e74c3c', fg='white', font=('Arial', 10),
                              relief='flat', padx=15, pady=5)
        logout_btn.pack(side='right', padx=20, pady=10)
        
        # Main content
        content_frame = tk.Frame(self.current_frame, bg='#2c3e50')
        content_frame.pack(fill='both', expand=True)
        
        # Left panel - Quiz options
        left_panel = tk.Frame(content_frame, bg='#34495e', relief='raised', bd=2)
        left_panel.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        tk.Label(left_panel, text="Start New Quiz", bg='#34495e', fg='#ecf0f1', 
                font=('Arial', 16, 'bold')).pack(pady=20)
        
        # Category selection
        tk.Label(left_panel, text="Category:", bg='#34495e', fg='#ecf0f1', 
                font=('Arial', 12)).pack(pady=(0, 5))
        self.category_var = tk.StringVar(value="Science")
        category_menu = ttk.OptionMenu(left_panel, self.category_var, "Science", 
                                      "Science", "Math", "History", "Geography", "Literature")
        category_menu.pack(pady=(0, 15))
        
        # Difficulty selection
        tk.Label(left_panel, text="Difficulty:", bg='#34495e', fg='#ecf0f1', 
                font=('Arial', 12)).pack(pady=(0, 5))
        self.difficulty_var = tk.StringVar(value="Easy")
        difficulty_menu = ttk.OptionMenu(left_panel, self.difficulty_var, "Easy", 
                                        "Easy", "Medium", "Hard")
        difficulty_menu.pack(pady=(0, 20))
        
        # Start quiz button
        start_btn = tk.Button(left_panel, text="Start Quiz", 
                             command=self.start_quiz,
                             bg='#3498db', fg='white', font=('Arial', 14, 'bold'),
                             relief='flat', padx=40, pady=15)
        start_btn.pack(pady=(0, 20))
        
        # Right panel - Statistics
        right_panel = tk.Frame(content_frame, bg='#34495e', relief='raised', bd=2)
        right_panel.pack(side='right', fill='both', expand=True, padx=(10, 0))
        
        tk.Label(right_panel, text="Your Statistics", bg='#34495e', fg='#ecf0f1', 
                font=('Arial', 16, 'bold')).pack(pady=20)
        
        # Display user stats
        self.display_user_stats(right_panel)
        
        # Leaderboard button
        leaderboard_btn = tk.Button(right_panel, text="View Leaderboard", 
                                   command=self.show_leaderboard,
                                   bg='#f39c12', fg='white', font=('Arial', 12),
                                   relief='flat', padx=20, pady=10)
        leaderboard_btn.pack(pady=20)
    
    def display_user_stats(self, parent):
        """Display user statistics"""
        stats = get_user_stats(self.user_id)
        
        if not stats:
            tk.Label(parent, text="No quiz history yet", bg='#34495e', fg='#bdc3c7', 
                    font=('Arial', 12)).pack(pady=20)
            return
        
        # Create stats display
        for stat in stats:
            stat_frame = tk.Frame(parent, bg='#34495e')
            stat_frame.pack(fill='x', padx=20, pady=5)
            
            tk.Label(stat_frame, text=f"{stat['category']} ({stat['difficulty']})", 
                    bg='#34495e', fg='#ecf0f1', font=('Arial', 12, 'bold')).pack(anchor='w')
            tk.Label(stat_frame, text=f"Best Score: {stat['best_score']}/10", 
                    bg='#34495e', fg='#27ae60', font=('Arial', 11)).pack(anchor='w')
            tk.Label(stat_frame, text=f"Attempts: {stat['attempts']}", 
                    bg='#34495e', fg='#bdc3c7', font=('Arial', 10)).pack(anchor='w')
    
    def show_leaderboard(self):
        """Display leaderboard"""
        leaderboard = get_leaderboard()
        
        # Create new window for leaderboard
        leaderboard_window = tk.Toplevel(self.root)
        leaderboard_window.title("Leaderboard")
        leaderboard_window.geometry("600x400")
        leaderboard_window.configure(bg='#2c3e50')
        
        tk.Label(leaderboard_window, text="Top Performers", bg='#2c3e50', fg='#ecf0f1', 
                font=('Arial', 20, 'bold')).pack(pady=20)
        
        # Create treeview for leaderboard
        columns = ('Rank', 'Username', 'Category', 'Score', 'Date')
        tree = ttk.Treeview(leaderboard_window, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        
        tree.pack(padx=20, pady=20, fill='both', expand=True)
        
        # Populate leaderboard
        for i, entry in enumerate(leaderboard, 1):
            tree.insert('', 'end', values=(i, entry['username'], entry['category'], 
                                          f"{entry['score']}/10", entry['date']))
    
    def start_quiz(self):
        """Start a new quiz"""
        self.category = self.category_var.get()
        self.difficulty = self.difficulty_var.get()
        
        self.questions = get_questions(self.category, self.difficulty)
        if not self.questions:
            messagebox.showinfo("Info", "No questions available for selected category/difficulty.")
            return
        
        # Limit to 10 questions
        if len(self.questions) > 10:
            self.questions = self.questions[:10]
        
        self.score = 0
        self.current_question_index = 0
        self.time_remaining = 30  # 30 seconds per question
        
        self.show_question()
    
    def show_question(self):
        """Display current question"""
        self.clear_screen()
        
        if self.current_question_index >= len(self.questions):
            self.end_quiz()
            return
        
        # Header with progress and timer
        header_frame = tk.Frame(self.current_frame, bg='#34495e')
        header_frame.pack(fill='x', pady=(0, 20))
        
        progress_text = f"Question {self.current_question_index + 1} of {len(self.questions)}"
        tk.Label(header_frame, text=progress_text, bg='#34495e', fg='#ecf0f1', 
                font=('Arial', 14)).pack(side='left', padx=20, pady=10)
        
        self.timer_label = tk.Label(header_frame, text=f"Time: {self.time_remaining}s", 
                                   bg='#34495e', fg='#e74c3c', font=('Arial', 14, 'bold'))
        self.timer_label.pack(side='right', padx=20, pady=10)
        
        # Question card
        question_card = tk.Frame(self.current_frame, bg='#34495e', relief='raised', bd=2)
        question_card.pack(fill='both', expand=True, padx=20, pady=20)
        
        q = self.questions[self.current_question_index]
        
        # Question text
        question_text = tk.Text(question_card, height=4, wrap='word', 
                               bg='#ecf0f1', fg='#2c3e50', font=('Arial', 14),
                               relief='flat', padx=20, pady=20)
        question_text.insert('1.0', q['text'])
        question_text.config(state='disabled')
        question_text.pack(fill='x', padx=20, pady=20)
        
        # Options
        self.answer_var = tk.StringVar()
        options_frame = tk.Frame(question_card, bg='#34495e')
        options_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        for i, option in enumerate(q['options']):
            option_btn = tk.Radiobutton(options_frame, text=option, 
                                       variable=self.answer_var, value=option,
                                       bg='#34495e', fg='#ecf0f1', font=('Arial', 12),
                                       selectcolor='#2c3e50', activebackground='#34495e',
                                       activeforeground='#3498db')
            option_btn.pack(anchor='w', pady=5, padx=20)
        
        # Submit button
        submit_btn = tk.Button(question_card, text="Submit Answer", 
                              command=self.submit_answer,
                              bg='#3498db', fg='white', font=('Arial', 14, 'bold'),
                              relief='flat', padx=40, pady=15)
        submit_btn.pack(pady=20)
        
        # Start timer
        self.start_timer()
    
    def start_timer(self):
        """Start countdown timer for current question"""
        if self.time_remaining > 0:
            self.timer_label.config(text=f"Time: {self.time_remaining}s")
            self.time_remaining -= 1
            self.root.after(1000, self.start_timer)
        else:
            # Time's up - auto-submit
            self.submit_answer()
    
    def submit_answer(self):
        """Submit answer and move to next question"""
        selected = self.answer_var.get()
        if not selected:
            messagebox.showwarning("Warning", "Please select an answer")
            return
        
        # Check answer
        correct = self.questions[self.current_question_index]['correct']
        if selected == correct:
            self.score += 1
            messagebox.showinfo("Correct!", "Well done! That's the right answer.")
        else:
            messagebox.showinfo("Incorrect", f"The correct answer was: {correct}")
        
        self.current_question_index += 1
        self.show_question()
    
    def end_quiz(self):
        """End quiz and show results"""
        save_score(self.user_id, self.category, self.score, self.difficulty)
        
        self.clear_screen()
        
        # Results card
        results_card = tk.Frame(self.current_frame, bg='#34495e', relief='raised', bd=2)
        results_card.pack(expand=True, padx=40, pady=40)
        
        tk.Label(results_card, text="Quiz Complete!", bg='#34495e', fg='#ecf0f1', 
                font=('Arial', 24, 'bold')).pack(pady=30)
        
        score_text = f"Your Score: {self.score}/{len(self.questions)}"
        tk.Label(results_card, text=score_text, bg='#34495e', fg='#27ae60', 
                font=('Arial', 18, 'bold')).pack(pady=10)
        
        percentage = (self.score / len(self.questions)) * 100
        percentage_text = f"Percentage: {percentage:.1f}%"
        tk.Label(results_card, text=percentage_text, bg='#34495e', fg='#bdc3c7', 
                font=('Arial', 14)).pack(pady=10)
        
        # Performance message
        if percentage >= 90:
            performance_msg = "Excellent! Outstanding performance!"
            color = '#27ae60'
        elif percentage >= 70:
            performance_msg = "Good job! Well done!"
            color = '#f39c12'
        elif percentage >= 50:
            performance_msg = "Not bad! Keep practicing!"
            color = '#e67e22'
        else:
            performance_msg = "Keep studying! You'll improve!"
            color = '#e74c3c'
        
        tk.Label(results_card, text=performance_msg, bg='#34495e', fg=color, 
                font=('Arial', 12)).pack(pady=20)
        
        # Buttons
        button_frame = tk.Frame(results_card, bg='#34495e')
        button_frame.pack(pady=30)
        
        tk.Button(button_frame, text="Take Another Quiz", 
                 command=self.show_dashboard,
                 bg='#3498db', fg='white', font=('Arial', 12, 'bold'),
                 relief='flat', padx=20, pady=10).pack(side='left', padx=10)
        
        tk.Button(button_frame, text="View Leaderboard", 
                 command=self.show_leaderboard,
                 bg='#f39c12', fg='white', font=('Arial', 12, 'bold'),
                 relief='flat', padx=20, pady=10).pack(side='left', padx=10)
    
    def logout(self):
        """Logout user and return to login screen"""
        self.user_id = None
        self.username = None
        self.show_login_screen()

if __name__ == '__main__':
    root = tk.Tk()
    app = ModernQuizApp(root)
    root.mainloop()
