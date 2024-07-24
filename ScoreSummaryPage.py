import customtkinter as ctk

class ScoreSummaryPage:
    def __init__(self, master, player_name, correct_count, wrong_count, game_settings, config_window, login_window):
        self.master = master
        self.player_name = player_name
        self.correct_count = correct_count
        self.wrong_count = wrong_count
        self.game_settings = game_settings
        self.config_window = config_window
        self.login_window = login_window

        self.master.title("Score Summary")
        self.master.geometry("600x400")

        self.frame = ctk.CTkFrame(self.master)
        self.frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.create_widgets()

    def create_widgets(self):
        ctk.CTkLabel(self.frame, text="Game Over!", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=10)
        ctk.CTkLabel(self.frame, text=f"Player: {self.player_name}", font=ctk.CTkFont(size=18)).pack(pady=5)
        ctk.CTkLabel(self.frame, text=f"Correct Words: {self.correct_count}", font=ctk.CTkFont(size=16)).pack(pady=5)
        ctk.CTkLabel(self.frame, text=f"Wrong Words: {self.wrong_count}", font=ctk.CTkFont(size=16)).pack(pady=5)
        
        total_words = self.correct_count + self.wrong_count
        accuracy = (self.correct_count / total_words) * 100 if total_words > 0 else 0
        ctk.CTkLabel(self.frame, text=f"Accuracy: {accuracy:.2f}%", font=ctk.CTkFont(size=16)).pack(pady=5)

        ctk.CTkButton(self.frame, text="Restart Game", command=self.restart_game).pack(pady=10)
        ctk.CTkButton(self.frame, text="Change Settings", command=self.change_settings).pack(pady=10)
        ctk.CTkButton(self.frame, text="Logout", command=self.logout).pack(pady=10)

    def restart_game(self):
        from SpellingGame import SpellingGame
        self.master.destroy()
        game_window = ctk.CTkToplevel(self.config_window)
        SpellingGame(game_window, self.player_name, self.game_settings, self.config_window, self.login_window)

    def change_settings(self):
        self.master.destroy()
        self.config_window.deiconify()

    def logout(self):
        self.master.destroy()
        self.config_window.destroy()
        self.login_window.deiconify()