import customtkinter as ctk
from tkinter import Toplevel, messagebox
from  SpellingGame import SpellingGame

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

WINDOW_GEOMETRY = "1000x600"

class GameConfig:
    def __init__(self, master, player_name, login_window):
        self.master = master
        self.player_name = player_name
        self.login_window = login_window

        self.master.title("Game Configuration")
        self.master.geometry("500x400")

        self.frame = ctk.CTkFrame(self.master)
        self.frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.create_widgets()

    def create_widgets(self):
        ctk.CTkLabel(self.frame, text=f"Welcome, {self.player_name}!", font=ctk.CTkFont(size=20)).grid(row=0, column=0, columnspan=2, pady=10)

        ctk.CTkLabel(self.frame, text="Select Difficulty Level:", font=ctk.CTkFont(size=16)).grid(row=1, column=0, pady=10, sticky='e')
        self.level_var = ctk.StringVar(value="all words")
        ctk.CTkOptionMenu(self.frame, variable=self.level_var, values=["all words", "beginner", "intermediate", "advanced", "master"]).grid(row=1, column=1, pady=10, sticky='w')

        ctk.CTkLabel(self.frame, text="Number of Words:", font=ctk.CTkFont(size=16)).grid(row=2, column=0, pady=10, sticky='e')
        self.num_words_entry = ctk.CTkEntry(self.frame, width=200)
        self.num_words_entry.grid(row=2, column=1, pady=10, sticky='w')

        ctk.CTkLabel(self.frame, text="Character Length:", font=ctk.CTkFont(size=16)).grid(row=3, column=0, pady=10, sticky='e')
        self.char_length_entry = ctk.CTkEntry(self.frame, width=200)
        self.char_length_entry.grid(row=3, column=1, pady=10, sticky='w')

        ctk.CTkLabel(self.frame, text="Timer Option:", font=ctk.CTkFont(size=16)).grid(row=4, column=0, pady=10, sticky='e')
        self.timer_option_var = ctk.StringVar(value="No Timer")
        ctk.CTkOptionMenu(self.frame, variable=self.timer_option_var, values=["No Timer", "By Words", "By Session"]).grid(row=4, column=1, pady=10, sticky='w')

        ctk.CTkLabel(self.frame, text="Timer Duration (seconds):", font=ctk.CTkFont(size=16)).grid(row=5, column=0, pady=10, sticky='e')
        self.timer_duration_entry = ctk.CTkEntry(self.frame, width=200)
        self.timer_duration_entry.grid(row=5, column=1, pady=10, sticky='w')

        self.start_button = ctk.CTkButton(self.frame, text="Start Game", command=self.start_game)
        self.start_button.grid(row=6, column=0, columnspan=2, pady=20)

    def start_game(self):
        level = self.level_var.get()
        num_words = self.num_words_entry.get().strip()
        char_length = self.char_length_entry.get().strip()
        timer_option = self.timer_option_var.get()
        timer_duration = self.timer_duration_entry.get().strip()

        try:
            num_words = int(num_words) if num_words else None
            char_length = int(char_length) if char_length else None
            timer_duration = int(timer_duration) if timer_duration else None
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for the fields")
            return

        game_settings = {
            'level': level,
            'num_words': num_words,
            'char_length': char_length,
            'timer_option': timer_option,
            'timer_duration': timer_duration
        }

        self.master.withdraw()
        game_window = ctk.CTkToplevel(self.master)
        SpellingGame(game_window, self.player_name, game_settings, self.master, self.login_window)