import tkinter as tk
from tkinter import messagebox
class LoginSystem:
    def __init__(self, on_login_success):
        self.USERNAME = "admin"
        self.PASSWORD = "password123"
        self.on_login_success = on_login_success

    def start_login(self):
        self.login_window = tk.Tk()
        self.login_window.title("Login - School Management System")
        self.login_window.geometry("400x300")
        self.bg_image = tk.PhotoImage(file=r"C:\Users\diyan\Downloads\school management system\bglogin.png")
        bg_label = tk.Label(self.login_window, image=self.bg_image)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        frame = tk.Frame(self.login_window, padx=20, pady=20, bg="white")
        frame.pack(expand=True)

        tk.Label(frame, text="School Management System", 
                 font=("Arial", 14, "bold"), fg="#4CAF50", bg="white").pack(pady=10)
        tk.Label(frame, text="User ID:", bg="white").pack()
        self.entry_id = tk.Entry(frame)
        self.entry_id.pack(pady=5)
        
        tk.Label(frame, text="Password:", bg="white").pack()
        self.entry_password = tk.Entry(frame, show="*")
        self.entry_password.pack(pady=5)
        
        login_button = tk.Button(frame, text="Login", command=self.login,
                                 bg="#4CAF50", fg="white", width=20)
        login_button.pack(pady=20)
        self.login_window.mainloop()

    def login(self):
        user_id = self.entry_id.get()
        password = self.entry_password.get()
        if user_id == self.USERNAME and password == self.PASSWORD:
            messagebox.showinfo("Login Successful", 
                                "Welcome to School Management System!")
            self.login_window.destroy()
            self.on_login_success()
        else:
            messagebox.showerror("Login Failed", "Invalid User ID or Password!")
