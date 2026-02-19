import re
import tkinter as tk
from tkinter import ttk, messagebox
import random
import string

# ---------------------------
# Common weak passwords
# ---------------------------
common_passwords = ["password", "12345", "123456", "qwerty", "abc123"]

# ---------------------------
# Password Analysis
# ---------------------------
def analyze_password(password):
    checklist = []

    length_ok = len(password) >= 8
    upper_ok = bool(re.search(r"[A-Z]", password))
    lower_ok = bool(re.search(r"[a-z]", password))
    digit_ok = bool(re.search(r"\d", password))
    special_ok = bool(re.search(r"[!@#$%^&*(),.?\":{}|<>]", password))
    common_ok = password.lower() not in common_passwords
    repeat_ok = not re.search(r"(.)\1\1", password)

    checklist.append(("At least 8 characters", length_ok))
    checklist.append(("Contains uppercase letter", upper_ok))
    checklist.append(("Contains lowercase letter", lower_ok))
    checklist.append(("Contains number", digit_ok))
    checklist.append(("Contains special character", special_ok))
    checklist.append(("Not a common password", common_ok))
    checklist.append(("No repeated characters (aaa)", repeat_ok))

    score = sum(item[1] for item in checklist)

    if score <= 3:
        strength = "Weak"
        color = "#e74c3c"
    elif score <= 5:
        strength = "Moderate"
        color = "#f39c12"
    else:
        strength = "Strong"
        color = "#27ae60"

    return strength, color, checklist, score

# ---------------------------
# Password Generator
# ---------------------------
def generate_password():
    length = length_var.get()
    char_pool = ""

    if upper_var.get():
        char_pool += string.ascii_uppercase
    if lower_var.get():
        char_pool += string.ascii_lowercase
    if digit_var.get():
        char_pool += string.digits
    if special_var.get():
        char_pool += "!@#$%^&*(),.?\":{}|<>"

    if not char_pool:
        result_label.config(text="Select at least one option!", fg="#e74c3c")
        return

    password = "".join(random.choice(char_pool) for _ in range(length))

    entry.delete(0, tk.END)

    generated_entry.config(state="normal")
    generated_entry.delete(0, tk.END)
    generated_entry.insert(0, password)
    generated_entry.config(state="readonly")

    strength, color, checklist, score = analyze_password(password)

    result_label.config(text=f"Strength: {strength}", fg=color)
    progress["value"] = (score / 7) * 100
    style.configure("TProgressbar", background=color)

    checklist_box.delete("1.0", tk.END)
    for text, status in checklist:
        mark = "✔" if status else "✖"
        checklist_box.insert(tk.END, f"{mark} {text}\n")

# ---------------------------
# GUI Logic
# ---------------------------
def reset_ui():
    result_label.config(text="Strength: ", fg="#2c3e50")
    progress["value"] = 0
    style.configure("TProgressbar", background="#3498db")
    checklist_box.delete("1.0", tk.END)

def on_key_release(event):
    password = entry.get()

    if password.strip() == "":
        reset_ui()
        return

    strength, color, checklist, score = analyze_password(password)

    result_label.config(text=f"Strength: {strength}", fg=color)
    progress["value"] = (score / 7) * 100
    style.configure("TProgressbar", background=color)

    checklist_box.delete("1.0", tk.END)
    for text, status in checklist:
        mark = "✔" if status else "✖"
        checklist_box.insert(tk.END, f"{mark} {text}\n")

def toggle_password():
    if show_var.get():
        entry.config(show="")
    else:
        entry.config(show="*")

def copy_to_clipboard():
    password = generated_entry.get()
    if password:
        root.clipboard_clear()
        root.clipboard_append(password)
        root.update()
        messagebox.showinfo("Success", "Password copied to clipboard!")

# ---------------------------
# GUI Setup
# ---------------------------

root = tk.Tk()
root.title("Password Strength Analyzer")
root.geometry("700x700")
root.resizable(False, False)

# Light Blue Background
root.configure(bg="#d6ecff")

style = ttk.Style()
style.theme_use("clam")
style.configure("TProgressbar", thickness=18,
                troughcolor="#b3daff", background="#3498db")

# Title
title = tk.Label(root, text="Password Strength Analyzer", font=("Segoe UI Semibold", 15),
                 bg="#d6ecff", fg="#1f4e79")
title.pack(pady=10)

# Password Entry
entry = tk.Entry(root, width=30, font=("Segoe UI", 14), show="*",
                 bg="white", fg="#2c3e50",
                 relief="flat")
entry.pack(pady=10)
entry.bind("<KeyRelease>", on_key_release)

# Show/Hide Toggle
show_var = tk.BooleanVar()
eye_button = tk.Checkbutton(root, text="Show Password", font=("Segoe UI", 10), variable=show_var, command=toggle_password,
                            bg="#d6ecff", fg="#2c3e50")
eye_button.pack()

# Strength Label
result_label = tk.Label(root, text="Strength: ", font=("Segoe UI Semibold", 12),
                        bg="#d6ecff", fg="#2c3e50")
result_label.pack(pady=5)

# Progress Bar
progress = ttk.Progressbar(root, length=400, mode="determinate", maximum=100)
progress.pack(pady=5)

# Checklist Text Box
checklist_box = tk.Text(root, height=7, width=60, font=("Segoe UI", 11),
                        bg="white", fg="#2c3e50",
                        relief="flat")
checklist_box.pack(pady=5)

# ---------------------------
# Generator Section
# ---------------------------

gen_label = tk.Label(root, text="Secure Password Generator", font=("Segoe UI Semibold", 15),
                     bg="#d6ecff", fg="#1f4e79")
gen_label.pack(pady=10)

length_var = tk.IntVar(value=12)

length_frame = tk.Frame(root, bg="#d6ecff")
length_frame.pack()

tk.Label(length_frame, text="Length:",  font=("Segoe UI", 11),
         bg="#d6ecff", fg="#2c3e50").pack(side=tk.LEFT)

tk.Spinbox(length_frame, from_=6, to=32, font=("Segoe UI", 11),
           textvariable=length_var, width=5,
           bg="white", fg="#2c3e50").pack(side=tk.LEFT)

upper_var = tk.BooleanVar(value=True)
lower_var = tk.BooleanVar(value=True)
digit_var = tk.BooleanVar(value=True)
special_var = tk.BooleanVar(value=True)

options_frame = tk.Frame(root, bg="#d6ecff")
options_frame.pack(pady=5)

tk.Checkbutton(options_frame, text="Uppercase", variable=upper_var,
               bg="#d6ecff", fg="#2c3e50",
               font=("Segoe UI", 10)).grid(row=0, column=0, sticky="w")

tk.Checkbutton(options_frame, text="Lowercase", variable=lower_var,
               bg="#d6ecff", fg="#2c3e50",
               font=("Segoe UI", 10)).grid(row=0, column=1, sticky="w")

tk.Checkbutton(options_frame, text="Digits", variable=digit_var,
               bg="#d6ecff", fg="#2c3e50",
               font=("Segoe UI", 10)).grid(row=1, column=0, sticky="w")

tk.Checkbutton(options_frame, text="Special", variable=special_var,
               bg="#d6ecff", fg="#2c3e50",
               font=("Segoe UI", 10)).grid(row=1, column=1, sticky="w")

generate_btn = tk.Button(root, text="Generate Password", font=("Segoe UI Semibold", 11),
                         command=generate_password,
                         bg="#3498db", fg="white",
                         relief="flat", padx=10, pady=3)
generate_btn.pack(pady=5)

# ---------------------------
# Generated Password Display
# ---------------------------

generated_label = tk.Label(root, text="Generated Password", font=("Segoe UI Semibold", 13),
                           bg="#d6ecff", fg="#1f4e79")
generated_label.pack(pady=5)

generated_entry = tk.Entry(root, width=30, font=("Segoe UI", 14),                           
                           bg="white", fg="#1f4e79",
                           readonlybackground="white", state="readonly",
                           relief="flat")
generated_entry.pack(pady=5)

copy_btn = tk.Button(root, text="Copy Password", font=("Segoe UI Semibold", 11),
                     command=copy_to_clipboard,
                     bg="#5dade2", fg="white",                     
                     relief="flat", padx=10, pady=5)
copy_btn.pack(pady=10)

reset_ui()
root.mainloop()
