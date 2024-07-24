import random
import customtkinter as ctk
from tkinter import messagebox, Menu, Toplevel, Label, Button, StringVar, OptionMenu, Radiobutton, IntVar
from functools import partial
from word_list import words  # Make sure this file exists with the words dictionary

ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light")
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue")



class WelcomePage:
    def __init__(self, master):
        self.master = master
        self.master.title("Welcome to Spelling Game")
        self.master.geometry("500x350")

        self.frame = ctk.CTkFrame(master)
        self.frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.title_label = ctk.CTkLabel(self.frame, text="Welcome to Spelling Game", font=ctk.CTkFont(size=20, weight="bold"))
        self.title_label.pack(pady=20)

        self.name_label = ctk.CTkLabel(self.frame, text="Enter your name:", font=ctk.CTkFont(size=14))
        self.name_label.pack(pady=10)

        self.name_entry = ctk.CTkEntry(self.frame, width=200, font=ctk.CTkFont(size=14))
        self.name_entry.pack(pady=10)

        self.start_button = ctk.CTkButton(self.frame, text="Start Game", command=self.start_game, font=ctk.CTkFont(size=14))
        self.start_button.pack(pady=20)

        self.settings_button = ctk.CTkButton(self.frame, text="Game Settings", command=self.open_settings, font=ctk.CTkFont(size=14))
        self.settings_button.pack(pady=10)

    def start_game(self):
        player_name = self.name_entry.get().strip()
        if player_name:
            self.master.withdraw()
            game_window = ctk.CTkToplevel(self.master)
            SpellingGame(game_window, player_name, self.master)
        else:
            messagebox.showwarning("Name Required", "Please enter your name to start the game.")

    def open_settings(self):
        if hasattr(self, 'game_settings') and self.game_settings and self.game_settings.settings_window.winfo_exists():
            self.game_settings.settings_window.lift()
        else:
            self.game_settings = GameSettings(self.master)

class GameSettings:
    def __init__(self, master):
        self.master = master
        self.settings_window = Toplevel(self.master)
        self.settings_window.title("Game Settings")
        self.settings_window.geometry("400x300")  # Set a specific size
        self.settings_window.grab_set()  # Prevent interaction with the main window
        self.settings_window.transient(self.master)  # Set as transient to master
        self.settings_window.focus_set()  # Set focus to this window
        self.time_toggle_var = IntVar(self.settings_window)
        self.time_toggle = ctk.CTkCheckBox(self.settings_window, text="Minutes", variable=self.time_toggle_var)
        self.time_toggle.grid(row=1, column=2, padx=10, pady=10)


        # Timer Options
        timer_label = Label(self.settings_window, text="Timer Options:")
        timer_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        self.timer_options = ["No Timer", "By Words", "By Session"]
        self.timer_var = StringVar(self.settings_window)
        self.timer_var.set(self.timer_options[0])  # Default selection
        timer_dropdown = OptionMenu(self.settings_window, self.timer_var, *self.timer_options)
        timer_dropdown.grid(row=0, column=1, padx=10, pady=10)
        
        # Time Duration
        # Time Duration
        self.time_duration_label = Label(self.settings_window, text="Time Duration:")
        self.time_duration_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        
        self.time_var = IntVar(self.settings_window)
        self.time_var.set(30)  # Default time in seconds
        self.time_entry = ctk.CTkEntry(self.settings_window, width=30, font=ctk.CTkFont(size=14), textvariable=self.time_var)
        self.time_entry.grid(row=1, column=1, padx=10, pady=10)
        
        self.time_toggle_var = IntVar(self.settings_window)
        self.time_toggle = ctk.CTkCheckBox(self.settings_window, text="Minutes", variable=self.time_toggle_var)
        self.time_toggle.grid(row=1, column=2, padx=10, pady=10)
        
        # Word Length
        word_length_label = Label(self.settings_window, text="Max Word Length:")
        word_length_label.grid(row=5, column=0, padx=10, pady=10, sticky="w")
        
        self.word_length_var = IntVar(self.settings_window)
        self.word_length_var.set(0)  # Default 0 means unlimited
        word_length_entry = ctk.CTkEntry(self.settings_window, width=100, font=ctk.CTkFont(size=14), textvariable=self.word_length_var)
        word_length_entry.grid(row=5, column=1, padx=10, pady=10)
        
        # Number of Words
        num_words_label = Label(self.settings_window, text="Number of Words:")
        num_words_label.grid(row=6, column=0, padx=10, pady=10, sticky="w")
        
        self.num_words_var = IntVar(self.settings_window)
        self.num_words_var.set(0)  # Default 0 means unlimited
        num_words_entry = ctk.CTkEntry(self.settings_window, width=100, font=ctk.CTkFont(size=14), textvariable=self.num_words_var)
        num_words_entry.grid(row=6, column=1, padx=10, pady=10)
        
        # Level Selection
        level_label = Label(self.settings_window, text="Level:")
        level_label.grid(row=4, column=0, padx=10, pady=10, sticky="w")
        
        self.level_options = ["All Words", "Beginner", "Intermediate", "Advanced", "Master"]
        self.level_var = StringVar(self.settings_window)
        self.level_var.set(self.level_options[0])  # Default selection
        level_dropdown = OptionMenu(self.settings_window, self.level_var, *self.level_options)
        level_dropdown.grid(row=4, column=1, padx=10, pady=10)
        
        # Apply Button
        apply_button = Button(self.settings_window, text="Apply", command=self.apply_settings)
        apply_button.grid(row=5, columnspan=2, pady=20)

    def apply_settings(self):
        # ... (existing code)
        self.settings_window.grab_release()  # Release grab before destroying
        self.settings_window.destroy()  # Close the settings window
        
    def get_settings(self):
        return {
        "timer_option": self.timer_var.get(),
        "time_duration": self.time_var.get(),
        "is_minutes": bool(self.time_toggle_var.get()),
            "word_length": self.word_length_var.get(),
            "num_words": self.num_words_var.get(),
            "level": self.level_var.get().lower().replace(" ", "-")
        }

class SpellingGame:
    def __init__(self, master, player_name, welcome_window):
        self.master = master
        self.welcome_window = welcome_window
        self.master.title("Spelling Game")
        self.master.geometry("1000x600")

        self.word_list = list(words)  # Convert list of dictionaries to a list
        self.game_settings = None
        self.current_word_index = 0
        self.correct_count = 0
        self.wrong_count = 0

        self.timer_active = False
        self.remaining_time = 0
        self.timer_id = None

        self.create_widgets(player_name)
        self.create_menu()
        self.next_word()

    def create_widgets(self, player_name):
        self.frame = ctk.CTkFrame(self.master)
        self.frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.top_frame = ctk.CTkFrame(self.frame)
        self.top_frame.pack(side='top', fill='x')

        self.timer_label = ctk.CTkLabel(self.top_frame, text="", font=ctk.CTkFont(size=16))
        self.timer_label.pack(side='right', padx=10)

        self.greeting_label = ctk.CTkLabel(self.top_frame, text=f"Hello, {player_name}!", font=ctk.CTkFont(size=16))
        self.greeting_label.pack(side='left', padx=10)

        self.score_frame = ctk.CTkFrame(self.top_frame)
        self.score_frame.pack(side='right', padx=10)

        self.correct_label = ctk.CTkLabel(self.score_frame, text="Correct", font=ctk.CTkFont(size=12))
        self.correct_label.grid(row=0, column=0)

        self.wrong_label = ctk.CTkLabel(self.score_frame, text="Wrong", font=ctk.CTkFont(size=12))
        self.wrong_label.grid(row=0, column=1, padx=10)

        self.correct_count_label = ctk.CTkLabel(self.score_frame, text="0", font=ctk.CTkFont(size=20, weight='bold'))
        self.correct_count_label.grid(row=1, column=0)

        self.wrong_count_label = ctk.CTkLabel(self.score_frame, text="0", font=ctk.CTkFont(size=20, weight='bold'))
        self.wrong_count_label.grid(row=1, column=1, padx=10)

        self.definition_label = ctk.CTkLabel(self.frame, text="", wraplength=550, font=ctk.CTkFont(size=14))
        self.definition_label.pack(pady=70)

        self.word_frame = ctk.CTkFrame(self.frame)
        self.word_frame.pack(pady=3)

        self.entry_boxes = []

        self.submit_button = ctk.CTkButton(self.frame, text="Submit", command=self.check_answer, font=ctk.CTkFont(size=25))
        self.submit_button.pack(pady=10)

        self.reveal_skip_button = ctk.CTkButton(self.frame, text="Reveal and Skip", command=self.reveal_and_skip, font=ctk.CTkFont(size=14))
        self.reveal_skip_button.pack(pady=10)

    def start_timer(self):
        if self.game_settings:
            settings = self.game_settings.get_settings()
            timer_option = settings['timer_option']
            time_duration = settings['time_duration']
            is_minutes = settings['is_minutes']

            if timer_option != "No Timer":
                self.timer_active = True
                self.remaining_time = time_duration * 60 if is_minutes else time_duration
                self.update_timer()

    def update_timer(self):
        if self.timer_active and self.remaining_time > 0:
            minutes, seconds = divmod(self.remaining_time, 60)
            self.timer_label.configure(text=f"Time: {minutes:02d}:{seconds:02d}")
            self.remaining_time -= 1
            self.timer_id = self.master.after(1000, self.update_timer)
        elif self.timer_active and self.remaining_time <= 0:
            self.timer_expired()

    def timer_expired(self):
        self.timer_active = False
        if self.game_settings.get_settings()['timer_option'] == "By Words":
            messagebox.showinfo("Time's up!", f"The correct word was: {self.current_word}")
            self.wrong_count += 1
            self.current_word_index += 1
            self.update_score()
            self.next_word()
        else:  # By Session
            self.show_summary()

    def show_summary(self):
        summary_window = ctk.CTkToplevel(self.master)
        summary_window.title("Game Summary")
        summary_window.geometry("500x350")

        summary_label = ctk.CTkLabel(summary_window, text=f"Correct: {self.correct_count}\nWrong: {self.wrong_count}", font=ctk.CTkFont(size=16))
        summary_label.pack(pady=20)

        restart_button = ctk.CTkButton(summary_window, text="Start Over", command=self.restart_game)
        restart_button.pack(pady=10)

    def restart_game(self):
        self.master.destroy()
        new_game_window = ctk.CTkToplevel(self.welcome_window)
        SpellingGame(new_game_window, self.player_name, self.welcome_window)


    def create_menu(self):
        menu_bar = Menu(self.master)
        file_menu = Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Logout", command=self.logout)
        file_menu.add_command(label="Minimize", command=self.minimize_window)
        file_menu.add_command(label="Close", command=self.close_window)
        menu_bar.add_cascade(label="File", menu=file_menu)

        settings_menu = Menu(menu_bar, tearoff=0)
        settings_menu.add_command(label="Configure", command=self.open_settings)
        menu_bar.add_cascade(label="Settings", menu=settings_menu)

        self.master.config(menu=menu_bar)

    def open_settings(self):
        if hasattr(self, 'game_settings') and self.game_settings and self.game_settings.settings_window.winfo_exists():
            self.game_settings.settings_window.lift()
        else:
            self.game_settings = GameSettings(self.master)

    def next_word(self):
        self.master.attributes('-topmost', True)  # Ensure game window is on top
        self.start_timer()  # Start the timer for each new word
        if self.current_word_index < len(self.word_list):
            word_info = self.word_list[self.current_word_index]
            word = word_info["word"]
            definition = word_info["definition"]

            blanks = self.create_blanks(word)
            self.current_word = word
            self.definition_label.configure(text=f"Definition: {definition}")
            self.display_word(blanks)
        else:
            messagebox.showinfo("Congratulations", f"You've completed all the words!\nFinal Score:\nCorrect: {self.correct_count}\nWrong: {self.wrong_count}")
            self.master.quit()

    def display_word(self, blanks):
        for widget in self.word_frame.winfo_children():
            widget.destroy()

        self.entry_boxes = []
        self.displayed_word = list(blanks)  # Keep track of displayed characters

        for i, ch in enumerate(blanks):
            if ch == '_':
                entry = ctk.CTkEntry(self.word_frame, width=60, font=ctk.CTkFont(size=40), justify='center')
                entry.pack(side='left', padx=5)
                self.entry_boxes.append((entry, i))
                entry.bind("<KeyRelease>", lambda event, index=len(self.entry_boxes)-1: self.on_key_release(event, index))
            else:
                label = ctk.CTkLabel(self.word_frame, text=ch, font=ctk.CTkFont(size=40))
                label.pack(side='left', padx=5)

        if self.entry_boxes:
            self.entry_boxes[0][0].focus_set()  # Set focus to the first input box

    def on_key_release(self, event, index):
        if event.keysym.isalpha() and len(event.char) == 1:  # Allow only alphabetic characters
            next_index = index + 1
            if next_index < len(self.entry_boxes):
                self.entry_boxes[next_index][0].focus_set()  # Move to the next input box
        else:
            self.entry_boxes[index][0].delete(0, "end")  # Clear the invalid input

    def check_answer(self):
        guess = list(self.displayed_word)
        for entry, index in self.entry_boxes:
            if entry.get():
                guess[index] = entry.get().lower()
            else:
                guess[index] = '_'  # Treat empty inputs as incorrect

        if ''.join(guess) == self.current_word:
            messagebox.showinfo("Correct", "That's correct!", parent=self.master)
            self.correct_count += 1
            self.current_word_index += 1
            self.update_score()
            self.next_word()
        else:
            messagebox.showerror("Incorrect", "Sorry, that's not correct. Try again.", parent=self.master)
            self.wrong_count += 1
            self.update_score()

    def reveal_and_skip(self):
        messagebox.showinfo("Reveal", f"The correct word was: {self.current_word}", parent=self.master)
        self.wrong_count += 1
        self.current_word_index += 1
        self.update_score()
        self.next_word()

    def update_score(self):
        self.correct_count_label.configure(text=str(self.correct_count))
        self.wrong_count_label.configure(text=str(self.wrong_count))

    def logout(self):
        self.master.destroy()
        self.welcome_window.deiconify()  # Show the welcome window again

    def minimize_window(self):
        self.master.iconify()

    def close_window(self):
        if messagebox.askyesno("Quit", "Are you sure you want to quit?"):
            self.master.quit()

    def create_blanks(self, word):
        word_length = len(word)
        min_visible = max(1, int(word_length * 0.3))  # At least 30% of characters, minimum 1
        
        # Create a list of indices for alphabetic characters
        alpha_indices = [i for i, char in enumerate(word) if char.isalpha()]
        
        # Randomly select indices to reveal
        reveal_indices = random.sample(alpha_indices, min_visible)
        
        blanks = ""
        for i, letter in enumerate(word):
            if not letter.isalpha() or i in reveal_indices:
                blanks += letter
            else:
                blanks += "_"
        
        return blanks


if __name__ == "__main__":
    root = ctk.CTk()
    welcome_page = WelcomePage(root)
    root.mainloop()