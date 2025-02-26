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

# Login Function
def login():
    user_id = entry_id.get()
    password = entry_password.get()
    if user_id == USERNAME and password == PASSWORD:
        messagebox.showinfo("Login Successful", "Welcome to School Management System!")
        login_window.destroy()
        open_dashboard()
    else:
        messagebox.showerror("Login Failed", "Invalid User ID or Password!")

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
    tk.Button(dashboard, text="Mark Attendance", command=mark_attendance_page).pack(pady=20)
    tk.Button(dashboard, text="Fee Management", command=fee_management_page).pack(pady=20)
    dashboard.mainloop()

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

# Fee Management System
def fee_management_page():
    fee_window = tk.Toplevel(dashboard)
    fee_window.title("Fee Management")
    fee_window.geometry("600x400")

    tk.Label(fee_window, text="Select Student:").pack()
    student_var = tk.StringVar()
    student_dropdown = ttk.Combobox(fee_window, textvariable=student_var)
    student_dropdown['values'] = [student["name"] for student in data["students"]]
    student_dropdown.pack()

    tk.Label(fee_window, text="Fee Amount:").pack()
    fee_amount_entry = tk.Entry(fee_window)
    fee_amount_entry.pack()

    tk.Label(fee_window, text="Fee Type:").pack()
    fee_type_entry = tk.Entry(fee_window)
    fee_type_entry.pack()

    tk.Button(fee_window, text="Add Fee Record", command=lambda: add_fee_record(student_var.get(), fee_amount_entry.get(), fee_type_entry.get(), fee_window)).pack(pady=10)

    tk.Button(fee_window, text="View Fee Records", command=lambda: view_fee_records(student_var.get(), fee_window)).pack(pady=10)

def add_fee_record(student_name, fee_amount, fee_type, window):
    if not student_name or not fee_amount or not fee_type:
        messagebox.showwarning("Input Error", "Please fill in all fields.")
        return

    if student_name not in data["fees"]:
        data["fees"][student_name] = []

    data["fees"][student_name].append({
        "amount": fee_amount,
        "type": fee_type,
        "date": datetime.today().strftime('%Y-%m-%d'),
        "paid": False
    })
    save_data()
    messagebox.showinfo("Success", "Fee record added successfully!")
    window.destroy()

def view_fee_records(student_name, window):
    if not student_name:
        messagebox.showwarning("Input Error", "Please select a student.")
        return

    if student_name not in data["fees"]:
        messagebox.showinfo("No Records", "No fee records found for the selected student.")
        return

    records = data["fees"][student_name]
    records_window = tk.Toplevel(window)
    records_window.title(f"Fee Records for {student_name}")
    records_window.geometry("600x400")

    for record in records:
        status = "Paid" if record["paid"] else "Pending"
        tk.Label(records_window, text=f"Amount: {record['amount']}, Type: {record['type']}, Date: {record['date']}, Status: {status}").pack()

    tk.Button(records_window, text="Mark as Paid", command=lambda: mark_fee_paid(student_name, records_window)).pack(pady=10)

def mark_fee_paid(student_name, window):
    if student_name not in data["fees"]:
        messagebox.showinfo("No Records", "No fee records found for the selected student.")
        return

    for record in data["fees"][student_name]:
        record["paid"] = True
    save_data()
    messagebox.showinfo("Success", "All fees marked as paid!")
    window.destroy()

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

    tk.Label(login_window, text="School Management System", font=("Arial", 14, "bold"), fg="#4CAF50").pack(pady=5)
    tk.Label(login_window, text="User ID:").pack()
    entry_id = tk.Entry(login_window)
    entry_id.pack()
    tk.Label(login_window, text="Password:").pack()
    entry_password = tk.Entry(login_window, show="*")
    entry_password.pack()
    tk.Button(login_window, text="Login", command=login).pack(pady=10)

    login_window.mainloop()

start_login()