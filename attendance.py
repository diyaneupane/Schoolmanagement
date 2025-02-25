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
    
    frame_students = tk.LabelFrame(dashboard, text="Add Student", padx=10, pady=10)
    frame_students.pack(padx=10, pady=10, fill="x")
    tk.Label(frame_students, text="Name:").grid(row=0, column=0)
    student_name_entry = tk.Entry(frame_students)
    student_name_entry.grid(row=0, column=1)
    tk.Label(frame_students, text="Class:").grid(row=1, column=0)
    student_class_entry = tk.Entry(frame_students)
    student_class_entry.grid(row=1, column=1)
   
    dashboard.mainloop()


# Function to Mark Attendance
def mark_attendance_page():
    attendance_window = tk.Toplevel(dashboard)
    attendance_window.title("Mark Attendance")
    attendance_window.geometry("400x300")

    tk.Label(attendance_window, text="Select Class:").pack()
    class_var = tk.StringVar()
    class_dropdown = ttk.Combobox(attendance_window, textvariable=class_var)
    class_dropdown['values'] = list(set(student["class"] for student in data["students"]))
    class_dropdown.pack()

    tk.Label(attendance_window, text="Date:").pack()
    date_entry = tk.Entry(attendance_window)
    date_entry.insert(0, datetime.today().strftime('%Y-%m-%d'))  # Default to today's date
    date_entry.pack()

    tk.Button(attendance_window, text="Mark Attendance", command=lambda: show_students_for_attendance(class_var.get(), date_entry.get(), attendance_window)).pack(pady=10)

def show_students_for_attendance(selected_class, date, window):
    if not selected_class or not date:
        messagebox.showwarning("Input Error", "Please select a class and enter a date.")
        return

    students_in_class = [student for student in data["students"] if student["class"] == selected_class]
    if not students_in_class:
        messagebox.showinfo("No Students", "No students found in the selected class.")
        return

    attendance_frame = tk.Frame(window)
    attendance_frame.pack(pady=10)

    attendance_status = {}
    for student in students_in_class:
        var = tk.StringVar(value="Present")
        tk.Label(attendance_frame, text=student["name"]).pack()
        tk.Radiobutton(attendance_frame, text="Present", variable=var, value="Present").pack()
        tk.Radiobutton(attendance_frame, text="Absent", variable=var, value="Absent").pack()
        attendance_status[student["name"]] = var

    tk.Button(attendance_frame, text="Submit Attendance", command=lambda: save_attendance(selected_class, date, attendance_status, window)).pack(pady=10)

def save_attendance(selected_class, date, attendance_status, window):
    if selected_class not in data["attendance"]:
        data["attendance"][selected_class] = {}
    data["attendance"][selected_class][date] = {name: var.get() for name, var in attendance_status.items()}
    save_data()
    messagebox.showinfo("Success", "Attendance marked successfully!")
    window.destroy()

# Function to View Attendance Records
def view_attendance_records():
    attendance_window = tk.Toplevel(dashboard)
    attendance_window.title("View Attendance Records")
    attendance_window.geometry("600x400")

    tk.Label(attendance_window, text="Select Class:").pack()
    class_var = tk.StringVar()
    class_dropdown = ttk.Combobox(attendance_window, textvariable=class_var)
    class_dropdown['values'] = list(set(student["class"] for student in data["students"]))
    class_dropdown.pack()

    tk.Label(attendance_window, text="Select Date:").pack()
    date_var = tk.StringVar()
    date_dropdown = ttk.Combobox(attendance_window, textvariable=date_var)
    date_dropdown.pack()

    def update_dates():
        selected_class = class_var.get()
        if selected_class in data["attendance"]:
            date_dropdown['values'] = list(data["attendance"][selected_class].keys())
        else:
            date_dropdown['values'] = []

    class_dropdown.bind("<<ComboboxSelected>>", lambda e: update_dates())

    tk.Button(attendance_window, text="View Attendance", command=lambda: show_attendance_records(class_var.get(), date_var.get(), attendance_window)).pack(pady=10)

def show_attendance_records(selected_class, date, window):
    if not selected_class or not date:
        messagebox.showwarning("Input Error", "Please select a class and date.")
        return

    if selected_class not in data["attendance"] or date not in data["attendance"][selected_class]:
        messagebox.showinfo("No Records", "No attendance records found for the selected class and date.")
        return

    records = data["attendance"][selected_class][date]
    records_window = tk.Toplevel(window)
    records_window.title(f"Attendance Records for {selected_class} on {date}")
    records_window.geometry("400x300")

    for name, status in records.items():
        tk.Label(records_window, text=f"{name}: {status}").pack()