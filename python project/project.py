
import string
import random
import tkinter as tk
from tkinter import ttk, messagebox

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

    password += [random.choice(chars) for _ in range(length - len(password))]
    random.shuffle(password)
    return ''.join(password)

def on_generate():
    user_name = name_var.get().strip()
    if not user_name:
        messagebox.showerror("Input Error", "Please enter your name.")
        return
    try:
        length = int(length_var.get())
    except ValueError:
        messagebox.showerror("Invalid Input", "Enter a valid number for password length.")
        return
    if length < 4:
        messagebox.showerror("Invalid Input", "Password length must be at least 4.")
        return
    pwd = generate_password(
        length,
        lower_var.get(),
        upper_var.get(),
        digits_var.get(),
        specials_var.get()
    )
    if not pwd:
        messagebox.showerror("Selection Error", "Select at least one character type.")
        return
    result_var.set(f"{user_name}, your password: {pwd}")
    messagebox.showinfo("Thank You", "Thank you! Your password has been generated.")

# --- GUI Setup ---
root = tk.Tk()
root.title("Random Password Generator")
root.geometry("430x400")
root.resizable(False, False)
root.configure(bg="#ffe4ec")  # Soft pink background

style = ttk.Style()
style.theme_use('clam')
style.configure("TLabel", font=("Segoe UI", 12), background="#ffe4ec")
style.configure("TButton", font=("Segoe UI", 11, "bold"), background="#ff69b4", foreground="#fff")
style.map("TButton", background=[("active", "#ff1493")])

header = tk.Label(root, text="Random Password Generator", font=("Segoe UI", 18, "bold"), bg="#ffe4ec", fg="#d72660")
header.pack(pady=18)

frame = tk.Frame(root, bg="#ffe4ec")
frame.pack(pady=5)

# --- User Name Entry ---
tk.Label(frame, text="Your Name:", bg="#ffe4ec", fg="#3a86ff", font=("Segoe UI", 12, "bold")).grid(row=0, column=0, sticky="w", pady=6)
name_var = tk.StringVar()
name_entry = ttk.Entry(frame, textvariable=name_var, width=18, font=("Segoe UI", 12))
name_entry.grid(row=0, column=1, padx=10, pady=6)

tk.Label(frame, text="Password Length:", bg="#ffe4ec", fg="#3a86ff", font=("Segoe UI", 12, "bold")).grid(row=1, column=0, sticky="w", pady=6)
length_var = tk.StringVar(value="12")
length_entry = ttk.Entry(frame, textvariable=length_var, width=8, font=("Segoe UI", 12))
length_entry.grid(row=1, column=1, padx=10, pady=6)

lower_var = tk.BooleanVar(value=True)
upper_var = tk.BooleanVar(value=True)
digits_var = tk.BooleanVar(value=True)
specials_var = tk.BooleanVar(value=False)

tk.Checkbutton(frame, text="Lowercase (a-z)", variable=lower_var, bg="#ffe4ec", fg="#ff8800", font=("Segoe UI", 11, "bold")).grid(row=2, column=0, sticky="w")
tk.Checkbutton(frame, text="Uppercase (A-Z)", variable=upper_var, bg="#ffe4ec", fg="#118ab2", font=("Segoe UI", 11, "bold")).grid(row=3, column=0, sticky="w")
tk.Checkbutton(frame, text="Digits (0-9)", variable=digits_var, bg="#ffe4ec", fg="#06d6a0", font=("Segoe UI", 11, "bold")).grid(row=2, column=1, sticky="w")
tk.Checkbutton(frame, text="Special (!@#...)", variable=specials_var, bg="#ffe4ec", fg="#ef476f", font=("Segoe UI", 11, "bold")).grid(row=3, column=1, sticky="w")

ttk.Button(root, text="Generate Password", command=on_generate).pack(pady=18)

result_var = tk.StringVar()
result_label = tk.Label(
    root,
    textvariable=result_var,
    font=("Segoe UI", 16, "bold"),
    bg="#fffbe7",
    fg="#d72660",
    relief="groove",
    bd=2,
    width=32,
    anchor="center",
    pady=10
)
result_label.pack(pady=12)

footer = tk.Label(root, text="© 2025 Password Generator", font=("Segoe UI", 10), bg="#ffe4ec", fg="#6c757d")
footer.pack(side="bottom", pady=8)

root.mainloop()
