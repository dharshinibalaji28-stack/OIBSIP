import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os
from datetime import datetime
import matplotlib.pyplot as plt

root = tk.Tk()
root.title("BMI Calculator Pro")
root.geometry("650x700")
root.configure(bg="#f5f7fa")

title = tk.Label(
    root,
    text="BMI Calculator Pro",
    font=("Arial",24,"bold"),
    bg="#f5f7fa",
    fg="#2c3e50"
)
title.pack(pady=20)

frame = tk.Frame(root,bg="#ffffff",bd=2,relief="groove")
frame.pack(padx=20,pady=10,fill="both")

tk.Label(
    frame,
    text="Name",
    font=("Arial",12,"bold"),
    bg="white"
).pack(pady=(20,5))

name_entry=tk.Entry(frame,font=("Arial",12),width=30)
name_entry.pack()

tk.Label(
    frame,
    text="Weight (kg)",
    font=("Arial",12,"bold"),
    bg="white"
).pack(pady=(15,5))

weight_entry=tk.Entry(frame,font=("Arial",12),width=30)
weight_entry.pack()

tk.Label(
    frame,
    text="Height (m)",
    font=("Arial",12,"bold"),
    bg="white"
).pack(pady=(15,5))

height_entry=tk.Entry(frame,font=("Arial",12),width=30)
height_entry.pack()

result_label=tk.Label(
    frame,
    text="",
    font=("Arial",13,"bold"),
    bg="white"
)
result_label.pack(pady=20)

filename="history.csv"
def calculate_bmi():
    try:
        name = name_entry.get().strip()

        if name == "":
            messagebox.showerror("Error", "Please enter your name")
            return

        weight = float(weight_entry.get())
        height = float(height_entry.get())

        if weight <= 0 or height <= 0:
            messagebox.showerror("Error", "Weight and Height must be greater than 0")
            return

        bmi = weight / (height * height)

        if bmi < 18.5:
            category = "Underweight"
            color = "blue"
        elif bmi < 25:
            category = "Normal"
            color = "green"
        elif bmi < 30:
            category = "Overweight"
            color = "orange"
        else:
            category = "Obese"
            color = "red"

        result_label.config(
            text=f"Name : {name}\n\nBMI : {round(bmi,2)}\n\nCategory : {category}",
            fg=color
        )

        file_exists = os.path.isfile(filename)

        with open(filename, "a", newline="") as file:
            writer = csv.writer(file)

            if not file_exists:
                writer.writerow([
                    "Date",
                    "Name",
                    "Weight",
                    "Height",
                    "BMI",
                    "Category"
                ])

            writer.writerow([
                datetime.now().strftime("%d-%m-%Y %H:%M"),
                name,
                weight,
                height,
                round(bmi,2),
                category
            ])

    except ValueError:
        messagebox.showerror(
            "Error",
            "Please enter valid numeric values."
        )
def show_history():
    if not os.path.exists(filename):
        messagebox.showinfo("History", "No history found.")
        return

    history_window = tk.Toplevel(root)
    history_window.title("BMI History")
    history_window.geometry("700x400")

    tree = ttk.Treeview(
        history_window,
        columns=("Date", "Name", "Weight", "Height", "BMI", "Category"),
        show="headings"
    )

    tree.heading("Date", text="Date")
    tree.heading("Name", text="Name")
    tree.heading("Weight", text="Weight")
    tree.heading("Height", text="Height")
    tree.heading("BMI", text="BMI")
    tree.heading("Category", text="Category")

    tree.column("Date", width=140)
    tree.column("Name", width=100)
    tree.column("Weight", width=80)
    tree.column("Height", width=80)
    tree.column("BMI", width=80)
    tree.column("Category", width=120)

    tree.pack(fill="both", expand=True)

    with open(filename, "r") as file:
        reader = csv.reader(file)
        next(reader)

        for row in reader:
            tree.insert("", tk.END, values=row)
def show_graph():

    if not os.path.exists(filename):
        messagebox.showinfo("Graph", "No data available.")
        return

    names = []
    bmi_values = []

    with open(filename, "r") as file:
        reader = csv.DictReader(file)

        for row in reader:
            names.append(row["Name"])
            bmi_values.append(float(row["BMI"]))

    plt.figure(figsize=(8,5))
    plt.bar(names, bmi_values)
    plt.title("BMI History")
    plt.xlabel("Users")
    plt.ylabel("BMI")
    plt.grid(axis="y")
    plt.show()


def show_pie_chart():

    if not os.path.exists(filename):
        messagebox.showinfo("Chart", "No data available.")
        return

    categories = {
        "Underweight":0,
        "Normal":0,
        "Overweight":0,
        "Obese":0
    }

    with open(filename, "r") as file:
        reader = csv.DictReader(file)

        for row in reader:
            categories[row["Category"]] += 1

    plt.figure(figsize=(6,6))
    plt.pie(
        categories.values(),
        labels=categories.keys(),
        autopct="%1.1f%%",
        startangle=90
    )

    plt.title("BMI Category Distribution")
    plt.show()
button_frame = tk.Frame(root, bg="#f5f7fa")
button_frame.pack(pady=20)

calculate_button = tk.Button(
    button_frame,
    text="Calculate BMI",
    command=calculate_bmi,
    font=("Arial",12,"bold"),
    bg="#4CAF50",
    fg="white",
    width=18
)
calculate_button.grid(row=0, column=0, padx=10, pady=10)

history_button = tk.Button(
    button_frame,
    text="View History",
    command=show_history,
    font=("Arial",12,"bold"),
    bg="#2196F3",
    fg="white",
    width=18
)
history_button.grid(row=0, column=1, padx=10, pady=10)

graph_button = tk.Button(
    button_frame,
    text="Bar Graph",
    command=show_graph,
    font=("Arial",12,"bold"),
    bg="#FF9800",
    fg="white",
    width=18
)
graph_button.grid(row=1, column=0, padx=10, pady=10)

pie_button = tk.Button(
    button_frame,
    text="Pie Chart",
    command=show_pie_chart,
    font=("Arial",12,"bold"),
    bg="#9C27B0",
    fg="white",
    width=18
)
pie_button.grid(row=1, column=1, padx=10, pady=10)

footer = tk.Label(
    root,
    text="Developed using Python, Tkinter, CSV and Matplotlib",
    font=("Arial",10),
    bg="#f5f7fa",
    fg="gray"
)
footer.pack(pady=15)

root.mainloop()
