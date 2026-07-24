import tkinter as tk
from tkinter import messagebox
import random
import string
import csv
import os
from datetime import datetime
import matplotlib.pyplot as plt

# ---------------- Main Window ----------------

root = tk.Tk()
root.title("Password Generator Pro")
root.geometry("550x700")
root.configure(bg="white")

# ---------------- Heading ----------------

heading = tk.Label(
    root,
    text="Password Generator Pro",
    font=("Arial", 24, "bold"),
    bg="white",
    fg="navy"
)
heading.pack(pady=20)

# ---------------- Password Length ----------------

length_label = tk.Label(
    root,
    text="Enter Password Length",
    font=("Arial", 14),
    bg="white"
)
length_label.pack()

length_entry = tk.Entry(
    root,
    font=("Arial", 14),
    justify="center"
)
length_entry.pack(pady=10)

# ---------------- Checkboxes ----------------

upper_var = tk.BooleanVar(value=True)
lower_var = tk.BooleanVar(value=True)
number_var = tk.BooleanVar(value=True)
symbol_var = tk.BooleanVar(value=True)

tk.Checkbutton(
    root,
    text="Uppercase Letters",
    variable=upper_var,
    bg="white",
    font=("Arial",12)
).pack()

tk.Checkbutton(
    root,
    text="Lowercase Letters",
    variable=lower_var,
    bg="white",
    font=("Arial",12)
).pack()

tk.Checkbutton(
    root,
    text="Numbers",
    variable=number_var,
    bg="white",
    font=("Arial",12)
).pack()

tk.Checkbutton(
    root,
    text="Symbols",
    variable=symbol_var,
    bg="white",
    font=("Arial",12)
).pack()

# ---------------- Result Labels ----------------

password_label = tk.Label(
    root,
    text="",
    font=("Arial",18,"bold"),
    bg="white",
    fg="blue"
)
password_label.pack(pady=15)

strength_label = tk.Label(
    root,
    text="",
    font=("Arial",14,"bold"),
    bg="white"
)
strength_label.pack()

current_password = ""
# ---------------- PASSWORD GENERATOR FUNCTION ---------------- #

def generate_password():
    characters = ""

    if upper_var.get():
        characters += string.ascii_uppercase

    if lower_var.get():
        characters += string.ascii_lowercase

    if number_var.get():
        characters += string.digits

    if symbol_var.get():
        characters += string.punctuation

    if characters == "":
        messagebox.showwarning("Warning", "Select at least one option!")
        return

    try:
        length = int(length_entry.get())
    except:
        messagebox.showerror("Error", "Enter a valid password length")
        return

    password = "".join(random.choice(characters) for _ in range(length))

    password_label.config(text=password)

    strength = check_strength(password)
    strength_label.config(text=f"Password Strength: {strength}")

    save_history(password, strength)


# ---------------- PASSWORD STRENGTH ---------------- #

def check_strength(password):
    score = 0

    if len(password) >= 8:
        score += 1

    if any(c.isupper() for c in password):
        score += 1

    if any(c.islower() for c in password):
        score += 1

    if any(c.isdigit() for c in password):
        score += 1

    if any(c in string.punctuation for c in password):
        score += 1

    if score <= 2:
        return "Weak"
    elif score <= 4:
        return "Medium"
    else:
        return "Strong"
    # ---------------- SAVE HISTORY ---------------- #

def save_history(password, strength):

    file_exists = os.path.isfile("history.csv")

    with open("history.csv", "a", newline="") as file:

        writer = csv.writer(file)

        if not file_exists:
            writer.writerow([
                "Date",
                "Password",
                "Strength"
            ])

        writer.writerow([
            datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            password,
            strength
        ])


# ---------------- COPY PASSWORD ---------------- #

def copy_password():

    password = password_label.cget("text")

    if password == "":
        messagebox.showwarning(
            "Warning",
            "Generate a password first!"
        )
        return

    root.clipboard_clear()
    root.clipboard_append(password)
    root.update()

    messagebox.showinfo(
        "Success",
        "Password copied to clipboard!"
    )


# ---------------- CLEAR ---------------- #

def clear_all():

    length_entry.delete(0, tk.END)

    upper_var.set(True)
    lower_var.set(True)
    number_var.set(True)
    symbol_var.set(True)

    password_label.config(text="")
    strength_label.config(text="")
    # ---------------- VIEW HISTORY ---------------- #

def view_history():

    if not os.path.exists("history.csv"):
        messagebox.showinfo("History", "No history found!")
        return

    history_window = tk.Toplevel(root)
    history_window.title("Password History")
    history_window.geometry("600x400")

    text = tk.Text(history_window, font=("Consolas", 10))
    text.pack(fill="both", expand=True)

    with open("history.csv", "r") as file:
        text.insert(tk.END, file.read())


# ---------------- BAR GRAPH ---------------- #

def show_bar_graph():

    if not os.path.exists("history.csv"):
        messagebox.showinfo("Graph", "No history found!")
        return

    weak = 0
    medium = 0
    strong = 0

    with open("history.csv", "r") as file:

        reader = csv.DictReader(file)

        for row in reader:

            if row["Strength"] == "Weak":
                weak += 1

            elif row["Strength"] == "Medium":
                medium += 1

            elif row["Strength"] == "Strong":
                strong += 1

    plt.figure(figsize=(5,4))
    plt.bar(
        ["Weak", "Medium", "Strong"],
        [weak, medium, strong],
        color=["red", "orange", "green"]
    )

    plt.title("Password Strength Distribution")
    plt.xlabel("Strength")
    plt.ylabel("Count")
    plt.show()


# ---------------- PIE CHART ---------------- #

def show_pie_chart():

    if not os.path.exists("history.csv"):
        messagebox.showinfo("Graph", "No history found!")
        return

    weak = 0
    medium = 0
    strong = 0

    with open("history.csv", "r") as file:

        reader = csv.DictReader(file)

        for row in reader:

            if row["Strength"] == "Weak":
                weak += 1

            elif row["Strength"] == "Medium":
                medium += 1

            elif row["Strength"] == "Strong":
                strong += 1

    plt.figure(figsize=(5,5))
    plt.pie(
        [weak, medium, strong],
        labels=["Weak", "Medium", "Strong"],
        autopct="%1.1f%%"
    )

    plt.title("Password Strength Distribution")
    plt.show()
    # ---------------- BUTTONS ---------------- #

generate_button = tk.Button(
    root,
    text="Generate Password",
    command=generate_password,
    bg="green",
    fg="white",
    font=("Arial",12,"bold"),
    width=22
)
generate_button.pack(pady=5)

copy_button = tk.Button(
    root,
    text="Copy Password",
    command=copy_password,
    bg="blue",
    fg="white",
    font=("Arial",12,"bold"),
    width=22
)
copy_button.pack(pady=5)

history_button = tk.Button(
    root,
    text="View History",
    command=view_history,
    bg="orange",
    fg="white",
    font=("Arial",12,"bold"),
    width=22
)
history_button.pack(pady=5)

bar_button = tk.Button(
    root,
    text="Show Bar Graph",
    command=show_bar_graph,
    bg="purple",
    fg="white",
    font=("Arial",12,"bold"),
    width=22
)
bar_button.pack(pady=5)

pie_button = tk.Button(
    root,
    text="Show Pie Chart",
    command=show_pie_chart,
    bg="brown",
    fg="white",
    font=("Arial",12,"bold"),
    width=22
)
pie_button.pack(pady=5)

clear_button = tk.Button(
    root,
    text="Clear",
    command=clear_all,
    bg="red",
    fg="white",
    font=("Arial",12,"bold"),
    width=22
)
clear_button.pack(pady=5)

# ---------------- FOOTER ---------------- #

footer = tk.Label(
    root,
    text="Developed by B. Dharshini\nOASIS INFOBYTE - Python Programming",
    font=("Arial",10),
    bg="white",
    fg="gray"
)
footer.pack(pady=20)

# ---------------- START PROGRAM ---------------- #

root.mainloop()