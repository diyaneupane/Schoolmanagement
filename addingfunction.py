import tkinter as tk
from tkinter import messagebox, ttk
import json
import os
from datetime import datetime

# Hardcoded login credentials
USERNAME = "admin"
PASSWORD = "password123"

# File to store data
DATA_FILE = "data.json"

# Load data from file
if os.path.exists(DATA_FILE):
    try:
        with open(DATA_FILE, "r") as file:
            data = json.load(file)
            if "students" not in data:
                data["students"] = []
            if "teachers" not in data:
                data["teachers"] = []
            if "attendance" not in data:
                data["attendance"] = {}
            if "fees" not in data:
                data["fees"] = {}
    except (json.JSONDecodeError, FileNotFoundError):
        data = {"students": [], "teachers": [], "attendance": {}, "fees": {}}
else:
    data = {"students": [], "teachers": [], "attendance": {}, "fees": {}}

    # Function to save data to file
def save_data():
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

# Function to View Data
def view_data_page():
    data_window = tk.Toplevel(dashboard)
    data_window.title("Students and Teachers Data")
    data_window.geometry("800x600")

    # Students Table
    student_frame = tk.Frame(data_window)
    student_frame.pack(pady=5, fill='both', expand=True)
    tk.Label(student_frame, text="Students List", font=("Arial", 14)).pack()

    student_tree = ttk.Treeview(student_frame, columns=("Class", "Name"), show="headings", height=10)
    student_tree.heading("Class", text="Class")
    student_tree.heading("Name", text="Name")
    student_tree.column("Class", width=200, anchor="center")
    student_tree.column("Name", width=200, anchor="center")

    student_scroll = ttk.Scrollbar(student_frame, orient="vertical", command=student_tree.yview)
    student_tree.configure(yscrollcommand=student_scroll.set)
    student_tree.pack(side='left', fill='both', expand=True)
    student_scroll.pack(side='right', fill='y')

    for student in data["students"]:
        student_tree.insert("", tk.END, values=(student["class"], student["name"]))

    tk.Button(student_frame, text="Delete Selected Student", command=lambda: delete_student(student_tree)).pack(pady=5)

# Teachers Table
    teacher_frame = tk.Frame(data_window)
    teacher_frame.pack(pady=5, fill='both', expand=True)
    tk.Label(teacher_frame, text="Teachers List", font=("Arial", 14)).pack()

    teacher_tree = ttk.Treeview(teacher_frame, columns=("Subject", "Name"), show="headings", height=10)
    teacher_tree.heading("Subject", text="Subject")
    teacher_tree.heading("Name", text="Name")
    teacher_tree.column("Subject", width=200, anchor="center")
    teacher_tree.column("Name", width=200, anchor="center")

    teacher_scroll = ttk.Scrollbar(teacher_frame, orient="vertical", command=teacher_tree.yview)
    teacher_tree.configure(yscrollcommand=teacher_scroll.set)
    teacher_tree.pack(side='left', fill='both', expand=True)
    teacher_scroll.pack(side='right', fill='y')

    for teacher in data["teachers"]:
        teacher_tree.insert("", tk.END, values=(teacher["subject"], teacher["name"]))

    tk.Button(teacher_frame, text="Delete Selected Teacher", command=lambda: delete_teacher(teacher_tree)).pack(pady=5)
   
# Dashboard Function
def open_dashboard():
    global dashboard
    dashboard = tk.Tk()
    dashboard.title("School Management System")
    dashboard.geometry("800x600")
    dashboard.configure(bg="#f4f4f4")

    frame_header = tk.Frame(dashboard, bg="#4CAF50", pady=10)
    frame_header.pack(fill="x")
    tk.Label(frame_header, text="School Management System", font=("Arial", 16, "bold"), bg="#4CAF50", fg="white").pack(side="left", padx=10)
    tk.Button(frame_header, text="Logout", command=logout, bg="red", fg="white").pack(side="right", padx=10)

    frame_students = tk.LabelFrame(dashboard, text="Add Student", padx=10, pady=10)
    frame_students.pack(padx=10, pady=10, fill="x")
    tk.Label(frame_students, text="Name:").grid(row=0, column=0)
    student_name_entry = tk.Entry(frame_students)
    student_name_entry.grid(row=0, column=1)
    tk.Label(frame_students, text="Class:").grid(row=1, column=0)
    student_class_entry = tk.Entry(frame_students)
    student_class_entry.grid(row=1, column=1)
    tk.Button(frame_students, text="Add Student", command=lambda: add_student(student_name_entry, student_class_entry)).grid(row=2, columnspan=2, pady=5)

    frame_teachers = tk.LabelFrame(dashboard, text="Add Teacher", padx=10, pady=10)
    frame_teachers.pack(padx=10, pady=10, fill="x")
    tk.Label(frame_teachers, text="Name:").grid(row=0, column=0)
    teacher_name_entry = tk.Entry(frame_teachers)
    teacher_name_entry.grid(row=0, column=1)
    tk.Label(frame_teachers, text="Subject:").grid(row=1, column=0)
    teacher_subject_entry = tk.Entry(frame_teachers)
    teacher_subject_entry.grid(row=1, column=1)
    tk.Button(frame_teachers, text="Add Teacher", command=lambda: add_teacher(teacher_name_entry, teacher_subject_entry)).grid(row=2, columnspan=2, pady=5)

    tk.Button(dashboard, text="View Data", command=view_data_page).pack(pady=20)

    dashboard.mainloop()

# Delete Student
def delete_student(tree):
    selected_item = tree.selection()
    if selected_item:
        values = tree.item(selected_item, "values")
        data["students"] = [s for s in data["students"] if not (s["class"] == values[0] and s["name"] == values[1])]
        save_data()
        tree.delete(selected_item)
        messagebox.showinfo("Success", "Student Deleted Successfully!")
    else:
        messagebox.showwarning("Select Error", "Please select a student to delete.")

# Delete Teacher
def delete_teacher(tree):
    selected_item = tree.selection()
    if selected_item:
        values = tree.item(selected_item, "values")
        data["teachers"] = [t for t in data["teachers"] if not (t["subject"] == values[0] and t["name"] == values[1])]
        save_data()
        tree.delete(selected_item)
        messagebox.showinfo("Success", "Teacher Deleted Successfully!")
    else:
        messagebox.showwarning("Select Error", "Please select a teacher to delete.")
# Add Student
def add_student(name_entry, class_entry):
    name = name_entry.get().strip()
    class_ = class_entry.get().strip()
    if name and class_:
        data["students"].append({"name": name, "class": class_})
        save_data()
        messagebox.showinfo("Success", "Student Added Successfully!")
        name_entry.delete(0, tk.END)
        class_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Input Error", "Please fill in both Name and Class fields.")

# Add Teacher
def add_teacher(name_entry, subject_entry):
    name = name_entry.get().strip()
    subject = subject_entry.get().strip()
    if name and subject:
        data["teachers"].append({"name": name, "subject": subject})
        save_data()
        messagebox.showinfo("Success", "Teacher Added Successfully!")
        name_entry.delete(0, tk.END)
        subject_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Input Error", "Please fill in both Name and Subject fields.")

# Logout Function
def logout():
    dashboard.destroy()
    start_login()

# Start login window
def start_login():
    global login_window, entry_id, entry_password
    login_window = tk.Tk()
    login_window.title("Login - School Management System")
    login_window.geometry("400x300")
