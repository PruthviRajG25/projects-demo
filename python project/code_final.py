import string
import secrets
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.font import Font

class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Generator")
        self.root.geometry("400x450")
        self.root.resizable(False, False)
        self.configure_styles()
        self.create_widgets()
        
    def configure_styles(self):
        # Color scheme
        self.bg_color = "#f5f7fa"
        self.primary_color = "#4b6cb7"
        self.secondary_color = "#6c8ae4"
        self.accent_color = "#ff6b6b"
        self.text_color = "#2d3748"
        self.light_text = "#718096"
        
        # Configure ttk styles
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TFrame', background=self.bg_color)
        style.configure('TLabel', background=self.bg_color, foreground=self.text_color)
        style.configure('TCheckbutton', background=self.bg_color, foreground=self.text_color)
        style.configure('TButton', background=self.primary_color, foreground="white", 
                       font=('Segoe UI', 10, 'bold'), borderwidth=0)
        style.map('TButton', 
                 background=[('active', self.secondary_color), ('disabled', '#cccccc')],
                 foreground=[('disabled', '#999999')])
        
    def create_widgets(self):
        # Main container
        main_frame = ttk.Frame(self.root, padding=(20, 15))
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_font = Font(family='Segoe UI', size=16, weight='bold')
        ttk.Label(main_frame, text="Password Generator", font=title_font, 
                 foreground=self.primary_color).pack(pady=(0, 15))
        
        # Length input
        length_frame = ttk.Frame(main_frame)
        length_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(length_frame, text="Password Length:").pack(side=tk.LEFT, padx=(0, 10))
        
        self.length_entry = ttk.Entry(length_frame, width=5, justify='center')
        self.length_entry.pack(side=tk.LEFT)
        self.length_entry.insert(0, "12")
        
        # Character options
        options_frame = ttk.Frame(main_frame)
        options_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(options_frame, text="Include:", font=('Segoe UI', 10)).pack(anchor=tk.W)
        
        self.upper_var = tk.BooleanVar(value=True)
        self.lower_var = tk.BooleanVar(value=True)
        self.digits_var = tk.BooleanVar(value=True)
        self.symbols_var = tk.BooleanVar(value=False)
        
        self.create_option_checkbox(options_frame, "Uppercase letters (A-Z)", self.upper_var)
        self.create_option_checkbox(options_frame, "Lowercase letters (a-z)", self.lower_var)
        self.create_option_checkbox(options_frame, "Numbers (0-9)", self.digits_var)
        self.create_option_checkbox(options_frame, "Symbols (!@#$)", self.symbols_var)
        
        # Generate button
        generate_btn = ttk.Button(main_frame, text="Generate Password", 
                                command=self.generate_password)
        generate_btn.pack(pady=15, ipady=8, ipadx=20)
        
        # Password display
        password_frame = ttk.Frame(main_frame)
        password_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(password_frame, text="Generated Password:").pack(anchor=tk.W)
        
        self.password_var = tk.StringVar()
        password_entry = ttk.Entry(password_frame, textvariable=self.password_var, 
                                 state="readonly", font=('Consolas', 12), 
                                 foreground=self.primary_color)
        password_entry.pack(fill=tk.X, ipady=8)
        
        # Copy button
        self.copy_btn = ttk.Button(main_frame, text="Copy to Clipboard", 
                                 command=self.copy_to_clipboard, state=tk.DISABLED)
        self.copy_btn.pack(ipady=6, ipadx=15)
        
        # Strength indicator
        strength_frame = ttk.Frame(main_frame)
        strength_frame.pack(fill=tk.X, pady=(15, 0))
        
        self.strength_label = ttk.Label(strength_frame, text="Strength: -", 
                                      foreground=self.light_text)
        self.strength_label.pack(side=tk.LEFT)
        
        self.strength_meter = ttk.Progressbar(strength_frame, length=150, mode='determinate')
        self.strength_meter.pack(side=tk.RIGHT)
        
    def create_option_checkbox(self, parent, text, variable):
        cb = ttk.Checkbutton(parent, text=text, variable=variable)
        cb.pack(anchor=tk.W, pady=2)
        return cb
    
    def generate_password(self):
        try:
            length = int(self.length_entry.get())
            if length<0:
                messagebox.showerror("Error", "Password must be positive integer")
                return 
            if length < 8:
                messagebox.showerror("Error", "Password must be at least 8 characters")
                return
            if length > 50:
                messagebox.showerror("Error", "Password too long (max 50 characters)")
                return
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number")
            return
        
        use_upper = self.upper_var.get()
        use_lower = self.lower_var.get()
        use_digits = self.digits_var.get()
        use_symbols = self.symbols_var.get()
        
        if not any([use_upper, use_lower, use_digits, use_symbols]):
            messagebox.showerror("Error", "Select at least one character type")
            return
        
        pool = ''
        if use_upper: pool += string.ascii_uppercase
        if use_lower: pool += string.ascii_lowercase
        if use_digits: pool += string.digits
        if use_symbols: pool += string.punctuation
        
        password = ''.join(secrets.choice(pool) for _ in range(length))
        self.password_var.set(password)
        self.copy_btn.config(state=tk.NORMAL)
        
        # Update strength meter
        self.update_strength_meter(length, use_upper, use_lower, use_digits, use_symbols)
    
    def update_strength_meter(self, length, upper, lower, digits, symbols):
        # Simple strength calculation
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
        style.configure("Color.Horizontal.TProgressbar", troughcolor=self.bg_color, # should do changes
                       background=color, bordercolor=self.bg_color)
    
    def copy_to_clipboard(self):
        password = self.password_var.get()
        if password:
            self.root.clipboard_clear()
            self.root.clipboard_append(password)
            
            # Visual feedback
            original_text = self.copy_btn['text']
            self.copy_btn.config(text="Copied!")
            self.root.after(1500, lambda: self.copy_btn.config(text=original_text))
        else:
            messagebox.showwarning("Warning", "No password generated yet")

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.eval('tk::PlaceWindow . center')  # Center window
    root.mainloop()
