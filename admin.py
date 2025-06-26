import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
from database import connect_db
from quiz import get_category_stats, get_question_count
from user import get_username_by_id

class AdminPanel:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz Master Pro - Admin Panel")
        self.root.geometry("1000x700")
        self.root.configure(bg='#2c3e50')
        
        # Make it resizable
        self.root.resizable(True, True)
        self.root.minsize(800, 600)
        
        # Setup styles
        self.setup_styles()
        
        # Create main interface
        self.create_main_interface()
    
    def setup_styles(self):
        """Configure modern ttk styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure('Title.TLabel', 
                       font=('Arial', 20, 'bold'), 
                       foreground='#ecf0f1',
                       background='#2c3e50')
        
        style.configure('Subtitle.TLabel', 
                       font=('Arial', 12), 
                       foreground='#bdc3c7',
                       background='#2c3e50')
    
    def create_main_interface(self):
        """Create the main admin interface"""
        # Header
        header_frame = tk.Frame(self.root, bg='#34495e')
        header_frame.pack(fill='x', pady=(0, 20))
        
        title_label = ttk.Label(header_frame, text="Admin Panel", style='Title.TLabel')
        title_label.pack(pady=20)
        
        # Main content with tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Questions tab
        questions_frame = tk.Frame(notebook, bg='#2c3e50')
        notebook.add(questions_frame, text="Manage Questions")
        self.create_questions_tab(questions_frame)
        
        # Statistics tab
        stats_frame = tk.Frame(notebook, bg='#2c3e50')
        notebook.add(stats_frame, text="Statistics")
        self.create_stats_tab(stats_frame)
        
        # Users tab
        users_frame = tk.Frame(notebook, bg='#2c3e50')
        notebook.add(users_frame, text="Manage Users")
        self.create_users_tab(users_frame)
    
    def create_questions_tab(self, parent):
        """Create the questions management tab"""
        # Left panel - Add/Edit questions
        left_panel = tk.Frame(parent, bg='#34495e', relief='raised', bd=2)
        left_panel.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        tk.Label(left_panel, text="Add/Edit Question", bg='#34495e', fg='#ecf0f1', 
                font=('Arial', 16, 'bold')).pack(pady=20)
        
        # Question form
        form_frame = tk.Frame(left_panel, bg='#34495e')
        form_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Category
        tk.Label(form_frame, text="Category:", bg='#34495e', fg='#ecf0f1', 
                font=('Arial', 12)).pack(anchor='w', pady=(0, 5))
        self.category_var = tk.StringVar(value="Science")
        category_menu = ttk.OptionMenu(form_frame, self.category_var, "Science", 
                                      "Science", "Math", "History", "Geography", "Literature")
        category_menu.pack(fill='x', pady=(0, 15))
        
        # Difficulty
        tk.Label(form_frame, text="Difficulty:", bg='#34495e', fg='#ecf0f1', 
                font=('Arial', 12)).pack(anchor='w', pady=(0, 5))
        self.difficulty_var = tk.StringVar(value="Easy")
        difficulty_menu = ttk.OptionMenu(form_frame, self.difficulty_var, "Easy", 
                                        "Easy", "Medium", "Hard")
        difficulty_menu.pack(fill='x', pady=(0, 15))
        
        # Question text
        tk.Label(form_frame, text="Question:", bg='#34495e', fg='#ecf0f1', 
                font=('Arial', 12)).pack(anchor='w', pady=(0, 5))
        self.question_text = tk.Text(form_frame, height=4, wrap='word', 
                                    bg='#ecf0f1', fg='#2c3e50', font=('Arial', 11))
        self.question_text.pack(fill='x', pady=(0, 15))
        
        # Options
        tk.Label(form_frame, text="Options (one per line):", bg='#34495e', fg='#ecf0f1', 
                font=('Arial', 12)).pack(anchor='w', pady=(0, 5))
        self.options_text = tk.Text(form_frame, height=4, wrap='word', 
                                   bg='#ecf0f1', fg='#2c3e50', font=('Arial', 11))
        self.options_text.pack(fill='x', pady=(0, 15))
        
        # Correct answer
        tk.Label(form_frame, text="Correct Answer:", bg='#34495e', fg='#ecf0f1', 
                font=('Arial', 12)).pack(anchor='w', pady=(0, 5))
        self.correct_answer = tk.Entry(form_frame, bg='#ecf0f1', fg='#2c3e50', 
                                      font=('Arial', 11))
        self.correct_answer.pack(fill='x', pady=(0, 20))
        
        # Buttons
        button_frame = tk.Frame(form_frame, bg='#34495e')
        button_frame.pack(fill='x')
        
        tk.Button(button_frame, text="Add Question", 
                 command=self.add_question,
                 bg='#27ae60', fg='white', font=('Arial', 12, 'bold'),
                 relief='flat', padx=20, pady=10).pack(side='left', padx=(0, 10))
        
        tk.Button(button_frame, text="Clear Form", 
                 command=self.clear_question_form,
                 bg='#95a5a6', fg='white', font=('Arial', 12, 'bold'),
                 relief='flat', padx=20, pady=10).pack(side='left')
        
        # Right panel - Question list
        right_panel = tk.Frame(parent, bg='#34495e', relief='raised', bd=2)
        right_panel.pack(side='right', fill='both', expand=True, padx=(10, 0))
        
        tk.Label(right_panel, text="Question List", bg='#34495e', fg='#ecf0f1', 
                font=('Arial', 16, 'bold')).pack(pady=20)
        
        # Filter frame
        filter_frame = tk.Frame(right_panel, bg='#34495e')
        filter_frame.pack(fill='x', padx=20, pady=(0, 10))
        
        tk.Label(filter_frame, text="Filter:", bg='#34495e', fg='#ecf0f1', 
                font=('Arial', 10)).pack(side='left')
        
        self.filter_category = tk.StringVar(value="All")
        filter_menu = ttk.OptionMenu(filter_frame, self.filter_category, "All", 
                                    "All", "Science", "Math", "History", "Geography", "Literature",
                                    command=self.refresh_question_list)
        filter_menu.pack(side='left', padx=10)
        
        # Question list
        self.create_question_list(right_panel)
    
    def create_question_list(self, parent):
        """Create the question list display"""
        # Create treeview
        columns = ('ID', 'Category', 'Difficulty', 'Question', 'Options', 'Correct')
        self.question_tree = ttk.Treeview(parent, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.question_tree.heading(col, text=col)
            if col == 'Question':
                self.question_tree.column(col, width=200)
            elif col == 'Options':
                self.question_tree.column(col, width=150)
            else:
                self.question_tree.column(col, width=80)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(parent, orient='vertical', command=self.question_tree.yview)
        self.question_tree.configure(yscrollcommand=scrollbar.set)
        
        self.question_tree.pack(side='left', fill='both', expand=True, padx=20, pady=20)
        scrollbar.pack(side='right', fill='y', pady=20)
        
        # Bind double-click to edit
        self.question_tree.bind('<Double-1>', self.edit_question)
        
        # Load questions
        self.refresh_question_list()
    
    def refresh_question_list(self, event=None):
        """Refresh the question list"""
        # Clear existing items
        for item in self.question_tree.get_children():
            self.question_tree.delete(item)
        
        # Load questions from database
        conn = connect_db()
        if not conn:
            return
        
        c = conn.cursor()
        try:
            filter_cat = self.filter_category.get()
            if filter_cat == "All":
                c.execute("SELECT question_id, category, difficulty, question_text, options, correct_answer FROM questions ORDER BY category, difficulty")
            else:
                c.execute("SELECT question_id, category, difficulty, question_text, options, correct_answer FROM questions WHERE category=? ORDER BY difficulty", (filter_cat,))
            
            rows = c.fetchall()
            for row in rows:
                q_id, category, difficulty, question_text, options_json, correct = row
                try:
                    options = json.loads(options_json) if options_json else []
                    options_text = ", ".join(options[:2]) + "..." if len(options) > 2 else ", ".join(options)
                except:
                    options_text = "Error parsing options"
                
                # Truncate question text
                question_display = question_text[:50] + "..." if len(question_text) > 50 else question_text
                
                self.question_tree.insert('', 'end', values=(q_id, category, difficulty, question_display, options_text, correct))
        except Exception as e:
            messagebox.showerror("Error", f"Error loading questions: {e}")
        finally:
            conn.close()
    
    def add_question(self):
        """Add a new question to the database"""
        category = self.category_var.get()
        difficulty = self.difficulty_var.get()
        question_text = self.question_text.get('1.0', tk.END).strip()
        options_text = self.options_text.get('1.0', tk.END).strip()
        correct_answer = self.correct_answer.get().strip()
        
        # Validation
        if not question_text:
            messagebox.showwarning("Warning", "Please enter a question")
            return
        
        if not options_text:
            messagebox.showwarning("Warning", "Please enter options")
            return
        
        if not correct_answer:
            messagebox.showwarning("Warning", "Please enter the correct answer")
            return
        
        # Parse options
        options = [opt.strip() for opt in options_text.split('\n') if opt.strip()]
        if len(options) < 2:
            messagebox.showwarning("Warning", "Please enter at least 2 options")
            return
        
        if correct_answer not in options:
            messagebox.showwarning("Warning", "Correct answer must be one of the options")
            return
        
        # Save to database
        conn = connect_db()
        if not conn:
            return
        
        c = conn.cursor()
        try:
            c.execute("""
                INSERT INTO questions (category, difficulty, question_type, question_text, options, correct_answer)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (category, difficulty, "multiple_choice", question_text, json.dumps(options), correct_answer))
            conn.commit()
            messagebox.showinfo("Success", "Question added successfully!")
            self.clear_question_form()
            self.refresh_question_list()
        except Exception as e:
            messagebox.showerror("Error", f"Error adding question: {e}")
        finally:
            conn.close()
    
    def clear_question_form(self):
        """Clear the question form"""
        self.question_text.delete('1.0', tk.END)
        self.options_text.delete('1.0', tk.END)
        self.correct_answer.delete(0, tk.END)
    
    def edit_question(self, event):
        """Edit selected question"""
        selection = self.question_tree.selection()
        if not selection:
            return
        
        item = self.question_tree.item(selection[0])
        question_id = item['values'][0]
        
        # Load question details
        conn = connect_db()
        if not conn:
            return
        
        c = conn.cursor()
        try:
            c.execute("SELECT category, difficulty, question_text, options, correct_answer FROM questions WHERE question_id=?", (question_id,))
            row = c.fetchone()
            if row:
                category, difficulty, question_text, options_json, correct_answer = row
                
                # Populate form
                self.category_var.set(category)
                self.difficulty_var.set(difficulty)
                self.question_text.delete('1.0', tk.END)
                self.question_text.insert('1.0', question_text)
                
                try:
                    options = json.loads(options_json) if options_json else []
                    self.options_text.delete('1.0', tk.END)
                    self.options_text.insert('1.0', '\n'.join(options))
                except:
                    pass
                
                self.correct_answer.delete(0, tk.END)
                self.correct_answer.insert(0, correct_answer)
                
                # Change button to update
                # (In a full implementation, you'd change the button text and command)
        except Exception as e:
            messagebox.showerror("Error", f"Error loading question: {e}")
        finally:
            conn.close()
    
    def create_stats_tab(self, parent):
        """Create the statistics tab"""
        # Header
        header_frame = tk.Frame(parent, bg='#34495e')
        header_frame.pack(fill='x', pady=(0, 20))
        
        tk.Label(header_frame, text="Quiz Statistics", bg='#34495e', fg='#ecf0f1', 
                font=('Arial', 18, 'bold')).pack(pady=20)
        
        # Stats display
        stats_frame = tk.Frame(parent, bg='#34495e', relief='raised', bd=2)
        stats_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Create treeview for stats
        columns = ('Category', 'Difficulty', 'Total Attempts', 'Avg Score', 'Max Score')
        self.stats_tree = ttk.Treeview(stats_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.stats_tree.heading(col, text=col)
            self.stats_tree.column(col, width=120)
        
        self.stats_tree.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Load statistics
        self.load_statistics()
    
    def load_statistics(self):
        """Load and display statistics"""
        # Clear existing items
        for item in self.stats_tree.get_children():
            self.stats_tree.delete(item)
        
        # Get statistics
        stats = get_category_stats()
        
        # Display statistics
        for stat in stats:
            self.stats_tree.insert('', 'end', values=(
                stat['category'],
                stat['difficulty'],
                stat['total_attempts'],
                stat['avg_score'],
                stat['max_score']
            ))
    
    def create_users_tab(self, parent):
        """Create the users management tab"""
        # Header
        header_frame = tk.Frame(parent, bg='#34495e')
        header_frame.pack(fill='x', pady=(0, 20))
        
        tk.Label(header_frame, text="User Management", bg='#34495e', fg='#ecf0f1', 
                font=('Arial', 18, 'bold')).pack(pady=20)
        
        # Users list
        users_frame = tk.Frame(parent, bg='#34495e', relief='raised', bd=2)
        users_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Create treeview for users
        columns = ('User ID', 'Username', 'Created Date', 'Total Quizzes')
        self.users_tree = ttk.Treeview(users_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.users_tree.heading(col, text=col)
            self.users_tree.column(col, width=120)
        
        self.users_tree.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Load users
        self.load_users()
    
    def load_users(self):
        """Load and display users"""
        # Clear existing items
        for item in self.users_tree.get_children():
            self.users_tree.delete(item)
        
        # Get users from database
        conn = connect_db()
        if not conn:
            return
        
        c = conn.cursor()
        try:
            c.execute("""
                SELECT u.user_id, u.username, u.created_date, COUNT(s.score_id) as quiz_count
                FROM users u
                LEFT JOIN scores s ON u.user_id = s.user_id
                GROUP BY u.user_id, u.username, u.created_date
                ORDER BY u.username
            """)
            
            rows = c.fetchall()
            for row in rows:
                user_id, username, created_date, quiz_count = row
                self.users_tree.insert('', 'end', values=(user_id, username, created_date, quiz_count))
        except Exception as e:
            messagebox.showerror("Error", f"Error loading users: {e}")
        finally:
            conn.close()

def main():
    """Main function to run admin panel"""
    root = tk.Tk()
    app = AdminPanel(root)
    root.mainloop()

if __name__ == '__main__':
    main()

