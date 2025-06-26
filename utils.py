import hashlib
import re
import string
import random

def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def validate_username(username):
    """Validate username format"""
    if not username:
        return False, "Username cannot be empty"
    
    if len(username) < 3:
        return False, "Username must be at least 3 characters long"
    
    if len(username) > 20:
        return False, "Username must be less than 20 characters"
    
    # Allow letters, numbers, and underscores only
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return False, "Username can only contain letters, numbers, and underscores"
    
    return True, "Username is valid"

def validate_password(password):
    """Validate password strength"""
    if not password:
        return False, "Password cannot be empty"
    
    if len(password) < 6:
        return False, "Password must be at least 6 characters long"
    
    if len(password) > 50:
        return False, "Password must be less than 50 characters"
    
    # Check for at least one letter and one number
    if not re.search(r'[a-zA-Z]', password):
        return False, "Password must contain at least one letter"
    
    if not re.search(r'\d', password):
        return False, "Password must contain at least one number"
    
    return True, "Password is valid"

def sanitize_input(text):
    """Sanitize user input to prevent injection attacks"""
    if not text:
        return ""
    
    # Remove potentially dangerous characters
    dangerous_chars = ['<', '>', '"', "'", '&', ';', '(', ')', '{', '}']
    for char in dangerous_chars:
        text = text.replace(char, '')
    
    return text.strip()

def format_time(seconds):
    """Format seconds into MM:SS format"""
    minutes = seconds // 60
    remaining_seconds = seconds % 60
    return f"{minutes:02d}:{remaining_seconds:02d}"

def format_score(score, total):
    """Format score as percentage"""
    if total == 0:
        return "0%"
    percentage = (score / total) * 100
    return f"{percentage:.1f}%"

def get_performance_message(percentage):
    """Get performance message based on percentage"""
    if percentage >= 90:
        return "Excellent! Outstanding performance!", '#27ae60'
    elif percentage >= 80:
        return "Great job! Very well done!", '#27ae60'
    elif percentage >= 70:
        return "Good work! Keep it up!", '#f39c12'
    elif percentage >= 60:
        return "Not bad! You're improving!", '#e67e22'
    elif percentage >= 50:
        return "You're getting there! Keep practicing!", '#e67e22'
    else:
        return "Keep studying! You'll improve with practice!", '#e74c3c'

def generate_random_string(length=8):
    """Generate a random string for temporary IDs"""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def validate_email(email):
    """Basic email validation"""
    if not email:
        return False, "Email cannot be empty"
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        return False, "Please enter a valid email address"
    
    return True, "Email is valid"

def truncate_text(text, max_length=50):
    """Truncate text to specified length"""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."

def format_date(date_string):
    """Format date string for display"""
    try:
        from datetime import datetime
        dt = datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
        return dt.strftime('%B %d, %Y at %I:%M %p')
    except:
        return date_string
