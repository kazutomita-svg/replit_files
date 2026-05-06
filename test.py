import tkinter as tk
from tkinter import ttk, messagebox
import random

class RoboticsToolkit:
    def __init__(self, root):
        self.root = root
        self.root.title("JackBord Toolkit v8.0 - Mastery Quiz")
        self.root.geometry("600x700")

        # 1. Setup Notebook
        self.notebook = ttk.Notebook(root)
        self.tab_power = ttk.Frame(self.notebook)
        self.tab_units = ttk.Frame(self.notebook)
        self.tab_resistors = ttk.Frame(self.notebook)
        self.tab_quiz = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_power, text="Power")
        self.notebook.add(self.tab_units, text="Units")
        self.notebook.add(self.tab_resistors, text="Resistors")
        self.notebook.add(self.tab_quiz, text="Quiz")
        self.notebook.pack(expand=1, fill="both")

        # Initialize existing modules (Assuming logic from V7)
        self.setup_power_logic_ui()
        self.setup_units_ui()
        self.setup_resistor_ui()
        
        # 2. Quiz Data and Variables
        self.quiz_questions = [
            {"q": "What is the formula for Power?", "o": ["P = I/V", "P = IV", "P = V/I", "P = I+V"], "a": "P = IV"},
            {"q": "What is the limit for current on a JackBord pin?", "o": ["100mA", "500mA", "1A", "5A"], "a": "500mA"},
            {"q": "How many Ohms is 1.5kΩ?", "o": ["150", "1500", "15000", "1.5"], "a": "1500"},
            {"q": "Which prefix represents 10^-6?", "o": ["Milli (m)", "Kilo (k)", "Micro (μ)", "Mega (M)"], "a": "Micro (μ)"},
            {"q": "A resistor with Brown, Black, Red bands is how many Ohms?", "o": ["100Ω", "1kΩ", "10kΩ", "110Ω"], "a": "1kΩ"},
            {"q": "What color represents a '2' in the digit bands?", "o": ["Red", "Orange", "Brown", "Black"], "a": "Red"},
            {"q": "If Voltage is 10V and Current is 0.2A, what is the Power?", "o": ["2W", "50W", "0.02W", "20W"], "a": "2W"},
            {"q": "What does a Gold tolerance band mean?", "o": ["±1%", "±5%", "±10%", "±2%"], "a": "±5%"},
            {"q": "Convert 5,000,000Ω to Mega-Ohms.", "o": ["50MΩ", "0.5MΩ", "5MΩ", "500MΩ"], "a": "5MΩ"},
            {"q": "Which current is safer for the JackBord?", "o": ["600mA", "200mA", "1.2A", "0.8A"], "a": "200mA"}
        ]
        
        self.current_q_index = 0
        self.score = 0
        self.setup_quiz_ui()

    def setup_quiz_ui(self):
        # Header
        tk.Label(self.tab_quiz, text="Mastery Quiz: Electronics Basics", 
                 font=("Arial", 14, "bold")).pack(pady=10)
        
        # Question Display Area
        self.quiz_frame = ttk.LabelFrame(self.tab_quiz, text=" Question ")
        self.quiz_frame.pack(padx=20, pady=10, fill="both", expand=True)

        self.q_label = tk.Label(self.quiz_frame, text="Click 'Start Quiz' to begin!", 
                                font=("Arial", 11), wraplength=450)
        self.q_label.pack(pady=20)

        # Answer Buttons Container
        self.ans_frame = tk.Frame(self.quiz_frame)
        self.ans_frame.pack(pady=10)
        
        self.ans_buttons = []
        for i in range(4):
            btn = tk.Button(self.ans_frame, text="", width=30, 
                            command=lambda i=i: self.check_answer(i))
            btn.pack(pady=5)
            self.ans_buttons.append(btn)
            btn.config(state="disabled")

        # Control/Status
        self.start_btn = tk.Button(self.tab_quiz, text="Start Quiz", command=self.start_quiz)
        self.start_btn.pack(pady=10)
        
        self.progress_label = tk.Label(self.tab_quiz, text="Score: 0/10")
        self.progress_label.pack()

    def start_quiz(self):
        self.current_q_index = 0
        self.score = 0
        self.start_btn.config(state="disabled")
        for btn in self.ans_buttons:
            btn.config(state="normal")
        self.show_question()

    def show_question(self):
        if self.current_q_index < len(self.quiz_questions):
            q_data = self.quiz_questions[self.current_q_index]
            self.q_label.config(text=f"Q{self.current_q_index + 1}: {q_data['q']}")
            
            # Shuffle options for variety
            options = list(q_data['o'])
            random.shuffle(options)
            
            for i, opt in enumerate(options):
                self.ans_buttons[i].config(text=opt)
            
            self.progress_label.config(text=f"Question {self.current_q_index + 1} of 10 | Score: {self.score}")
        else:
            self.end_quiz()

    def check_answer(self, btn_idx):
        selected = self.ans_buttons[btn_idx].cget("text")
        correct = self.quiz_questions[self.current_q_index]['a']
        
        if selected == correct:
            self.score += 1
            
        self.current_q_index += 1
        self.show_question()

    def end_quiz(self):
        pass_mark = 7 # 70% of 10 questions
        percent = (self.score / 10) * 100
        
        if self.score >= pass_mark:
            msg = f"PASS! You scored {percent}%\nYou are ready to use the JackBord."
            color = "green"
        else:
            msg = f"FAIL. You scored {percent}%\nYou need at least 70% to pass. Please review the tabs and try again."
            color = "red"
            
        self.q_label.config(text=msg, fg=color, font=("Arial", 12, "bold"))
        for btn in self.ans_buttons:
            btn.config(text="", state="disabled")
        self.start_btn.config(state="normal", text="Retake Quiz")

    # (Existing setup_power_logic_ui, setup_units_ui, setup_resistor_ui would go here)
    