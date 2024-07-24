import random
import customtkinter as ctk
from tkinter import messagebox, Menu, Toplevel, Label, Button, StringVar, OptionMenu, Radiobutton, IntVar
from functools import partial
from word_list import words  # Make sure this file exists with the words dictionary
from RegisterPage import RegisterPage  # Make sure this file exists with the words dictionary
# Assuming database.py is in the same directory
from database import init_db, add_user, get_user, update_last_login, update_score, get_user_stats
import config
from  GameSettings import GameSettings
from GameConfig import GameConfig

ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light")
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue")

WINDOW_GEOMETRY = "1000x600"



class WelcomePage:
    def __init__(self, master):
        self.master = master
        self.master.title("Welcome to Spelling Game")
        self.master.geometry(WINDOW_GEOMETRY)

        self.frame = ctk.CTkFrame(master)
        self.frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.title_label = ctk.CTkLabel(self.frame, text="Welcome to Spelling Game", font=ctk.CTkFont(size=20, weight="bold"))
        self.title_label.pack(pady=20)

        self.name_label = ctk.CTkLabel(self.frame, text="Enter your username:", font=ctk.CTkFont(size=14))
        self.name_label.pack(pady=10)

        self.name_entry = ctk.CTkEntry(self.frame, width=200, font=ctk.CTkFont(size=14))
        self.name_entry.pack(pady=10)

        self.start_button = ctk.CTkButton(self.frame, text="Login", command=self.login, font=ctk.CTkFont(size=14))
        self.start_button.pack(pady=20)

        self.register_button = ctk.CTkButton(self.frame, text="Register", command=self.open_register, font=ctk.CTkFont(size=14))
        self.register_button.pack(pady=10)

    def login(self):
        username = self.name_entry.get().strip()
        if username:
            user = get_user(username)
            if user:
                user_id, username, level, high_score, last_login = user
                update_last_login(user_id)
                self.master.withdraw()
                config_window = ctk.CTkToplevel(self.master)
                GameConfig(config_window, username, self.master)
            else:
                messagebox.showerror("Error", "User not found.")
        else:
            messagebox.showwarning("Input Required", "Please enter your username.")

    def open_register(self):
        self.master.withdraw()
        register_window = Toplevel(self.master)
        RegisterPage(register_window, self)



if __name__ == "__main__":
    # Initialize the database
    init_db()
    root = ctk.CTk()
    welcome_page = WelcomePage(root)
    root.mainloop()