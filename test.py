import tkinter as tk
from tkinter import ttk, messagebox
import random
from datetime import datetime
import os

class RoboticsToolkit:
    def __init__(self, root):
        self.root = root
        self.root.title("JackBord Toolkit Version 9 - File I/O & History")
        self.root.geometry("600x850") # Increased height for history log

        # Tab Controller
        self.notebook = ttk.Notebook(root)
        self.tab_power = ttk.Frame(self.notebook)
        self.tab_units = ttk.Frame(self.notebook)
        self.tab_resistors = ttk.Frame(self.notebook)
        self.tab_quiz = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_power, text="Power")
        self.notebook.add(self.tab_units, text="Units")
        self.notebook.add(self.tab_resistors, text="Resistors")
        self.notebook.add(self.tab_quiz, text="Quiz & History") # Renamed for clarity
        self.notebook.pack(expand=1, fill="both")

        # Initialize existing modules
        self.setup_power_logic_ui()
        self.setup_units_ui()

        # Color data for resistor calculations
        self.colors = {
            "Black": 0, "Brown": 1, "Red": 2, "Orange": 3, "Yellow": 4,
            "Green": 5, "Blue": 6, "Violet": 7, "Gray": 8, "White": 9
        }
        self.multipliers = {
            "Black": 1, "Brown": 10, "Red": 100, "Orange": 1000, "Yellow": 10000,
            "Green": 100000, "Blue": 1000000
        }
        self.tolerances = {
            "Brown": 1, "Red": 2, "Gold": 5, "Silver": 10
        }

        self.setup_resistor_ui()

        # Quiz Data and Variables
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

    # --- Power, Units, and Resistor Methods remain identical to your code ---
    def setup_power_logic_ui(self):
        power_box = ttk.LabelFrame(self.tab_power, text=" Power Calculator (P = IV) ")
        power_box.pack(padx=20, pady=20, fill="x")
        tk.Label(power_box, text="Voltage (V):").grid(row=0, column=0, padx=10, pady=10)
        self.voltage_entry = tk.Entry(power_box)
        self.voltage_entry.grid(row=0, column=1, padx=10, pady=10)
        tk.Label(power_box, text="Current:").grid(row=1, column=0, padx=10, pady=10)
        self.current_entry = tk.Entry(power_box)
        self.current_entry.grid(row=1, column=1, padx=10, pady=10)
        self.unit_var = tk.StringVar(value="mA")
        self.unit_dropdown = ttk.Combobox(power_box, textvariable=self.unit_var, width=5, state="readonly")
        self.unit_dropdown['values'] = ("mA", "A")
        self.unit_dropdown.grid(row=1, column=2, padx=5)
        self.calc_button = tk.Button(power_box, text="Calculate & Check Safety", command=self.calculate_power)
        self.calc_button.grid(row=2, column=0, columnspan=3, pady=15)
        self.result_label = tk.Label(self.tab_power, text="Enter values and click calculate.", wraplength=400, font=("Arial", 11))
        self.result_label.pack(pady=20)

    def calculate_power(self):
        try:
            v = float(self.voltage_entry.get())
            raw_i = float(self.current_entry.get())
            unit = self.unit_var.get()
            if unit == "mA":
                i_amps, i_ma = raw_i / 1000, raw_i
            else:
                i_amps, i_ma = raw_i, raw_i * 1000
            p_watts = v * i_amps
            if i_ma > 500:
                self.result_label.config(text=f"DANGER: {i_ma}mA exceeds limit!\nPower: {p_watts:.3f} W", fg="red", font=("Arial", 11, "bold"))
            else:
                self.result_label.config(text=f"SAFE: Within limits.\nPower: {p_watts:.3f} W\nCurrent: {i_amps} A", fg="green", font=("Arial", 11))
        except ValueError:
            messagebox.showerror("Input Error", "Please enter numeric values only.")

    def setup_units_ui(self):
        info_box = ttk.LabelFrame(self.tab_units, text=" Metric Prefix Reference ")
        info_box.pack(padx=20, pady=10, fill="x")
        prefix_data = "Mega (M) = 10^6\nKilo (k) = 10^3\nBase = 10^0\nMilli (m) = 10^-3\nMicro (μ) = 10^-6"
        info_label = tk.Label(info_box, text=prefix_data, justify="left", font=("Courier", 10), padx=10, pady=10)
        info_label.pack()
        unit_box = ttk.LabelFrame(self.tab_units, text=" Metric Prefix Converter ")
        unit_box.pack(padx=20, pady=20, fill="x")
        tk.Label(unit_box, text="Value:").grid(row=0, column=0, padx=10, pady=10)
        self.unit_input = tk.Entry(unit_box)
        self.unit_input.grid(row=0, column=1, padx=10, pady=10)
        self.prefixes = {"Micro (μ)": 1e-6, "Milli (m)": 1e-3, "Base (None)": 1, "Kilo (k)": 1e3, "Mega (M)": 1e6}
        self.from_unit = ttk.Combobox(unit_box, values=list(self.prefixes.keys()), state="readonly")
        self.from_unit.set("Base (None)")
        self.from_unit.grid(row=1, column=1, pady=5)
        self.to_unit = ttk.Combobox(unit_box, values=list(self.prefixes.keys()), state="readonly")
        self.to_unit.set("Milli (m)")
        self.to_unit.grid(row=2, column=1, pady=5)
        tk.Button(unit_box, text="Convert", command=self.convert_units).grid(row=3, column=0, columnspan=2, pady=15)
        self.unit_result = tk.Label(self.tab_units, text="Result: --", font=("Arial", 12, "bold"))
        self.unit_result.pack(pady=10)

    def convert_units(self):
        try:
            val = float(self.unit_input.get())
            result = (val * self.prefixes[self.from_unit.get()]) / self.prefixes[self.to_unit.get()]
            self.unit_result.config(text=f"Result: {result:g} {self.to_unit.get().split(' ')[1]}", fg="blue")
        except ValueError:
            messagebox.showerror("Error", "Enter a valid number.")

    def setup_resistor_ui(self):
        ref_box = ttk.LabelFrame(self.tab_resistors, text=" Color Code Reference ")
        ref_box.pack(padx=20, pady=10, fill="x")
        ref_label = tk.Label(ref_box, text="Black:0 | Brown:1 | Red:2 | Gold:±5%...", font=("Courier", 9))
        ref_label.pack()
        self.resistor_mode = tk.StringVar(value="4")
        mode_frame = tk.Frame(self.tab_resistors)
        mode_frame.pack(pady=5)
        tk.Radiobutton(mode_frame, text="4-Band", variable=self.resistor_mode, value="4", command=self.toggle_bands).pack(side="left")
        tk.Radiobutton(mode_frame, text="5-Band", variable=self.resistor_mode, value="5", command=self.toggle_bands).pack(side="left")
        self.band_frame = tk.Frame(self.tab_resistors)
        self.band_frame.pack(pady=10)
        self.b1 = ttk.Combobox(self.band_frame, values=list(self.colors.keys()), state="readonly")
        self.b1.pack()
        self.b2 = ttk.Combobox(self.band_frame, values=list(self.colors.keys()), state="readonly")
        self.b2.pack()
        self.b3 = ttk.Combobox(self.band_frame, values=list(self.colors.keys()), state="readonly")
        self.b_mult = ttk.Combobox(self.band_frame, values=list(self.multipliers.keys()), state="readonly")
        self.b_mult.pack()
        self.b_tol = ttk.Combobox(self.band_frame, values=list(self.tolerances.keys()), state="readonly")
        self.b_tol.pack()
        tk.Button(self.tab_resistors, text="Calculate", command=self.calc_resistor).pack()
        self.res_output = tk.Label(self.tab_resistors, text="Result...", font=("Arial", 12, "bold"))
        self.res_output.pack()
        self.toggle_bands()

    def toggle_bands(self):
        if self.resistor_mode.get() == "5": self.b3.pack()
        else: self.b3.pack_forget()

    def calc_resistor(self):
        try:
            val = int(str(self.colors[self.b1.get()]) + str(self.colors[self.b2.get()]))
            if self.resistor_mode.get() == "5": val = int(str(val) + str(self.colors[self.b3.get()]))
            total = val * self.multipliers[self.b_mult.get()]
            self.res_output.config(text=f"Value: {total}Ω ±{self.tolerances[self.b_tol.get()]}%")
        except: messagebox.showerror("Error", "Select all bands.")

    # --- UPDATED QUIZ UI FOR V9 (History Logging) ---
    def setup_quiz_ui(self):
        # Header
        tk.Label(self.tab_quiz, text="Mastery Quiz", font=("Arial", 14, "bold")).pack(pady=5)
        
        # Question Area
        self.quiz_frame = ttk.LabelFrame(self.tab_quiz, text=" Current Question ")
        self.quiz_frame.pack(padx=20, pady=5, fill="x")

        self.q_label = tk.Label(self.quiz_frame, text="Click 'Start Quiz' to begin!", wraplength=450)
        self.q_label.pack(pady=10)

        self.ans_buttons = []
        for i in range(4):
            btn = tk.Button(self.quiz_frame, text="", width=30, command=lambda i=i: self.check_answer(i))
            btn.pack(pady=2)
            self.ans_buttons.append(btn)
            btn.config(state="disabled")

        self.start_btn = tk.Button(self.tab_quiz, text="Start Quiz", command=self.start_quiz)
        self.start_btn.pack(pady=5)

        # --- NEW HISTORY SECTION FOR V9 ---
        hist_box = ttk.LabelFrame(self.tab_quiz, text=" Quiz Attempt History (Log File) ")
        hist_box.pack(padx=20, pady=10, fill="both", expand=True)

        self.history_text = tk.Text(hist_box, height=8, state="disabled", font=("Courier", 9))
        self.history_text.pack(padx=10, pady=5, fill="both", expand=True)

        btn_row = tk.Frame(hist_box)
        btn_row.pack(pady=5)
        tk.Button(btn_row, text="Refresh History", command=self.load_history).pack(side="left", padx=5)
        tk.Button(btn_row, text="Clear History File", command=self.clear_history_file).pack(side="left", padx=5)

    def start_quiz(self):
        self.current_q_index = 0
        self.score = 0
        for btn in self.ans_buttons: btn.config(state="normal")
        self.start_btn.config(state="disabled")
        self.show_question()

    def show_question(self):
        if self.current_q_index < len(self.quiz_questions):
            q_data = self.quiz_questions[self.current_q_index]
            self.q_label.config(text=f"Q{self.current_q_index + 1}: {q_data['q']}")
            opts = list(q_data['o'])
            random.shuffle(opts)
            for i, opt in enumerate(opts): self.ans_buttons[i].config(text=opt)
        else:
            self.save_result_to_file() # Save to file when finished
            self.end_quiz()

    def check_answer(self, idx):
        if self.ans_buttons[idx].cget("text") == self.quiz_questions[self.current_q_index]['a']:
            self.score += 1
        self.current_q_index += 1
        self.show_question()

    def end_quiz(self):
        percent = (self.score / 10) * 100
        msg = f"Score: {percent}%"
        self.q_label.config(text=f"Quiz Finished! {msg}", font=("Arial", 11, "bold"))
        for btn in self.ans_buttons: btn.config(state="disabled")
        self.start_btn.config(state="normal", text="Retake Quiz")
        self.load_history() # Update history view automatically

    # --- FILE I/O METHODS FOR V9 ---
    def save_result_to_file(self):
        """TECHNIQUE: Appending data to a text file"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        status = "PASS" if self.score >= 7 else "FAIL"
        entry = f"[{timestamp}] Score: {self.score}/10 | {status}\n"
        
        with open("quiz_log.txt", "a") as file:
            file.write(entry)

    def load_history(self):
        """TECHNIQUE: Reading data from a text file"""
        self.history_text.config(state="normal")
        self.history_text.delete("1.0", tk.END)
        
        if os.path.exists("quiz_log.txt"):
            with open("quiz_log.txt", "r") as file:
                self.history_text.insert(tk.END, file.read())
        else:
            self.history_text.insert(tk.END, "No history found.")
        
        self.history_text.config(state="disabled")

    def clear_history_file(self):
        """TECHNIQUE: Wiping a file"""
        if messagebox.askyesno("Confirm", "Wipe the history log?"):
            open("quiz_log.txt", "w").close()
            self.load_history()

if __name__ == "__main__":
    root = tk.Tk()
    app = RoboticsToolkit(root)
    root.mainloop()