import tkinter as tk
from tkinter import messagebox
import json
import os

# Create State Dictionary
STATES = [
    {"name": "Alabama",        "initials": "AL", "capital": "Montgomery"},
    {"name": "Alaska",         "initials": "AK", "capital": "Juneau"},
    {"name": "Arizona",        "initials": "AZ", "capital": "Phoenix"},
    {"name": "Arkansas",       "initials": "AR", "capital": "Little Rock"},
    {"name": "California",     "initials": "CA", "capital": "Sacramento"},
    {"name": "Colorado",       "initials": "CO", "capital": "Denver"},
    {"name": "Connecticut",    "initials": "CT", "capital": "Hartford"},
    {"name": "Delaware",       "initials": "DE", "capital": "Dover"},
    {"name": "Florida",        "initials": "FL", "capital": "Tallahassee"},
    {"name": "Georgia",        "initials": "GA", "capital": "Atlanta"},
    {"name": "Hawaii",         "initials": "HI", "capital": "Honolulu"},
    {"name": "Idaho",          "initials": "ID", "capital": "Boise"},
    {"name": "Illinois",       "initials": "IL", "capital": "Springfield"},
    {"name": "Indiana",        "initials": "IN", "capital": "Indianapolis"},
    {"name": "Iowa",           "initials": "IA", "capital": "Des Moines"},
    {"name": "Kansas",         "initials": "KS", "capital": "Topeka"},
    {"name": "Kentucky",       "initials": "KY", "capital": "Frankfort"},
    {"name": "Louisiana",      "initials": "LA", "capital": "Baton Rouge"},
    {"name": "Maine",          "initials": "ME", "capital": "Augusta"},
    {"name": "Maryland",       "initials": "MD", "capital": "Annapolis"},
    {"name": "Massachusetts",  "initials": "MA", "capital": "Boston"},
    {"name": "Michigan",       "initials": "MI", "capital": "Lansing"},
    {"name": "Minnesota",      "initials": "MN", "capital": "Saint Paul"},
    {"name": "Mississippi",    "initials": "MS", "capital": "Jackson"},
    {"name": "Missouri",       "initials": "MO", "capital": "Jefferson City"},
    {"name": "Montana",        "initials": "MT", "capital": "Helena"},
    {"name": "Nebraska",       "initials": "NE", "capital": "Lincoln"},
    {"name": "Nevada",         "initials": "NV", "capital": "Carson City"},
    {"name": "New Hampshire",  "initials": "NH", "capital": "Concord"},
    {"name": "New Jersey",     "initials": "NJ", "capital": "Trenton"},
    {"name": "New Mexico",     "initials": "NM", "capital": "Santa Fe"},
    {"name": "New York",       "initials": "NY", "capital": "Albany"},
    {"name": "North Carolina", "initials": "NC", "capital": "Raleigh"},
    {"name": "North Dakota",   "initials": "ND", "capital": "Bismarck"},
    {"name": "Ohio",           "initials": "OH", "capital": "Columbus"},
    {"name": "Oklahoma",       "initials": "OK", "capital": "Oklahoma City"},
    {"name": "Oregon",         "initials": "OR", "capital": "Salem"},
    {"name": "Pennsylvania",   "initials": "PA", "capital": "Harrisburg"},
    {"name": "Rhode Island",   "initials": "RI", "capital": "Providence"},
    {"name": "South Carolina", "initials": "SC", "capital": "Columbia"},
    {"name": "South Dakota",   "initials": "SD", "capital": "Pierre"},
    {"name": "Tennessee",      "initials": "TN", "capital": "Nashville"},
    {"name": "Texas",          "initials": "TX", "capital": "Austin"},
    {"name": "Utah",           "initials": "UT", "capital": "Salt Lake City"},
    {"name": "Vermont",        "initials": "VT", "capital": "Montpelier"},
    {"name": "Virginia",       "initials": "VA", "capital": "Richmond"},
    {"name": "Washington",     "initials": "WA", "capital": "Olympia"},
    {"name": "West Virginia",  "initials": "WV", "capital": "Charleston"},
    {"name": "Wisconsin",      "initials": "WI", "capital": "Madison"},
    {"name": "Wyoming",        "initials": "WY", "capital": "Cheyenne"},
]

RANKINGS_FILE = "rankings.json"
TIME_LIMIT = 300


# Creates a JSON rankings file
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




# The actual Flashcard App
class FlashcardApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("US States Flashcards")
        self.geometry("800x600")
        self.configure(bg="#0d1b2a")

        self.player_initials = ""
        self.score = 0.0
        self.elapsed = 0
        self.prompt_keys = []
        self.answer_keys = []
        elf.deck = []
        self.current_index = 0
        self.current_state = None
        self.answer_widgets = {}
        self.selected_map_answer = None
        self.timer_job = None
        self.start_time = None

        self.show_welcome()
        
    #General Screen Helper
    def clear_screen(self):
        for widget in self.winfo_children():
            widget.destroy()
            
    #Welcome Screen
    def show_welcome(self):
        self.clear_screen()

        tk.Label(self, text="US States Flashcards",
                 font=("Georgia", 28, "bold"),
                 bg="#0d1b2a", fg="red").pack(pady=(80, 8))

        tk.Label(self, text="Test your knowledge of all 50 states",
                 font=("Helvetica", 12),
                 bg="#0d1b2a", fg="#8899aa").pack(pady=(0, 40))

        frame = tk.Frame(self, bg="#162534", padx=40, pady=30)
        frame.pack()

        tk.Label(frame, text="Enter your initials (1-3 characters):",
                 font=("Helvetica", 12),
                 bg="#162534", fg="white").pack(anchor="w")

        self.initials_var = tk.StringVar()
        entry = tk.Entry(frame, textvariable=self.initials_var,
                         font=("Courier", 14, "bold"),
                         width=6, bg="#1b2e42", fg="red",
                         insertbackground="red", relief="flat", bd=4)
        entry.pack(anchor="w", pady=(6, 20))
        entry.focus()

        tk.Button(frame, text="Continue to Settings",
                  font=("Helvetica", 12),
                  bg="red", fg="#0d1b2a", relief="flat",
                  padx=16, pady=8,
                  command=self.validate_initials).pack()

        self.bind("<Return>", lambda event: self.validate_initials())

    def validate_initials(self):
        initials = self.initials_var.get().strip().upper()
        if 1 <= len(initials) <= 3 and initials.isalpha():
            self.player_initials = initials
            self.show_settings()
        else:
            messagebox.showerror("Invalid Initials",
                                 "Please enter 1 to 3 letters for your initials.")

    #Settings Screen
    def show_settings(self):
        self.clear_screen()

        tk.Label(self, text="Settings",
                 font=("Georgia", 24, "bold"),
                 bg="#0d1b2a", fg="red").pack(pady=(30, 4))

        tk.Label(self, text=f"Player: {self.player_initials}",
                 font=("Helvetica", 12),
                 bg="#0d1b2a", fg="white").pack(pady=(0, 16))

        show_frame = tk.LabelFrame(self, text=" What to SHOW on each card ",
                                   font=("Helvetica", 11), bg="#1b2e42",
                                   fg="red", padx=16, pady=10)
        show_frame.pack(fill="x", padx=60, pady=6)

        self.show_map = tk.BooleanVar()
        self.show_name = tk.BooleanVar()
        self.show_initials = tk.BooleanVar()
        self.show_capital = tk.BooleanVar()

        for label, var in [("Map Location", self.show_map),
                           ("State Name",   self.show_name),
                           ("Initials",     self.show_initials),
                           ("Capital City", self.show_capital)]:
            tk.Checkbutton(show_frame, text=label, variable=var,
                           font=("Helvetica", 11), bg="#1b2e42",
                           fg="white", selectcolor="#0d1b2a",
                           activebackground="#1b2e42").pack(anchor="w")

        ans_frame = tk.LabelFrame(self, text=" What the USER ANSWERS ",
                                  font=("Helvetica", 11), bg="#1b2e42",
                                  fg="red", padx=16, pady=10)
        ans_frame.pack(fill="x", padx=60, pady=6)

        self.ans_map = tk.BooleanVar()
        self.ans_name = tk.BooleanVar()
        self.ans_initials = tk.BooleanVar()
        self.ans_capital = tk.BooleanVar()

        for label, var in [("Map Location", self.ans_map),
                           ("State Name",   self.ans_name),
                           ("Initials",     self.ans_initials),
                           ("Capital City", self.ans_capital)]:
            tk.Checkbutton(ans_frame, text=label, variable=var,
                           font=("Helvetica", 11), bg="#1b2e42",
                           fg="white", selectcolor="#0d1b2a",
                           activebackground="#1b2e42").pack(anchor="w")

        mode_frame = tk.LabelFrame(self, text=" Answer Mode ",
                                   font=("Helvetica", 11), bg="#1b2e42",
                                   fg="red", padx=16, pady=10)
        mode_frame.pack(fill="x", padx=60, pady=6)

        self.answer_mode = tk.StringVar(value="dropdown")
        tk.Radiobutton(mode_frame, text="Drop-down menus (1/6 point each)",
                       variable=self.answer_mode, value="dropdown",
                       font=("Helvetica", 11), bg="#1b2e42", fg="white",
                       selectcolor="#0d1b2a",
                       activebackground="#1b2e42").pack(anchor="w")
        tk.Radiobutton(mode_frame, text="Text entry (2/6 point each)",
                       variable=self.answer_mode, value="text",
                       font=("Helvetica", 11), bg="#1b2e42", fg="white",
                       selectcolor="#0d1b2a",
                       activebackground="#1b2e42").pack(anchor="w")

        tk.Button(self, text="Start Flashcards",
                  font=("Helvetica", 13, "bold"),
                  bg="red", fg="#0d1b2a", relief="flat",
                  padx=20, pady=10,
                  command=self.validate_settings).pack(pady=16)

        tk.Button(self, text="Back to Welcome",
                  font=("Helvetica", 10, "bold"),
                  bg="#1b2e42", fg="black", relief="flat",
                  command=self.show_welcome).pack()

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
            messagebox.showwarning(
                "Settings", "Select at least 1 item to SHOW.")
            return
        if len(prompt_keys) > 3:
            messagebox.showwarning(
                "Settings", "Select at most 3 items to SHOW.")
            return
        if len(answer_keys) == 0:
            messagebox.showwarning(
                "Settings", "Select at least 1 item to ANSWER.")
            return
        if len(answer_keys) > 3:
            messagebox.showwarning(
                "Settings", "Select at most 3 items to ANSWER.")
            return

        overlap = set(prompt_keys) & set(answer_keys)
        if overlap:
            messagebox.showwarning("Settings",
                                   "Shown and answered items cannot overlap.")
            return

        self.prompt_keys = prompt_keys
        self.answer_keys = answer_keys
        self.show_flashcard()

    def show_flashcard(self):
        self.clear_screen()
        tk.Label(self, text="Flashcard Screen",
                 font=("Georgia", 20), bg="#0d1b2a", fg="white").pack(pady=40)
        tk.Button(self, text="End Session",
                  command=self.show_rankings).pack(pady=4)

    def show_rankings(self):
        self.clear_screen()
        tk.Label(self, text="Rankings Screen",
                 font=("Georgia", 20), bg="#0d1b2a", fg="white").pack(pady=40)
        tk.Button(self, text="Back to Welcome",
                  command=self.show_welcome).pack(pady=4)
        tk.Button(self, text="Settings",
                  command=self.show_settings).pack(pady=4)


app = FlashcardApp()
app.mainloop()
