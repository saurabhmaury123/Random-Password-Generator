import tkinter as tk
from tkinter import messagebox
import secrets
import string
import pyperclip

history = []

# Character Sets
UPPER = string.ascii_uppercase
LOWER = string.ascii_lowercase
DIGITS = string.digits
SYMBOLS = string.punctuation

AMBIGUOUS = "0O1lI"


def generate_password():
    length = length_var.get()

    if length < 8:
        messagebox.showerror("Error", "Password length must be at least 8.")
        return

    selected_sets = []

    if upper_var.get():
        selected_sets.append(UPPER)

    if lower_var.get():
        selected_sets.append(LOWER)

    if number_var.get():
        selected_sets.append(DIGITS)

    if symbol_var.get():
        selected_sets.append(SYMBOLS)

    if len(selected_sets) < 2:
        messagebox.showerror(
            "Error",
            "Select at least two character types."
        )
        return

    if exclude_var.get():
        selected_sets = [
            ''.join(c for c in s if c not in AMBIGUOUS)
            for s in selected_sets
        ]

    password = []

    # Ensure one character from each selected category
    for s in selected_sets:
        password.append(secrets.choice(s))

    all_chars = ''.join(selected_sets)

    while len(password) < length:
        password.append(secrets.choice(all_chars))

    secrets.SystemRandom().shuffle(password)

    password = ''.join(password)

    password_entry.delete(0, tk.END)
    password_entry.insert(0, password)

    pyperclip.copy(password)

    update_strength(password)

    history.insert(0, password)

    if len(history) > 5:
        history.pop()

    history_box.delete(0, tk.END)

    for item in history:
        history_box.insert(tk.END, item)


def update_strength(password):

    score = 0

    if len(password) >= 8:
        score += 1

    if len(password) >= 12:
        score += 1

    if any(c.isupper() for c in password):
        score += 1

    if any(c.islower() for c in password):
        score += 1

    if any(c.isdigit() for c in password):
        score += 1

    if any(c in SYMBOLS for c in password):
        score += 1

    if score <= 2:
        strength_label.config(text="Strength: Weak", fg="red")
    elif score <= 4:
        strength_label.config(text="Strength: Medium", fg="orange")
    else:
        strength_label.config(text="Strength: Strong", fg="green")


root = tk.Tk()
root.title("Random Password Generator")
root.geometry("500x600")
root.resizable(False, False)

tk.Label(root,
         text="Password Length",
         font=("Arial", 12, "bold")).pack(pady=5)

length_var = tk.IntVar(value=12)

tk.Spinbox(root,
           from_=8,
           to=64,
           textvariable=length_var,
           width=10).pack()

upper_var = tk.BooleanVar(value=True)
lower_var = tk.BooleanVar(value=True)
number_var = tk.BooleanVar(value=True)
symbol_var = tk.BooleanVar(value=True)
exclude_var = tk.BooleanVar()

tk.Checkbutton(root,
               text="Uppercase Letters",
               variable=upper_var).pack(anchor="w", padx=40)

tk.Checkbutton(root,
               text="Lowercase Letters",
               variable=lower_var).pack(anchor="w", padx=40)

tk.Checkbutton(root,
               text="Numbers",
               variable=number_var).pack(anchor="w", padx=40)

tk.Checkbutton(root,
               text="Symbols",
               variable=symbol_var).pack(anchor="w", padx=40)

tk.Checkbutton(root,
               text="Exclude Ambiguous Characters (0,O,1,l,I)",
               variable=exclude_var).pack(anchor="w", padx=40)

tk.Button(root,
          text="Generate Password",
          command=generate_password,
          bg="green",
          fg="white",
          font=("Arial", 11, "bold")).pack(pady=15)

password_entry = tk.Entry(root,
                          width=40,
                          font=("Consolas", 14),
                          justify="center")

password_entry.pack()

strength_label = tk.Label(root,
                          text="Strength:",
                          font=("Arial", 12, "bold"))

strength_label.pack(pady=10)

tk.Label(root,
         text="Last 5 Passwords",
         font=("Arial", 12, "bold")).pack()

history_box = tk.Listbox(root,
                         width=45,
                         height=5)

history_box.pack(pady=10)

tk.Label(root,
         text="Password is copied automatically to clipboard.",
         fg="blue").pack(pady=5)

root.mainloop()