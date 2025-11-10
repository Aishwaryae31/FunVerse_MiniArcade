
import tkinter as tk
from tkinter import messagebox
import random
import sys
import winsound
winsound.Beep(1000, 300)




# -----------------------------
# Setup Root Window
# -----------------------------
root = tk.Tk()
root.title("FunVerse: Mini Arcade 🎮")

# Fullscreen (maximized)
try:
    root.state('zoomed')
except Exception:
    # fallback for platforms that don't support 'zoomed'
    root.attributes("-fullscreen", True)
root.configure(bg="#f3f7fb")

# ESC key to exit
root.bind("<Escape>", lambda e: root.destroy())


# -----------------------------
# Sound Helper
# -----------------------------

try:
    from playsound import playsound
    _HAS_PLAYSOUND = True
except Exception:
    _HAS_PLAYSOUND = False

def play_sound(kind):
    if _HAS_PLAYSOUND:
        try:
            sounds = {
                "click": "click.mp3",
                "correct": "correct.mp3",
                "wrong": "wrong.mp3",
                "win": "win.mp3"
            }
            if kind in sounds:
                playsound(sounds[kind], block=False)
        except Exception:
            pass
    else:
        try:
            root.bell()
        except Exception:
            pass



# -----------------------------
# Utility Functions
# -----------------------------
def clear_root():
    for w in root.winfo_children():
        w.destroy()


def post_game_prompt(replay_fn, home_fn):
    play_sound("win")

    def prompt():
        if messagebox.askyesno("Game Over", "Replay this game?"):
            replay_fn()
        else:
            home_fn()
    root.after(250, prompt)


# -----------------------------
# Home Screen
# -----------------------------
def show_home():
    clear_root()
    root.configure(bg="#f3f7fb")
    play_sound("click")

    frame = tk.Frame(root, bg="#f3f7fb")
    frame.pack(expand=True)

    title = tk.Label(frame, text="🎮 FunVerse: Mini Arcade 🎮",
                     font=("Comic Sans MS", 42, "bold"), bg="#f3f7fb", fg="#2b547e")
    title.pack(pady=30)

    sub = tk.Label(frame, text="Choose your challenge:",
                   font=("Arial", 20), bg="#f3f7fb")
    sub.pack(pady=10)

    btn_cfg = {"width": 36, "height": 2, "font": ("Arial", 16)}
    tk.Button(frame, text="1.Memory Challenge — Color Match", bg="#ffe5d0",
              command=memory_menu, **btn_cfg).pack(pady=10)
    tk.Button(frame, text="2.Hand Wars — Rock Paper Scissors (vs AI)", bg="#e6f7ff",
              command=hand_wars_game, **btn_cfg).pack(pady=10)
    tk.Button(frame, text="3.Color Predictor (Guess the Color)", bg="#f0e6ff",
              command=color_predictor_menu, **btn_cfg).pack(pady=10)
    tk.Button(frame, text="4.Mind Guess 3000 — Number Guess", bg="#fff6d6",
              command=mind_guess_menu, **btn_cfg).pack(pady=10)
    tk.Button(frame, text="5.Tic-Tac-Toe", bg="#e3ffe3",
              command=tictactoe_menu, **btn_cfg).pack(pady=10)


    # Exit button stays visible
    exit_btn = tk.Button(root, text="Exit Game", width=20, bg="#ff9999",
                         font=("Arial", 16, "bold"), command=root.destroy)
    exit_btn.pack(side="bottom", pady=20)


# -----------------------------
# 1️⃣ Memory Challenge
# -----------------------------
def memory_menu():
    clear_root()
    root.configure(bg="#fff7ec")

    tk.Label(root, text="🧠 Memory Challenge", font=("Comic Sans MS", 30, "bold"),
             bg="#fff7ec", fg="#b02e0c").pack(pady=30)
    tk.Label(root, text="Choose number of pairs (4 / 6 / 8):",
             bg="#fff7ec", font=("Arial", 16)).pack(pady=10)

    pairs_var = tk.StringVar(value="6")
    tk.Entry(root, textvariable=pairs_var, width=6,
             font=("Arial", 16)).pack(pady=10)

    def start():
        try:
            p = int(pairs_var.get())
            if p not in (4, 6, 8):
                raise ValueError
        except:
            messagebox.showerror("Invalid", "Enter 4, 6, or 8 pairs.")
            return
        memory_game(p)
    tk.Button(root, text="Start Game", width=14, bg="#ffd6a5",
              font=("Arial", 14), command=start).pack(pady=10)
    tk.Button(root, text="Return Home", width=14,
              font=("Arial", 12), command=show_home).pack(pady=10)


def memory_game(pairs):
    clear_root()
    root.configure(bg="#fff7ec")

    tk.Label(root, text=f"Memory Challenge — Find {pairs} Pairs", font=("Comic Sans MS", 28, "bold"),
             bg="#fff7ec", fg="#b02e0c").pack(pady=20)

    colors = ["red", "blue", "green", "yellow", "purple", "orange", "pink",
              "cyan", "lime", "teal", "magenta", "brown"]
    random.shuffle(colors)
    chosen = colors[:pairs]
    tiles = chosen * 2
    random.shuffle(tiles)

    revealed = [False]*len(tiles)
    matched = [False]*len(tiles)
    first = [None]
    matches = [0]

    grid = tk.Frame(root, bg="#fff7ec")
    grid.pack(pady=20)
    buttons = []

    def reveal(i):
        if matched[i] or revealed[i]:
            return
        play_sound("click")
        revealed[i] = True
        buttons[i].config(bg=tiles[i], state="disabled")
        if first[0] is None:
            first[0] = i
            return
        j = first[0]
        if tiles[i] == tiles[j]:
            matched[i] = matched[j] = True
            matches[0] += 1
            play_sound("correct")
            first[0] = None
            if matches[0] == pairs:
                post_game_prompt(lambda: memory_game(pairs), show_home)
        else:
            play_sound("wrong")

            def hide():
                revealed[i] = revealed[j] = False
                buttons[i].config(bg="SystemButtonFace", state="normal")
                buttons[j].config(bg="SystemButtonFace", state="normal")
            root.after(600, hide)
            first[0] = None

    cols = 4
    for idx, _ in enumerate(tiles):
        b = tk.Button(grid, width=12, height=5, command=lambda i=idx: reveal(i))
        b.grid(row=idx//cols, column=idx % cols, padx=8, pady=8)
        buttons.append(b)

    tk.Button(root, text="Return Home", width=14,
              font=("Arial", 12), command=show_home).pack(pady=20)


# -----------------------------
# 2️⃣ Hand Wars (RPS vs AI)
# -----------------------------
def hand_wars_game():
    clear_root()
    root.configure(bg="#f3f7fb")

    tk.Label(root, text="⚔️ Hand Wars — Rock Paper Scissors (AI)", font=("Comic Sans MS", 28, "bold"),
             bg="#f3f7fb", fg="#9b2d2d").pack(pady=30)

    result_label = tk.Label(root, text="", font=("Arial", 20), bg="#f3f7fb")
    result_label.pack(pady=10)

    choices = ["rock", "paper", "scissors"]

    def play(choice):
        play_sound("click")
        ai = random.choice(choices)
        if ai == choice:
            msg = f"🤝 Tie! AI chose {ai}"
            play_sound("wrong")
        elif (choice == "rock" and ai == "scissors") or (choice == "paper" and ai == "rock") or (choice == "scissors" and ai == "paper"):
            msg = f"🔥 You win! AI chose {ai}"
            play_sound("correct")
        else:
            msg = f"💀 You lose! AI chose {ai}"
            play_sound("wrong")
        result_label.config(text=msg)
        root.after(300, lambda: post_game_prompt(hand_wars_game, show_home))

    btn_frame = tk.Frame(root, bg="#f3f7fb")
    btn_frame.pack(pady=10)
    for c in choices:
        tk.Button(btn_frame, text=c.capitalize(), width=14, height=2, bg="#ffd6d6",
                  font=("Arial", 14), command=lambda x=c: play(x)).pack(side="left", padx=10)

    tk.Button(root, text="Return Home", width=14,
              font=("Arial", 12), command=show_home).pack(pady=20)


# -----------------------------
# 3️⃣ Color Predictor (Robust hints + validation)
# -----------------------------
def color_predictor_menu():
    clear_root()
    root.configure(bg="#f3f7fb")

    tk.Label(root, text="🎨 Color Predictor", font=("Comic Sans MS", 28, "bold"),
             bg="#f3f7fb", fg="#6b3a8a").pack(pady=20)
    tk.Label(root, text="Guess the color name or reveal the answer!",
             font=("Arial", 16), bg="#f3f7fb").pack(pady=8)
    tk.Button(root, text="Start", width=12, font=("Arial", 14),
              bg="#e7dfff", command=color_predictor_game).pack(pady=10)
    tk.Button(root, text="Return Home", width=14,
              font=("Arial", 12), command=show_home).pack(pady=10)


def color_predictor_game():
    clear_root()
    root.configure(bg="#f3f7fb")

    tk.Label(root, text="🎨 Color Predictor", font=("Comic Sans MS", 28, "bold"),
             bg="#f3f7fb", fg="#6b3a8a").pack(pady=20)

    # canonical list of colors we accept
    colors = ["red", "blue", "green", "yellow", "purple", "orange", "pink", "brown",
              "black", "white", "gray", "grey", "teal", "magenta", "cyan", "lime", "navy"]
    # to avoid picking ambiguous duplicates like gray/grey at random every time,
    # pick from a canonical subset for the secret (choose one spelling only)
    secret_choices = ["red", "blue", "green", "yellow", "purple", "orange", "pink", "brown",
                      "black", "white", "gray", "teal", "magenta", "cyan"]
    secret = random.choice(secret_choices)
    attempts = [0]

    tk.Label(root, text="Enter your color guess:", font=("Arial", 16), bg="#f3f7fb").pack(pady=10)
    entry = tk.Entry(root, font=("Arial", 18), width=15)
    entry.pack(pady=10)
    entry.focus_set()

    result = tk.Label(root, text="", font=("Arial", 16), bg="#f3f7fb", justify="left")
    result.pack(pady=6)

    swatch = tk.Label(root, text="     ", bg="#f3f7fb",
                      width=20, height=2, relief="ridge")
    swatch.pack(pady=6)

    info = tk.Label(root, text=f"(Allowed colors: {', '.join(sorted(set(colors)))})", bg="#f3f7fb", font=("Arial", 10))
    info.pack(pady=4)

    def compute_hints(guess, secret_word):
        # position hint (letter correct in same position) and present letters (correct but wrong position)
        pos_hint = []
        secret_chars = list(secret_word)
        guess_chars = list(guess)

        # First pass: correct positions
        for i in range(max(len(guess_chars), len(secret_chars))):
            if i < len(guess_chars) and i < len(secret_chars) and guess_chars[i] == secret_chars[i]:
                pos_hint.append(guess_chars[i])
                # mark as used
                secret_chars[i] = None
            else:
                pos_hint.append("_")

        # Second pass: letters present elsewhere
        present = []
        # reconstruct available secret letters (those not matched in position)
        remaining = [c for c in secret_chars if c is not None]
        for i, ch in enumerate(guess_chars):
            if i < len(secret_word) and ch == secret_word[i]:
                # already handled as positioned match
                continue
            if ch in remaining:
                present.append(ch)
                # remove one occurrence to avoid duplicates
                remaining.remove(ch)

        # unique present letters (keep order guessed)
        present_unique = []
        for ch in present:
            if ch not in present_unique:
                present_unique.append(ch)

        # ensure pos_hint length equals secret length for clarity
        if len(pos_hint) > len(secret_word):
            pos_hint = pos_hint[:len(secret_word)]
        elif len(pos_hint) < len(secret_word):
            pos_hint.extend(["_"] * (len(secret_word) - len(pos_hint)))

        return "".join(pos_hint), present_unique

    def check():
        play_sound("click")
        g_raw = entry.get().strip()
        g = g_raw.lower()
        if not g:
            result.config(text="Enter a color name!", fg="orange")
            entry.focus_set()
            return

        # Validate guess — prefer to require guesses from allowed list so hints make sense
        if g not in colors:
            result.config(text=f"Unknown color '{g_raw}'. Try one of: {', '.join(sorted(set(colors)))}", fg="orange")
            entry.delete(0, tk.END)
            entry.focus_set()
            return

        attempts[0] += 1

        if g == secret:
            play_sound("correct")
            swatch.config(bg=secret)
            messagebox.showinfo("Correct!", f"You guessed '{secret}' in {attempts[0]} tries.")
            post_game_prompt(color_predictor_game, show_home)
            return
        else:
            play_sound("wrong")
            pos_hint, present_letters = compute_hints(g, secret)
            present_display = ", ".join(present_letters) if present_letters else "None"
            # show both hints: positional mask and letters present elsewhere
            result_text = (f"❌ Wrong guess: {g_raw}\n"
                           f"Position hint: {pos_hint}\n"
                           f"Letters present elsewhere: {present_display}\n"
                           f"Attempts: {attempts[0]}")
            result.config(text=result_text, fg="red")
            # clear entry and keep focus for next try
            entry.delete(0, tk.END)
            entry.focus_set()

    def show_answer():
        play_sound("click")
        swatch.config(bg=secret)
        messagebox.showinfo("Answer", f"The color was: {secret}")
        post_game_prompt(color_predictor_game, show_home)

    tk.Button(root, text="Check", width=12, bg="#d7c8ff",
              font=("Arial", 14), command=check).pack(pady=6)
    tk.Button(root, text="Show Answer", width=12, bg="#ffd6d6",
              font=("Arial", 14), command=show_answer).pack(pady=6)
    tk.Button(root, text="Return Home", width=14,
              font=("Arial", 12), command=show_home).pack(pady=10)


# -----------------------------
# 4️⃣ Mind Guess 3000
# -----------------------------
def mind_guess_menu():
    clear_root()
    root.configure(bg="#fff6d6")
    tk.Label(root, text="🔢 Mind Guess 3000", font=("Comic Sans MS", 28, "bold"),
             bg="#fff6d6", fg="#8b5e3c").pack(pady=30)
    tk.Label(root, text="Enter max range (e.g., 50 or 100):",
             bg="#fff6d6", font=("Arial", 16)).pack(pady=10)

    rng_var = tk.StringVar(value="100")
    tk.Entry(root, textvariable=rng_var, width=8,
             font=("Arial", 16)).pack(pady=10)

    def start():
        try:
            mx = int(rng_var.get())
            if mx < 10 or mx > 10000:
                raise ValueError
        except:
            messagebox.showerror("Invalid", "Enter integer between 10 and 10000")
            return
        mind_guess_game(mx)

    tk.Button(root, text="Start Game", width=14, bg="#ffdca3",
              font=("Arial", 14), command=start).pack(pady=10)
    tk.Button(root, text="Return Home", width=14,
              font=("Arial", 12), command=show_home).pack(pady=10)


def mind_guess_game(max_value):
    clear_root()
    root.configure(bg="#fff6d6")

    tk.Label(root, text=f"Mind Guess 3000 (1 - {max_value})", font=("Comic Sans MS", 28, "bold"),
             bg="#fff6d6", fg="#8b5e3c").pack(pady=20)

    secret = random.randint(1, max_value)
    attempts = [0]

    tk.Label(root, text="Enter your guess:",
             bg="#fff6d6", font=("Arial", 16)).pack(pady=10)
    entry = tk.Entry(root, font=("Arial", 18), width=12)
    entry.pack(pady=10)

    result = tk.Label(root, text="", bg="#fff6d6", font=("Arial", 16))
    result.pack(pady=10)

    def check():
        play_sound("click")
        val = entry.get().strip()
        if not val:
            result.config(text="Enter a number!", fg="orange")
            return
        try:
            g = int(val)
        except:
            result.config(text="Invalid input!", fg="red")
            return
        attempts[0] += 1
        if g < secret:
            play_sound("wrong")
            result.config(text="Too Low!", fg="red")
        elif g > secret:
            play_sound("wrong")
            result.config(text="Too High!", fg="red")
        else:
            play_sound("correct")
            messagebox.showinfo(
                "Congrats!", f"You guessed {secret} in {attempts[0]} tries!")
            post_game_prompt(lambda: mind_guess_game(max_value), show_home)

    tk.Button(root, text="Check", width=12, bg="#ffdca3",
              font=("Arial", 14), command=check).pack(pady=8)
    tk.Button(root, text="Return Home", width=14,
              font=("Arial", 12), command=show_home).pack(pady=20)


# -----------------------------
# 5️⃣ Tic-Tac-Toe (AI and 2-player)
# -----------------------------
def tictactoe_menu():
    clear_root()
    root.configure(bg="#e3ffe3")
    tk.Label(root, text="❌⭕ Tic-Tac-Toe", font=("Comic Sans MS", 30, "bold"),
             bg="#e3ffe3", fg="#116611").pack(pady=30)
    tk.Label(root, text="Choose mode:", font=("Arial", 16), bg="#e3ffe3").pack(pady=10)

    tk.Button(root, text="1. Player vs AI", width=20, font=("Arial", 14), bg="#d9ffd9",
              command=lambda: tictactoe_game(mode='ai')).pack(pady=8)
    tk.Button(root, text="2. 2-Player Local", width=20, font=("Arial", 14), bg="#d9ffd9",
              command=lambda: tictactoe_game(mode='2p')).pack(pady=8)
    tk.Button(root, text="Return Home", width=14,
              font=("Arial", 12), command=show_home).pack(pady=20)


# Helper: check for win or draw
def check_winner(board):
    wins = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
    for a,b,c in wins:
        if board[a] and board[a] == board[b] == board[c]:
            return board[a]
    if all(board):
        return 'Draw'
    return None


# Minimax AI for Tic-Tac-Toe
def minimax(board, player):
    winner = check_winner(board)
    if winner == 'X':
        return {'score': -1}
    elif winner == 'O':
        return {'score': 1}
    elif winner == 'Draw':
        return {'score': 0}

    moves = []
    for i in range(9):
        if not board[i]:
            move = {}
            move['index'] = i
            board[i] = player
            if player == 'O':
                result = minimax(board, 'X')
                move['score'] = result['score']
            else:
                result = minimax(board, 'O')
                move['score'] = result['score']
            board[i] = None
            moves.append(move)

    # choose best move
    if player == 'O':  # AI tries to maximize
        best = max(moves, key=lambda x: x['score'])
    else:  # human (X) tries to minimize
        best = min(moves, key=lambda x: x['score'])
    return best


def tictactoe_game(mode='ai'):
    clear_root()
    root.configure(bg="#e3ffe3")

    tk.Label(root, text="❌⭕ Tic-Tac-Toe", font=("Comic Sans MS", 28, "bold"),
             bg="#e3ffe3", fg="#116611").pack(pady=20)

    info = tk.Label(root, text=("You are X. AI is O." if mode=='ai' else "Player 1: X     Player 2: O"),
                    font=("Arial", 14), bg="#e3ffe3")
    info.pack(pady=8)

    board = [None]*9
    buttons = [None]*9
    current = ['X']  # 'X' starts

    board_frame = tk.Frame(root, bg="#e3ffe3")
    board_frame.pack(pady=10)

    def make_move(i):
        if board[i] or check_winner(board):
            return
        play_sound('click')
        board[i] = current[0]
        buttons[i].config(text=current[0], state='disabled', font=("Arial", 28, "bold"))
        w = check_winner(board)
        if w:
            if w == 'Draw':
                play_sound('wrong')
                messagebox.showinfo("Result", "It's a draw!")
            else:
                play_sound('correct')
                messagebox.showinfo("Result", f"{w} wins!")
            post_game_prompt(lambda: tictactoe_game(mode), show_home)
            return
        # switch player
        current[0] = 'O' if current[0] == 'X' else 'X'
        # If AI mode and it's AI's turn, let AI play
        if mode == 'ai' and current[0] == 'O':
            root.after(250, ai_move)

    def ai_move():
        # simple AI using minimax
        play_sound('click')
        # If board empty, choose random corner for variety
        if all(b is None for b in board):
            choice = random.choice([0,2,6,8])
        else:
            best = minimax(board[:], 'O')
            choice = best.get('index', None)
            if choice is None:
                # fallback random
                empties = [i for i,b in enumerate(board) if b is None]
                choice = random.choice(empties) if empties else None
        if choice is not None:
            board[choice] = 'O'
            buttons[choice].config(text='O', state='disabled', font=("Arial", 28, "bold"))
        w = check_winner(board)
        if w:
            if w == 'Draw':
                play_sound('wrong')
                messagebox.showinfo("Result", "It's a draw!")
            else:
                play_sound('correct')
                messagebox.showinfo("Result", f"{w} wins!")
            post_game_prompt(lambda: tictactoe_game(mode), show_home)
            return
        current[0] = 'X'

    # create 3x3 grid
    for i in range(9):
        b = tk.Button(board_frame, text='', width=6, height=3,
                      command=lambda i=i: make_move(i))
        b.grid(row=i//3, column=i%3, padx=6, pady=6)
        buttons[i] = b

    tk.Button(root, text="Return Home", width=14,
              font=("Arial", 12), command=show_home).pack(pady=20)


# -----------------------------
# Start App
# -----------------------------
show_home()
root.mainloop()
