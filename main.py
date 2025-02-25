import tkinter as tk
# Import from the same directory
from login_system import LoginSystem
try:
    from data_manager import DataManager
except ImportError:
    print("Error: data_manager module not found.")
    DataManager = None

class SchoolManagementSystem:
    def __init__(self):
        if DataManager is not None:
            self.data_manager = DataManager()
        else:
            print("DataManager is not available.")
            self.data_manager = None
        self.login_system = LoginSystem(self.start_dashboard)
        self.login_system.start_login()
        
    def start_dashboard(self):
        self.dashboard = tk.Tk()
        self.dashboard.title("School Management System")
        self.dashboard.geometry("800x600")
        self.setup_dashboard()
        
    def setup_dashboard(self):
        # Create header
        header = tk.Frame(self.dashboard, bg="#4CAF50", pady=10)
        header.pack(fill="x")
        
        title = tk.Label(header, text="School Management System", 
                        font=("Arial", 16, "bold"), bg="#4CAF50", fg="white")
        title.pack(side="left", padx=20)
        
        logout_btn = tk.Button(header, text="Logout", command=self.logout,
                             bg="red", fg="white")
        logout_btn.pack(side="right", padx=20)
        
        content = tk.Frame(self.dashboard, pady=20)
        content.pack(fill="both", expand=True)
        
        btns = [
            ("Add Student", self.show_add_student),
            ("Add Teacher", self.show_add_teacher),
            ("View Data", self.show_view_data),
            ("Mark Attendance", self.show_attendance),
            ("Fee Management", self.show_fee_management)
        ]
        
        for text, command in btns:
            btn = tk.Button(content, text=text, command=command,
                          width=20, height=2, bg="#4CAF50", fg="white")
            btn.pack(pady=10)
    
    def logout(self):
        self.dashboard.destroy()
        self.__init__()
        
    def show_add_student(self):
        pass
        
    def show_add_teacher(self):
        pass
        
    def show_view_data(self):
        pass
        
    def show_attendance(self):
        pass
        
    def show_fee_management(self):
        pass