import database
import gui
import tkinter as tk

def main():
    """Main entry point for the Quiz Application"""
    # Initialize database
    database.create_tables()
    
    # Create and run GUI
    root = tk.Tk()
    app = gui.QuizApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()
