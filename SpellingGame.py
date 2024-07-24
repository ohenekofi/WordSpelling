import random
import time
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from word_list import words  # Make sure to import the words list
from ScoreSummaryPage import ScoreSummaryPage

class SpellingGame:
    def __init__(self, master, player_name, game_settings, config_window, login_window):
        self.master = master
        self.player_name = player_name
        self.game_settings = game_settings
        self.config_window = config_window
        self.login_window = login_window

        self.master.title("Spelling Game")
        self.master.geometry("1000x650")

        self.start_time = time.time()
        self.elapsed_time = 0

        self.word_list = self.filter_words()
        self.current_word_index = 0
        self.correct_count = 0
        self.wrong_count = 0
        self.total_word_count = 0

        self.timer_active = False
        self.remaining_time = 0
        self.timer_id = None

        self.create_widgets()
        self.next_word()

    def filter_words(self):
        if self.game_settings['level'] != "all words":
            filtered_words = [word for word in words if word['level'] == self.game_settings['level']]
        else:
            filtered_words = words

        if self.game_settings['char_length']:
            filtered_words = [word for word in filtered_words if len(word['word']) == self.game_settings['char_length']]
        
        if self.game_settings['num_words']:
            filtered_words = random.sample(filtered_words, min(self.game_settings['num_words'], len(filtered_words)))
        
        return filtered_words

    def create_widgets(self):
        self.frame = ctk.CTkFrame(self.master)
        self.frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.top_frame = ctk.CTkFrame(self.frame)
        self.top_frame.pack(side='top', fill='x')

        self.timer_label = ctk.CTkLabel(self.top_frame, text="", font=ctk.CTkFont(size=16))
        self.timer_label.pack(side='right', padx=10)

        self.timer_track_label = ctk.CTkLabel(self.top_frame, text="", font=ctk.CTkFont(size=16))
        self.timer_track_label.pack(side='right', padx=10)

        self.greeting_label = ctk.CTkLabel(self.top_frame, text=f"Hello, {self.player_name}! - Level: {self.game_settings['level']}", font=ctk.CTkFont(size=16))
        self.greeting_label.pack(side='left', padx=10)

        self.update_elapsed_time()

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

        self.total_word_count_label = ctk.CTkLabel(self.top_frame, text="Total Words: 0", font=ctk.CTkFont(size=16))
        self.total_word_count_label.pack(side='right', padx=10)

        self.definition_label = ctk.CTkLabel(self.frame, text="", font=ctk.CTkFont(size=16))
        self.definition_label.pack(pady=20)

        self.word_frame = ctk.CTkFrame(self.frame)
        self.word_frame.pack(pady=10)

        self.controls_frame = ctk.CTkFrame(self.frame)
        self.controls_frame.pack(side='bottom', pady=20)

        self.check_button = ctk.CTkButton(self.controls_frame, text="Check", command=self.check_answer)
        self.check_button.grid(row=0, column=0, padx=10)

        self.skip_button = ctk.CTkButton(self.controls_frame, text="Reveal & Skip", command=self.reveal_and_skip)
        self.skip_button.grid(row=0, column=1, padx=10)

        self.logout_button = ctk.CTkButton(self.controls_frame, text="Logout", command=self.logout)
        self.logout_button.grid(row=0, column=2, padx=10)

    def start_timer(self):
        self.timer_active = True
        print(self.game_settings['timer_option'])
        if self.game_settings['timer_option'] == "By Words":
            self.remaining_time = self.game_settings['timer_duration']
            self.update_timer()
        elif self.game_settings['timer_option'] == "By Session":
            self.remaining_time = self.game_settings['timer_duration']
            self.timer_id = self.master.after(1000, self.update_timer)

    def update_timer(self):
        if self.remaining_time > 0 and self.timer_active:
            mins, secs = divmod(self.remaining_time, 60)
            self.timer_label.configure(text=f"Time Remaining: {mins:02d}:{secs:02d}")
            self.remaining_time -= 1
            self.timer_id = self.master.after(1000, self.update_timer)
        elif self.remaining_time <= 0:
            self.time_up()

    def time_up(self):
        if self.game_settings['timer_option'] == "By Words":
            messagebox.showinfo("Time's Up!", f"Time's up! The word was: '{self.current_word}'", parent=self.master)
            self.wrong_count += 1
            self.update_score()
            self.current_word_index += 1
            self.next_word()
        elif self.game_settings['timer_option'] == "By Session":
            if self.master.winfo_exists():
                self.master.withdraw()
            summary_window = ctk.CTkToplevel(self.config_window)
            ScoreSummaryPage(summary_window, self.player_name, self.correct_count, self.wrong_count, 
                             self.game_settings, self.config_window, self.login_window)
            if self.master.winfo_exists():
                self.master.destroy()

    def next_word(self):
        if not self.master.winfo_exists():
            return

        if self.master.winfo_exists():
            self.master.attributes('-topmost', True)
        
        # Cancel any existing timer
        if self.timer_id:
            self.master.after_cancel(self.timer_id)
        
        # Reset and start the timer
        self.timer_active = False
        self.start_timer()
        
        if self.current_word_index < len(self.word_list):
            self.total_word_count += 1
            word_info = self.word_list[self.current_word_index]
            word = word_info["word"]
            definition = word_info["definition"]

            blanks = self.create_blanks(word)
            self.current_word = word
            if self.definition_label.winfo_exists():
                self.definition_label.configure(text=f"Definition: {definition}")
            self.display_word(blanks)
            self.update_total_word_count()
        else:
            if self.master.winfo_exists():
                self.master.withdraw()
            summary_window = ctk.CTkToplevel(self.config_window)
            ScoreSummaryPage(summary_window, self.player_name, self.correct_count, self.wrong_count, 
                             self.game_settings, self.config_window, self.login_window)
            if self.master.winfo_exists():
                self.master.destroy()


    def update_total_word_count(self):
        self.safe_update_label(self.total_word_count_label, f"Total Words: {self.total_word_count}")


    def update_elapsed_time(self):
        self.elapsed_time = time.time() - self.start_time
        mins, secs = divmod(int(self.elapsed_time), 60)
        self.timer_track_label.configure(text=f"Time Elapsed: {mins:02d}:{secs:02d}")
        self.master.after(1000, self.update_elapsed_time)

    def safe_update_label(self, label, text):
        if label.winfo_exists():
            label.configure(text=text)

    def display_word(self, blanks):
        for widget in self.word_frame.winfo_children():
            widget.destroy()

        self.entry_boxes = []
        self.displayed_word = list(blanks)

        for i, ch in enumerate(blanks):
            if ch == '_':
                entry = ctk.CTkEntry(self.word_frame, width=60, font=ctk.CTkFont(size=40), justify='center')
                entry.pack(side='left', padx=5)
                self.entry_boxes.append((entry, i))
                entry.bind("<KeyRelease>", lambda event, index=len(self.entry_boxes)-1: self.on_key_release(event, index))
            else:
                label = ctk.CTkLabel(self.word_frame, text=ch, font=ctk.CTkFont(size=40))
                label.pack(side='left', padx=5)

        if self.entry_boxes and self.master.winfo_exists():
            self.master.after(100, self.focus_first_entry)

    def focus_first_entry(self):
        if self.entry_boxes:
            try:
                self.entry_boxes[0][0].focus_set()
            except tk.TclError:
                pass  # If the widget doesn't exist, just skip setting focus

    def on_key_release(self, event, index):
        if event.keysym.isalpha() and len(event.char) == 1:
            next_index = index + 1
            if next_index < len(self.entry_boxes):
                self.master.after(10, lambda: self.focus_entry(next_index))
        else:
            if self.master.winfo_exists():
                self.entry_boxes[index][0].delete(0, "end")

    def focus_entry(self, index):
        try:
            self.entry_boxes[index][0].focus_set()
        except tk.TclError:
            pass  # If the widget doesn't exist, just skip setting focus

    def check_answer(self):
        guess = list(self.displayed_word)
        for entry, index in self.entry_boxes:
            if entry.get():
                guess[index] = entry.get().lower()
            else:
                guess[index] = '_'

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
            self.current_word_index += 1
            #self.next_word()

    def reset_timer(self):
        if self.timer_id:
            self.master.after_cancel(self.timer_id)
            self.timer_active = False

    def reveal_and_skip(self):
        messagebox.showinfo("Word Revealed", f"The word was: '{self.current_word}'", parent=self.master)
        self.wrong_count += 1
        self.update_score()
        self.current_word_index += 1
        self.next_word()

    def update_score(self):
        self.safe_update_label(self.correct_count_label, str(self.correct_count))
        self.safe_update_label(self.wrong_count_label, str(self.wrong_count))
        self.safe_update_label(self.total_word_count_label, f"Total Words: {self.total_word_count}")

    def logout(self):
        self.master.destroy()
        self.config_window.deiconify()

    def minimize_window(self):
        self.master.iconify()

    def close_window(self):
        if messagebox.askyesno("Quit", "Are you sure you want to quit?"):
            self.master.quit()

    def create_blanks(self, word):
        word_length = len(word)
        min_visible = max(1, int(word_length * 0.3))

        alpha_indices = [i for i, char in enumerate(word) if char.isalpha()]

        reveal_indices = random.sample(alpha_indices, min_visible)

        blanks = ""
        for i, letter in enumerate(word):
            if not letter.isalpha() or i in reveal_indices:
                blanks += letter
            else:
                blanks += "_"

        return blanks
