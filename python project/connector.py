# Make sure to install the mysql-connector-python package using pip:
# pip install mysql-connector-python

import mysql.connector
from mysql.connector import Error
import string
import random
import tkinter as tk
from tkinter import ttk, messagebox

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'database': 'password_generator',
    'user': 'root',
    'password': 'PruthviR%123'
}

def create_db_connection():
    """Create and return a database connection"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        messagebox.showerror("Database Error", f"Error connecting to MySQL: {e}")
        return None

def save_to_database(user_name, password_length, use_lower, use_upper, use_digits, use_specials, generated_password):
    """Save the password generation data to the database"""
    connection = create_db_connection()
    if connection is None:
        return False
    
    try:
        cursor = connection.cursor()
        
        # Insert user if not exists
        cursor.execute("INSERT IGNORE INTO users (name) VALUES (%s)", (user_name,))
        
        # Get user ID
        cursor.execute("SELECT user_id FROM users WHERE name = %s", (user_name,))
        user_id = cursor.fetchone()[0]
        
        # Insert password request
        cursor.execute("""
            INSERT INTO password_requests 
            (user_id, password_length, use_lowercase, use_uppercase, use_digits, use_special_chars, is_valid) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (user_id, password_length, use_lower, use_upper, use_digits, use_specials, True))
        
        request_id = cursor.lastrowid
        
        # Insert generated password
        cursor.execute("""
            INSERT INTO generated_passwords (request_id, password) 
            VALUES (%s, %s)
        """, (request_id, generated_password))
        
        connection.commit()
        return True
        
    except Error as e:
        connection.rollback()
        messagebox.showerror("Database Error", f"Error saving to database: {e}")
        return False
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def generate_password(length, use_lower, use_upper, use_digits, use_specials):
    chars = ""
    if use_lower:
        chars += string.ascii_lowercase
    if use_upper:
        chars += string.ascii_uppercase
    if use_digits:
        chars += string.digits
    if use_specials:
        chars += string.punctuation

    if not chars or length < 4:
        return ""

    # Ensure at least one of each selected type
    password = []
    if use_lower:
        password.append(random.choice(string.ascii_lowercase))
    if use_upper:
        password.append(random.choice(string.ascii_uppercase))
    if use_digits:
        password.append(random.choice(string.digits))
    if use_specials:
        password.append(random.choice(string.punctuation))

    # Fill the rest of the password length
    while len(password) < length:
        password.append(random.choice(chars))

    random.shuffle(password)
    return ''.join(password[:length])