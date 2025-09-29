import mysql.connector
from mysql.connector import Error
import datetime

# ... your existing imports and PasswordGeneratorApp class code here ...

class PasswordGeneratorApp:
    def __init__(self, root):
        # ... existing init code ...
        self.init_db_connection()
        # rest of your init

    def init_db_connection(self):
        try:
            self.connection = mysql.connector.connect(
                host='localhost',      # Your MySQL host
                database='passwords_db',  # Your database name
                user='your_user',      # Your MySQL user
                password='your_password' # Your MySQL password
            )
            if self.connection.is_connected():
                print("Connected to MySQL database")
                self.create_table_if_not_exists()
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            self.connection = None

    def create_table_if_not_exists(self):
        create_table_query = """
        CREATE TABLE IF NOT EXISTS generated_passwords (
            id INT AUTO_INCREMENT PRIMARY KEY,
            password VARCHAR(100) NOT NULL,
            length INT NOT NULL,
            strength VARCHAR(20) NOT NULL,
            generated_at DATETIME NOT NULL
        );
        """
        cursor = self.connection.cursor()
        cursor.execute(create_table_query)
        self.connection.commit()
        cursor.close()

    def save_password_to_db(self, password, length, strength_text):
        if not self.connection or not self.connection.is_connected():
            print("No database connection.")
            return

        insert_query = """
        INSERT INTO generated_passwords (password, length, strength, generated_at)
        VALUES (%s, %s, %s, %s);
        """
        cursor = self.connection.cursor()
        try:
            cursor.execute(insert_query, (password, length, strength_text, datetime.datetime.now()))
            self.connection.commit()
            print("Password saved to database.")
        except Error as e:
            print(f"Failed to insert record: {e}")
        finally:
            cursor.close()

    def generate_password(self):
        # ... your existing generate_password code ...

        # At the end, after setting password and strength:
        password = self.password_var.get()
        self.copy_btn.config(state=tk.NORMAL)

        # Update strength meter and get strength text
        strength_text = self.update_strength_meter(length, use_upper, use_lower, use_digits, use_symbols)

        # Save to DB
        self.save_password_to_db(password, length, strength_text)

    def update_strength_meter(self, length, upper, lower, digits, symbols):
        # ... existing strength calculation ...
        char_types = sum([upper, lower, digits, symbols])
        strength = min(100, (length * 2) + (char_types * 15))

        self.strength_meter['value'] = strength

        if strength < 40:
            strength_text = "Weak"
            color = "#ff6b6b"
        elif strength < 70:
            strength_text = "Moderate"
            color = "#f9a73e"
        else:
            strength_text = "Strong"
            color = "#4caf50"

        self.strength_label.config(text=f"Strength: {strength_text}", foreground=color)
        self.strength_meter.configure(style="Color.Horizontal.TProgressbar")

        # Configure progress bar color
        style = ttk.Style()
        style.configure("Color.Horizontal.TProgressbar", troughcolor=self.bg_color,
                        background=color, bordercolor=self.bg_color)

        return strength_text  # Return the strength for DB saving

# ... rest of your code unchanged ...