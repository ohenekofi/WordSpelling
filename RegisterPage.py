import customtkinter as ctk
from tkinter import messagebox, Menu, Toplevel, Label, Button, StringVar, OptionMenu, Radiobutton, IntVar
# Assuming database.py is in the same directory
from database import init_db, add_user, get_user, update_last_login, update_score, get_user_stats
import config

ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light")
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue")

WINDOW_GEOMETRY = "1000x600"

class RegisterPage:
    def __init__(self, master, welcome_page):
        self.master = master
        self.welcome_page = welcome_page
        self.master.title("Register New User")
        self.master.geometry(WINDOW_GEOMETRY )

        self.frame = ctk.CTkFrame(master)
        self.frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.title_label = ctk.CTkLabel(self.frame, text="Register New User", font=ctk.CTkFont(size=20, weight="bold"))
        self.title_label.pack(pady=20)

        self.username_label = ctk.CTkLabel(self.frame, text="Username:", font=ctk.CTkFont(size=14))
        self.username_label.pack(pady=10)

        self.username_entry = ctk.CTkEntry(self.frame, width=200, font=ctk.CTkFont(size=14))
        self.username_entry.pack(pady=10)

        self.level_label = ctk.CTkLabel(self.frame, text="Choose Level:", font=ctk.CTkFont(size=14))
        self.level_label.pack(pady=10)

        self.level_var = StringVar(self.master)
        self.level_var.set("Beginner")
        self.level_options = ["Beginner", "Intermediate", "Advanced", "Master"]
        self.level_dropdown = OptionMenu(self.frame, self.level_var, *self.level_options)
        self.level_dropdown.pack(pady=10)

        self.register_button = ctk.CTkButton(self.frame, text="Register", command=self.register_user, font=ctk.CTkFont(size=14))
        self.register_button.pack(pady=20)

    def register_user(self):
        username = self.username_entry.get().strip()
        level = self.level_var.get().lower()

        if username:
            try:
                add_user(username, level)
                messagebox.showinfo("Success", "User registered successfully!")
                self.master.destroy()
                self.welcome_page.master.deiconify()  # Show the welcome window again
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Username already exists.")
        else:
            messagebox.showwarning("Input Required", "Please enter a username.")
