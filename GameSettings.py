import customtkinter as ctk
from tkinter import messagebox, Menu, Toplevel, Label, Button, StringVar, OptionMenu, Radiobutton, IntVar
from word_list import words  # Make sure this file exists with the words dictionary
# Assuming database.py is in the same directory
from database import init_db, add_user, get_user, update_last_login, update_score, get_user_stats
import config

ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light")
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue")

WINDOW_GEOMETRY = "500x300"

class GameSettings:
    def __init__(self, master):
        self.master = master
        self.settings_window = Toplevel(self.master)
        self.settings_window.title("Game Settings")
        self.settings_window.geometry(WINDOW_GEOMETRY)
        self.settings_window.grab_set()
        self.settings_window.transient(self.master)
        self.settings_window.focus_set()

        # Timer Options
        timer_label = Label(self.settings_window, text="Timer Options:")
        timer_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        self.timer_options = ["No Timer", "By Words", "By Session"]
        self.timer_var = StringVar(self.settings_window)
        self.timer_var.set(self.timer_options[0])
        timer_dropdown = OptionMenu(self.settings_window, self.timer_var, *self.timer_options)
        timer_dropdown.grid(row=0, column=1, padx=10, pady=10)

        # Time Duration
        self.time_duration_label = Label(self.settings_window, text="Time Duration:")
        self.time_duration_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.time_var = IntVar(self.settings_window)
        self.time_var.set(30)
        self.time_entry = ctk.CTkEntry(self.settings_window, width=30, font=ctk.CTkFont(size=14), textvariable=self.time_var)
        self.time_entry.grid(row=1, column=1, padx=10, pady=10)

        self.time_toggle_var = IntVar(self.settings_window)
        self.time_toggle = ctk.CTkCheckBox(self.settings_window, text="Minutes", variable=self.time_toggle_var)
        self.time_toggle.grid(row=1, column=2, padx=10, pady=10)

        # Word Length
        word_length_label = Label(self.settings_window, text="Max Word Length:")
        word_length_label.grid(row=5, column=0, padx=10, pady=10, sticky="w")

        self.word_length_var = IntVar(self.settings_window)
        self.word_length_var.set(0)
        word_length_entry = ctk.CTkEntry(self.settings_window, width=100, font=ctk.CTkFont(size=14), textvariable=self.word_length_var)
        word_length_entry.grid(row=5, column=1, padx=10, pady=10)

        # Number of Words
        num_words_label = Label(self.settings_window, text="Number of Words:")
        num_words_label.grid(row=6, column=0, padx=10, pady=10, sticky="w")

        self.num_words_var = IntVar(self.settings_window)
        self.num_words_var.set(0)
        num_words_entry = ctk.CTkEntry(self.settings_window, width=100, font=ctk.CTkFont(size=14), textvariable=self.num_words_var)
        num_words_entry.grid(row=6, column=1, padx=10, pady=10)

        # Level Selection
        level_label = Label(self.settings_window, text="Level:")
        level_label.grid(row=4, column=0, padx=10, pady=10, sticky="w")

        self.level_options = ["All Words", "Beginner", "Intermediate", "Advanced", "Master"]
        self.level_var = StringVar(self.settings_window)
        self.level_var.set(self.level_options[0])
        level_dropdown = OptionMenu(self.settings_window, self.level_var, *self.level_options)
        level_dropdown.grid(row=4, column=1, padx=10, pady=10)

        # Apply Button
        apply_button = Button(self.settings_window, text="Apply", command=self.apply_settings)
        apply_button.grid(row=10, columnspan=2, pady=20)

    def apply_settings(self):
        self.settings_window.grab_release()
        self.settings_window.destroy()

    def get_settings(self):
        return {
            "timer_option": self.timer_var.get(),
            "time_duration": self.time_var.get(),
            "is_minutes": bool(self.time_toggle_var.get()),
            "word_length": self.word_length_var.get(),
            "num_words": self.num_words_var.get(),
            "level": self.level_var.get().lower().replace(" ", "-")
        }

        