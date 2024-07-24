# Spelling Game

## Overview

Spelling Game is an interactive educational application designed to help users improve their spelling skills. It offers a customizable learning experience with various difficulty levels and game modes.

## Features

- User registration and login system
- Multiple difficulty levels: Beginner, Intermediate, Advanced, Master
- Customizable game settings:
  - Number of words
  - Word length
  - Timer options (No Timer, By Words, By Session)
- Score tracking and performance summary
- User-friendly GUI built with customtkinter

## Requirements

- Python 3.x
- customtkinter
- tkinter (usually comes pre-installed with Python)
- SQLite3 (for database management)

## Installation

1. Clone the repository or download the source code.
2. Install the required dependencies:
   ```
   pip install customtkinter
   ```

## File Structure

- `main.py`: The entry point of the application
- `WelcomePage.py`: Handles user login and registration
- `RegisterPage.py`: Manages new user registration
- `GameConfig.py`: Allows users to configure game settings
- `SpellingGame.py`: The main game logic
- `ScoreSummaryPage.py`: Displays game results and options after completion
- `database.py`: Handles database operations
- `word_list.py`: Contains the dictionary of words used in the game
- `config.py`: Stores configuration settings

## How to Run

1. Navigate to the project directory in your terminal.
2. Run the following command:
   ```
   python spelling.py
   ```

## How to Play

1. Launch the application and either log in or register a new account.
2. Configure your game settings:
   - Choose a difficulty level
   - Set the number of words
   - Specify the desired word length
   - Select a timer option
3. Start the game and spell the words presented to you.
4. After completing the game, view your score summary and choose to play again, change settings, or log out.

## Game Modes

- **No Timer**: Spell words at your own pace
- **By Words**: Set a time limit for each word
- **By Session**: Set a time limit for the entire game session

## Contributing

Contributions to improve the Spelling Game are welcome. Please feel free to submit pull requests or open issues to discuss potential enhancements.

## License

This project is open-source and available under the MIT License.