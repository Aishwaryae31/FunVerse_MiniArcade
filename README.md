🎮 FunVerse: Mini Arcade

FunVerse is a Python + Tkinter based mini arcade project that combines multiple classic games under one elegant GUI.
It’s designed for entertainment, learning basic AI logic (like Minimax in Tic-Tac-Toe), and GUI development using Tkinter.

Games Included

Tic Tac Toe (with AI using Minimax Algorithm):
Play against the computer or a friend.
The AI uses the Minimax algorithm to ensure unbeatable gameplay.
Demonstrates decision-making and recursion concepts in Python.

Rock Paper Scissors:
Simple, quick, and interactive game.
Randomized computer moves for fairness.
Displays winner using visual cues and messages.

Number Guess:
The computer picks a random number, and you guess it.
Hints are shown whether your guess is too high or too low.
Fun example of control flow and randomization.
Color Game / Memory Game (if present in your version)
Tests user memory or color recognition.
Adds variety to the arcade experience.

Tech Stack:
Language: Python 3
GUI Library: Tkinter
Modules Used:
tkinter (for UI)
random (for game logic)
messagebox (for results display)
sys (for exiting the app gracefully)

Algorithm Used:
Tic Tac Toe — Minimax Algorithm

The Minimax algorithm is a recursive decision-making technique used in two-player games.
It simulates all possible moves and their outcomes.
The computer acts as a maximizer, and the player as a minimizer.
It ensures that the computer always chooses the optimal move, making it unbeatable.

Why Minimax?
Perfect for deterministic games like Tic Tac Toe.
Easy to implement with recursion.
Demonstrates core AI logic without external libraries.

Run the Application
python funverse.py
(Make sure Python and Tkinter are installed)

Features:
Multiple games under one window
Simple, beginner-friendly GUI
Includes AI logic for Tic Tac Toe
Randomized fairness in other games
Fullscreen, colorful interface with pop-up results

Project Structure:
FunVerse-Mini-Arcade/
│
├── funverse.py Main file with Tkinter GUI
├── assets/ (Optional) Images or icons used
├── README.md
└── requirements.txt If you list dependencies

Screenshots:
homescreen-
<img width="1920" height="1021" alt="{F7572B51-E4B9-48C9-B9A9-B7167EE41586}" src="https://github.com/user-attachments/assets/44bed14c-7cf1-47ae-b14b-2982443c060c" />
Memory Challenge:
<img width="1124" height="836" alt="{F0C337A6-713F-4C0F-84E1-27B75AE03AC3}" src="https://github.com/user-attachments/assets/b354f601-a729-4d4e-bcd9-3b5c1cdcd0b9" />
Tic-tac-toe:
<img width="1915" height="989" alt="{CDC81928-3BD3-4E67-805C-EAD9EC952983}" src="https://github.com/user-attachments/assets/29bd7c85-d713-445f-9c30-46c7372284c4" />
Rock-paper-scissors:
<img width="1314" height="729" alt="{4A52786D-741B-4A81-9CB8-793EE69D2531}" src="https://github.com/user-attachments/assets/6ec3d417-d20c-42b2-856a-7239fe8b8bcd" />


Developer:
Aishwarya Marshettiwar
FunVerse: Mini Arcade — developed using Python and Tkinter as part of learning and project showcase.

License:
This project is open-source under the MIT License — free to use, modify, and share.

Future Enhancements:
Add scoreboard and player profiles
Include more mini-games like Snake or Memory Puzzle
Add sound effects and animations
Create an online version using Flask or React
