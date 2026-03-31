import tkinter as tk
from tkinter import messagebox
import json
import os
import random
import time

# -----------------------------
# STATE DATA
# -----------------------------
# Each state stores:
# - name
# - initials
# - capital
# - row and column for the map grid

STATES = {
    "WA": {"name": "Washington", "initials": "WA", "capital": "Olympia", "row": 0, "column": 0},
    "OR": {"name": "Oregon", "initials": "OR", "capital": "Salem", "row": 1, "column": 0},
    "CA": {"name": "California", "initials": "CA", "capital": "Sacramento", "row": 2, "column": 0},
    "AK": {"name": "Alaska", "initials": "AK", "capital": "Juneau", "row": 7, "column": 0},
    "HI": {"name": "Hawaii", "initials": "HI", "capital": "Honolulu", "row": 7, "column": 2},

    "ID": {"name": "Idaho", "initials": "ID", "capital": "Boise", "row": 1, "column": 1},
    "NV": {"name": "Nevada", "initials": "NV", "capital": "Carson City", "row": 2, "column": 1},
    "AZ": {"name": "Arizona", "initials": "AZ", "capital": "Phoenix", "row": 3, "column": 1},
    "UT": {"name": "Utah", "initials": "UT", "capital": "Salt Lake City", "row": 2, "column": 2},
    "MT": {"name": "Montana", "initials": "MT", "capital": "Helena", "row": 0, "column": 2},
    "WY": {"name": "Wyoming", "initials": "WY", "capital": "Cheyenne", "row": 1, "column": 2},
    "CO": {"name": "Colorado", "initials": "CO", "capital": "Denver", "row": 2, "column": 3},
    "NM": {"name": "New Mexico", "initials": "NM", "capital": "Santa Fe", "row": 3, "column": 2},

    "ND": {"name": "North Dakota", "initials": "ND", "capital": "Bismarck", "row": 0, "column": 3},
    "SD": {"name": "South Dakota", "initials": "SD", "capital": "Pierre", "row": 1, "column": 3},
    "NE": {"name": "Nebraska", "initials": "NE", "capital": "Lincoln", "row": 2, "column": 4},
    "KS": {"name": "Kansas", "initials": "KS", "capital": "Topeka", "row": 3, "column": 4},
    "OK": {"name": "Oklahoma", "initials": "OK", "capital": "Oklahoma City", "row": 4, "column": 4},
    "TX": {"name": "Texas", "initials": "TX", "capital": "Austin", "row": 5, "column": 4},

    "MN": {"name": "Minnesota", "initials": "MN", "capital": "Saint Paul", "row": 0, "column": 4},
    "IA": {"name": "Iowa", "initials": "IA", "capital": "Des Moines", "row": 1, "column": 5},
    "MO": {"name": "Missouri", "initials": "MO", "capital": "Jefferson City", "row": 2, "column": 5},
    "AR": {"name": "Arkansas", "initials": "AR", "capital": "Little Rock", "row": 3, "column": 5},
    "LA": {"name": "Louisiana", "initials": "LA", "capital": "Baton Rouge", "row": 5, "column": 5},

    "WI": {"name": "Wisconsin", "initials": "WI", "capital": "Madison", "row": 0, "column": 5},
    "IL": {"name": "Illinois", "initials": "IL", "capital": "Springfield", "row": 1, "column": 6},
    "MS": {"name": "Mississippi", "initials": "MS", "capital": "Jackson", "row": 4, "column": 6},
    "MI": {"name": "Michigan", "initials": "MI", "capital": "Lansing", "row": 0, "column": 6},
    "IN": {"name": "Indiana", "initials": "IN", "capital": "Indianapolis", "row": 1, "column": 7},
    "KY": {"name": "Kentucky", "initials": "KY", "capital": "Frankfort", "row": 2, "column": 7},
    "TN": {"name": "Tennessee", "initials": "TN", "capital": "Nashville", "row": 3, "column": 7},
    "AL": {"name": "Alabama", "initials": "AL", "capital": "Montgomery", "row": 4, "column": 7},

    "OH": {"name": "Ohio", "initials": "OH", "capital": "Columbus", "row": 1, "column": 8},
    "WV": {"name": "West Virginia", "initials": "WV", "capital": "Charleston", "row": 2, "column": 8},
    "VA": {"name": "Virginia", "initials": "VA", "capital": "Richmond", "row": 3, "column": 8},
    "NC": {"name": "North Carolina", "initials": "NC", "capital": "Raleigh", "row": 4, "column": 8},
    "SC": {"name": "South Carolina", "initials": "SC", "capital": "Columbia", "row": 5, "column": 8},
    "GA": {"name": "Georgia", "initials": "GA", "capital": "Atlanta", "row": 5, "column": 7},
    "FL": {"name": "Florida", "initials": "FL", "capital": "Tallahassee", "row": 6, "column": 8},

    "PA": {"name": "Pennsylvania", "initials": "PA", "capital": "Harrisburg", "row": 1, "column": 9},
    "NY": {"name": "New York", "initials": "NY", "capital": "Albany", "row": 0, "column": 9},
    "VT": {"name": "Vermont", "initials": "VT", "capital": "Montpelier", "row": 0, "column": 10},
    "NH": {"name": "New Hampshire", "initials": "NH", "capital": "Concord", "row": 0, "column": 11},
    "ME": {"name": "Maine", "initials": "ME", "capital": "Augusta", "row": 0, "column": 12},
    "MA": {"name": "Massachusetts", "initials": "MA", "capital": "Boston", "row": 1, "column": 10},
    "CT": {"name": "Connecticut", "initials": "CT", "capital": "Hartford", "row": 1, "column": 11},
    "RI": {"name": "Rhode Island", "initials": "RI", "capital": "Providence", "row": 1, "column": 12},
    "NJ": {"name": "New Jersey", "initials": "NJ", "capital": "Trenton", "row": 2, "column": 9},
    "DE": {"name": "Delaware", "initials": "DE", "capital": "Dover", "row": 2, "column": 10},
    "MD": {"name": "Maryland", "initials": "MD", "capital": "Annapolis", "row": 2, "column": 11},
}

RANKINGS_FILE = "rankings.json"
TIME_LIMIT = 300

# -----------------------------
# RANKINGS FUNCTIONS
# -----------------------------
def load_rankings():
    if os.path.exists(RANKINGS_FILE):
        try:
            with open(RANKINGS_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_rankings(rankings):
    with open(RANKINGS_FILE, "w") as f:
        json.dump(rankings, f, indent=2)

def insert_score(rankings, new_entry):
    rankings.append(new_entry)
    rankings.sort(key=lambda x: (-x["score"], x["elapsed"]))
    return rankings[:10]

# -----------------------------
# MAIN APP
# -----------------------------
class FlashcardApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("US States Flashcards")
        self.geometry("1000x700")
        self.configure(bg="#0d1b2a")

        # Session variables
        self.player_initials = ""
        self.score = 0.0
        self.elapsed = 0
        self.prompt_keys = []
        self.answer_keys = []
        self.deck = []
        self.current_index = 0
        self.current_state = None
        self.answer_widgets = {}
        self.selected_map_answer = None
        self.timer_job = None
        self.start_time = None

        self.show_welcome()

    # -----------------------------
    # GENERAL SCREEN HELPER
    # -----------------------------
    def clear_screen(self):
        for widget in self.winfo_children():
            widget.destroy()

    # -----------------------------
    # WELCOME SCREEN
    # -----------------------------
    def show_welcome(self):
        self.clear_screen()

        tk.Label(
            self, text="US States Flashcards",
            font=("Georgia", 28, "bold"),
            bg="#0d1b2a", fg="#e8a020"
        ).pack(pady=(80, 8))

        tk.Label(
            self, text="Test your knowledge of all 50 states",
            font=("Helvetica", 12),
            bg="#0d1b2a", fg="#8899aa"
        ).pack(pady=(0, 40))

        frame = tk.Frame(self, bg="#162534", padx=40, pady=30)
        frame.pack()

        tk.Label(
            frame, text="Enter your initials (3 letters):",
            font=("Helvetica", 12),
            bg="#162534", fg="white"
        ).pack(anchor="w")

        self.initials_var = tk.StringVar()
        entry = tk.Entry(
            frame,
            textvariable=self.initials_var,
            font=("Courier", 14, "bold"),
            width=6,
            bg="#1b2e42",
            fg="#e8a020",
            insertbackground="#e8a020",
            relief="flat",
            bd=4
        )
        entry.pack(anchor="w", pady=(6, 20))
        entry.focus()

        tk.Button(
            frame, text="Continue to Settings",
            font=("Helvetica", 12),
            bg="#e8a020", fg="#0d1b2a",
            relief="flat",
            padx=16, pady=8,
            command=self.validate_initials
        ).pack()

        self.bind("<Return>", lambda event: self.validate_initials())

    def validate_initials(self):
        initials = self.initials_var.get().strip().upper()
        if len(initials) == 3 and initials.isalpha():
            self.player_initials = initials
            self.show_settings()
        else:
            messagebox.showerror(
                "Invalid Initials",
                "Please enter exactly 3 letters for your initials."
            )

    # -----------------------------
    # SETTINGS SCREEN
    # -----------------------------
    def show_settings(self):
        self.clear_screen()

        tk.Label(
            self, text="Settings",
            font=("Georgia", 24, "bold"),
            bg="#0d1b2a", fg="#e8a020"
        ).pack(pady=(30, 4))

        tk.Label(
            self, text=f"Player: {self.player_initials}",
            font=("Helvetica", 12),
            bg="#0d1b2a", fg="#3ec9a7"
        ).pack(pady=(0, 16))

        # SHOW options
        show_frame = tk.LabelFrame(
            self, text=" What to SHOW on each card ",
            font=("Helvetica", 11),
            bg="#1b2e42", fg="#e8a020",
            padx=16, pady=10
        )
        show_frame.pack(fill="x", padx=60, pady=6)

        self.show_map = tk.BooleanVar()
        self.show_name = tk.BooleanVar()
        self.show_initials = tk.BooleanVar()
        self.show_capital = tk.BooleanVar()

        for label, var in [
            ("Map Location", self.show_map),
            ("State Name", self.show_name),
            ("Initials", self.show_initials),
            ("Capital City", self.show_capital)
        ]:
            tk.Checkbutton(
                show_frame,
                text=label,
                variable=var,
                font=("Helvetica", 11),
                bg="#1b2e42", fg="white",
                selectcolor="#0d1b2a",
                activebackground="#1b2e42"
            ).pack(anchor="w")

        # ANSWER options
        ans_frame = tk.LabelFrame(
            self, text=" What the USER ANSWERS ",
            font=("Helvetica", 11),
            bg="#1b2e42", fg="#e8a020",
            padx=16, pady=10
        )
        ans_frame.pack(fill="x", padx=60, pady=6)

        self.ans_map = tk.BooleanVar()
        self.ans_name = tk.BooleanVar()
        self.ans_initials = tk.BooleanVar()
        self.ans_capital = tk.BooleanVar()

        for label, var in [
            ("Map Location", self.ans_map),
            ("State Name", self.ans_name),
            ("Initials", self.ans_initials),
            ("Capital City", self.ans_capital)
        ]:
            tk.Checkbutton(
                ans_frame,
                text=label,
                variable=var,
                font=("Helvetica", 11),
                bg="#1b2e42", fg="white",
                selectcolor="#0d1b2a",
                activebackground="#1b2e42"
            ).pack(anchor="w")

        # Answer mode
        mode_frame = tk.LabelFrame(
            self, text=" Answer Mode ",
            font=("Helvetica", 11),
            bg="#1b2e42", fg="#e8a020",
            padx=16, pady=10
        )
        mode_frame.pack(fill="x", padx=60, pady=6)

        self.answer_mode = tk.StringVar(value="dropdown")

        tk.Radiobutton(
            mode_frame,
            text="Drop-down menus (1/6 point each)",
            variable=self.answer_mode,
            value="dropdown",
            font=("Helvetica", 11),
            bg="#1b2e42", fg="white",
            selectcolor="#0d1b2a",
            activebackground="#1b2e42"
        ).pack(anchor="w")

        tk.Radiobutton(
            mode_frame,
            text="Text entry (2/6 point each)",
            variable=self.answer_mode,
            value="text",
            font=("Helvetica", 11),
            bg="#1b2e42", fg="white",
            selectcolor="#0d1b2a",
            activebackground="#1b2e42"
        ).pack(anchor="w")

        tk.Button(
            self, text="Start Flashcards",
            font=("Helvetica", 13, "bold"),
            bg="#e8a020", fg="#0d1b2a",
            relief="flat", padx=20, pady=10,
            command=self.validate_settings
        ).pack(pady=16)

        tk.Button(
            self, text="View Rankings",
            font=("Helvetica", 10),
            bg="#1b2e42", fg="white",
            relief="flat",
            command=self.show_rankings
        ).pack(pady=4)

        tk.Button(
            self, text="Back to Welcome",
            font=("Helvetica", 10),
            bg="#1b2e42", fg="white",
            relief="flat",
            command=self.show_welcome
        ).pack()

    def validate_settings(self):
        prompt_keys = []
        answer_keys = []

        if self.show_map.get():
            prompt_keys.append("map")
        if self.show_name.get():
            prompt_keys.append("name")
        if self.show_initials.get():
            prompt_keys.append("initials")
        if self.show_capital.get():
            prompt_keys.append("capital")

        if self.ans_map.get():
            answer_keys.append("map")
        if self.ans_name.get():
            answer_keys.append("name")
        if self.ans_initials.get():
            answer_keys.append("initials")
        if self.ans_capital.get():
            answer_keys.append("capital")

        if len(prompt_keys) == 0:
            messagebox.showwarning("Settings", "Select at least 1 item to SHOW.")
            return
        if len(prompt_keys) > 3:
            messagebox.showwarning("Settings", "Select at most 3 items to SHOW.")
            return
        if len(answer_keys) == 0:
            messagebox.showwarning("Settings", "Select at least 1 item to ANSWER.")
            return
        if len(answer_keys) > 3:
            messagebox.showwarning("Settings", "Select at most 3 items to ANSWER.")
            return

        overlap = set(prompt_keys) & set(answer_keys)
        if overlap:
            messagebox.showwarning(
                "Settings",
                "Shown and answered items cannot overlap."
            )
            return

        self.prompt_keys = prompt_keys
        self.answer_keys = answer_keys
        self.start_session()

    # -----------------------------
    # SESSION SETUP
    # -----------------------------
    def start_session(self):
        self.score = 0.0
        self.elapsed = 0
        self.current_index = 0
        self.selected_map_answer = None

        # Copy all state codes and shuffle them
        self.deck = list(STATES.keys())
        random.shuffle(self.deck)

        self.start_time = time.time()

        if self.timer_job:
            self.after_cancel(self.timer_job)

        self.show_flashcard()
        self.update_timer()

    # -----------------------------
    # TIMER
    # -----------------------------
    def update_timer(self):
        self.elapsed = int(time.time() - self.start_time)

        if hasattr(self, "timer_label"):
            time_left = TIME_LIMIT - self.elapsed
            if time_left < 0:
                time_left = 0
            self.timer_label.config(text=f"Time Left: {time_left}s")

        if self.elapsed >= TIME_LIMIT:
            self.finish_session()
            return

        self.timer_job = self.after(1000, self.update_timer)

    # -----------------------------
    # FLASHCARD SCREEN
    # -----------------------------
    def show_flashcard(self):
        self.clear_screen()
        self.answer_widgets = {}
        self.selected_map_answer = None

        # Stop if all cards are done
        if self.current_index >= len(self.deck):
            self.finish_session()
            return

        current_code = self.deck[self.current_index]
        self.current_state = STATES[current_code]

        top_frame = tk.Frame(self, bg="#0d1b2a")
        top_frame.pack(pady=10)

        tk.Label(
            top_frame,
            text=f"Flashcard {self.current_index + 1} / {len(self.deck)}",
            font=("Helvetica", 13, "bold"),
            bg="#0d1b2a", fg="white"
        ).grid(row=0, column=0, padx=15)

        tk.Label(
            top_frame,
            text=f"Score: {self.score:.2f}",
            font=("Helvetica", 13, "bold"),
            bg="#0d1b2a", fg="#3ec9a7"
        ).grid(row=0, column=1, padx=15)

        self.timer_label = tk.Label(
            top_frame,
            text=f"Time Left: {TIME_LIMIT - self.elapsed}s",
            font=("Helvetica", 13, "bold"),
            bg="#0d1b2a", fg="#e8a020"
        )
        self.timer_label.grid(row=0, column=2, padx=15)

        main_frame = tk.Frame(self, bg="#0d1b2a")
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)

        left_frame = tk.Frame(main_frame, bg="#162534", padx=15, pady=15)
        left_frame.pack(side="left", fill="both", expand=True, padx=10)

        right_frame = tk.Frame(main_frame, bg="#162534", padx=15, pady=15)
        right_frame.pack(side="right", fill="both", expand=True, padx=10)

        tk.Label(
            left_frame,
            text="Flashcard Prompt",
            font=("Georgia", 18, "bold"),
            bg="#162534", fg="#e8a020"
        ).pack(pady=(0, 12))

        # Show selected prompt items
        if "map" in self.prompt_keys or "map" in self.answer_keys:
            self.canvas = tk.Canvas(
                left_frame,
                width=700,
                height=350,
                bg="white",
                highlightthickness=0
            )
            self.canvas.pack(pady=10)

            self.draw_map(
                highlight_code=current_code if "map" in self.prompt_keys else None
            )

            if "map" in self.answer_keys:
                self.canvas.bind("<Button-1>", self.map_click)

        if "name" in self.prompt_keys:
            tk.Label(
                left_frame,
                text=f"State Name: {self.current_state['name']}",
                font=("Helvetica", 13),
                bg="#162534", fg="white"
            ).pack(pady=6)

        if "initials" in self.prompt_keys:
            tk.Label(
                left_frame,
                text=f"Initials: {self.current_state['initials']}",
                font=("Helvetica", 13),
                bg="#162534", fg="white"
            ).pack(pady=6)

        if "capital" in self.prompt_keys:
            tk.Label(
                left_frame,
                text=f"Capital: {self.current_state['capital']}",
                font=("Helvetica", 13),
                bg="#162534", fg="white"
            ).pack(pady=6)

        tk.Label(
            right_frame,
            text="Your Answer",
            font=("Georgia", 18, "bold"),
            bg="#162534", fg="#e8a020"
        ).pack(pady=(0, 12))

        # Create answer widgets
        for key in self.answer_keys:
            if key == "map":
                tk.Label(
                    right_frame,
                    text="Click the correct state on the map.",
                    font=("Helvetica", 12),
                    bg="#162534", fg="white"
                ).pack(pady=6)
                continue

            tk.Label(
                right_frame,
                text=key.capitalize(),
                font=("Helvetica", 12, "bold"),
                bg="#162534", fg="white"
            ).pack(pady=(10, 4))

            if self.answer_mode.get() == "text":
                entry = tk.Entry(
                    right_frame,
                    font=("Helvetica", 12),
                    width=25
                )
                entry.pack(pady=4)
                self.answer_widgets[key] = entry
            else:
                choices = self.make_choices(key, current_code)
                var = tk.StringVar(value=choices[0])

                menu = tk.OptionMenu(right_frame, var, *choices)
                menu.config(font=("Helvetica", 11), width=22)
                menu.pack(pady=4)

                self.answer_widgets[key] = var

        button_frame = tk.Frame(self, bg="#0d1b2a")
        button_frame.pack(pady=12)

        tk.Button(
            button_frame,
            text="Submit Answer",
            font=("Helvetica", 12, "bold"),
            bg="#e8a020", fg="#0d1b2a",
            relief="flat",
            padx=18, pady=8,
            command=self.check_answer
        ).pack(side="left", padx=8)

        tk.Button(
            button_frame,
            text="End Session",
            font=("Helvetica", 12),
            bg="#1b2e42", fg="white",
            relief="flat",
            padx=18, pady=8,
            command=self.finish_session
        ).pack(side="left", padx=8)

    # -----------------------------
    # DRAW MAP
    # -----------------------------
    def draw_map(self, highlight_code=None, selected_code=None):
        self.canvas.delete("all")

        tile_size = 40
        gap = 4
        left_margin = 40
        top_margin = 20

        self.state_boxes = {}

        for code, info in STATES.items():
            row = info["row"]
            column = info["column"]

            x1 = left_margin + column * (tile_size + gap)
            y1 = top_margin + row * (tile_size + gap)
            x2 = x1 + tile_size
            y2 = y1 + tile_size

            fill_color = "#8ecae6"
            outline_color = "#3a506b"

            if code == highlight_code:
                fill_color = "#ffb703"
                outline_color = "#d97706"

            if code == selected_code:
                fill_color = "#90be6d"
                outline_color = "#2d6a4f"

            rect_id = self.canvas.create_rectangle(
                x1, y1, x2, y2,
                fill=fill_color,
                outline=outline_color,
                width=2
            )

            self.canvas.create_text(
                (x1 + x2) / 2,
                (y1 + y2) / 2,
                text=code,
                font=("Arial", 9, "bold")
            )

            self.state_boxes[rect_id] = code

    def map_click(self, event):
        clicked_items = self.canvas.find_overlapping(event.x, event.y, event.x, event.y)

        for item in clicked_items:
            if item in self.state_boxes:
                self.selected_map_answer = self.state_boxes[item]
                self.draw_map(
                    highlight_code=self.deck[self.current_index] if "map" in self.prompt_keys else None,
                    selected_code=self.selected_map_answer
                )
                break


    # CHOICES FOR DROPDOWN
    def make_choices(self, key, current_code):
        correct_state = STATES[current_code]

        if key == "name":
            correct_answer = correct_state["name"]
            all_answers = [STATES[code]["name"] for code in STATES]
        elif key == "initials":
            correct_answer = correct_state["initials"]
            all_answers = [STATES[code]["initials"] for code in STATES]
        else:  # capital
            correct_answer = correct_state["capital"]
            all_answers = [STATES[code]["capital"] for code in STATES]

        wrong_answers = [answer for answer in all_answers if answer != correct_answer]
        choices = random.sample(wrong_answers, 3)
        choices.append(correct_answer)
        random.shuffle(choices)
        return choices

    # -----------------------------
    # CHECK ANSWER
    # -----------------------------
    def check_answer(self):
        current_code = self.deck[self.current_index]
        current_state = STATES[current_code]

        for key in self.answer_keys:
            if key == "map":
                if self.selected_map_answer == current_code:
                    self.score += 1 / 6
                continue

            # Get user's answer
            if self.answer_mode.get() == "text":
                user_answer = self.answer_widgets[key].get().strip()
                points = 2 / 6
            else:
                user_answer = self.answer_widgets[key].get().strip()
                points = 1 / 6

            # Get correct answer
            if key == "name":
                correct_answer = current_state["name"]
            elif key == "initials":
                correct_answer = current_state["initials"]
            else:
                correct_answer = current_state["capital"]

            if user_answer.lower() == correct_answer.lower():
                self.score += points

        self.current_index += 1
        self.show_flashcard()

    # -----------------------------
    # FINISH SESSION
    # -----------------------------
    def finish_session(self):
        if self.timer_job:
            self.after_cancel(self.timer_job)
            self.timer_job = None

        if self.start_time:
            self.elapsed = int(time.time() - self.start_time)

        rankings = load_rankings()
        new_entry = {
            "initials": self.player_initials,
            "elapsed": self.elapsed,
            "score": round(self.score, 2)
        }
        rankings = insert_score(rankings, new_entry)
        save_rankings(rankings)

        self.show_rankings()

    # -----------------------------
    # RANKINGS SCREEN
    # -----------------------------
    def show_rankings(self):
        self.clear_screen()

        tk.Label(
            self, text="Top 10 Rankings",
            font=("Georgia", 24, "bold"),
            bg="#0d1b2a", fg="#e8a020"
        ).pack(pady=(30, 10))

        rankings = load_rankings()

        table_frame = tk.Frame(self, bg="#162534", padx=20, pady=20)
        table_frame.pack(pady=10)

        headers = ["Rank", "Initials", "Time", "Score"]
        for col, header in enumerate(headers):
            tk.Label(
                table_frame,
                text=header,
                font=("Helvetica", 12, "bold"),
                bg="#162534", fg="#3ec9a7",
                width=12
            ).grid(row=0, column=col, padx=4, pady=4)

        for i, entry in enumerate(rankings, start=1):
            tk.Label(
                table_frame, text=str(i),
                font=("Helvetica", 11),
                bg="#162534", fg="white",
                width=12
            ).grid(row=i, column=0, padx=4, pady=4)

            tk.Label(
                table_frame, text=entry["initials"],
                font=("Helvetica", 11),
                bg="#162534", fg="white",
                width=12
            ).grid(row=i, column=1, padx=4, pady=4)

            tk.Label(
                table_frame, text=f"{entry['elapsed']} s",
                font=("Helvetica", 11),
                bg="#162534", fg="white",
                width=12
            ).grid(row=i, column=2, padx=4, pady=4)

            tk.Label(
                table_frame, text=str(entry["score"]),
                font=("Helvetica", 11),
                bg="#162534", fg="white",
                width=12
            ).grid(row=i, column=3, padx=4, pady=4)

        tk.Button(
            self, text="Back to Welcome",
            font=("Helvetica", 11),
            bg="#e8a020", fg="#0d1b2a",
            relief="flat",
            padx=16, pady=8,
            command=self.show_welcome
        ).pack(pady=8)

        tk.Button(
            self, text="Go to Settings",
            font=("Helvetica", 11),
            bg="#1b2e42", fg="white",
            relief="flat",
            padx=16, pady=8,
            command=self.show_settings
        ).pack(pady=4)

# -----------------------------
# RUN APP
# -----------------------------
app = FlashcardApp()
app.mainloop()
