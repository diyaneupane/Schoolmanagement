import tkinter as tk
from tkinter import messagebox, ttk
import json
import os
from datetime import datetime

USERNAME = "admin"
PASSWORD = "password123"

DATA_FILE = "data.json"

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

def save_data():
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)def fee_management_page():
            
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
