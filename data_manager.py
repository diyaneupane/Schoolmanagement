import json
import os
from tkinter import messagebox

class DataManager:
    def __init__(self):
        self.DATA_FILE = "school_data.json"
        self.data = self.load_data()

    def load_data(self):
        if os.path.exists(self.DATA_FILE):
            try:
                with open(self.DATA_FILE, "r") as file:
                    data = json.load(file)
                    # Initialize missing keys
                    default_data = {
                        "students": [],
                        "teachers": [],
                        "attendance": {},
                        "fees": {}
                    }
                    for key in default_data:
                        if key not in data:
                            data[key] = default_data[key]
                    return data
            except:
                return self.create_empty_data()
        return self.create_empty_data()

    def create_empty_data(self):
        empty_data = {
            "students": [],
            "teachers": [],
            "attendance": {},
            "fees": {}
        }
        self.save_data(empty_data)
        return empty_data

    def save_data(self, data=None):
        if data is None:
            data = self.data
        with open(self.DATA_FILE, "w") as file:
            json.dump(data, file, indent=4)

    def delete_student(self, class_name, student_name):
        try:
            self.data["students"] = [
                s for s in self.data["students"] 
                if not (s["class"] == class_name and s["name"] == student_name)
            ]
            self.save_data()
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete student: {str(e)}")
            return False

    def delete_teacher(self, subject, teacher_name):
        try:
            self.data["teachers"] = [
                t for t in self.data["teachers"] 
                if not (t["subject"] == subject and t["name"] == teacher_name)
            ]
            self.save_data()
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete teacher: {str(e)}")
            return False
