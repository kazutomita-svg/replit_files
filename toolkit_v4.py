# Robotics & Electronics Toolkit Version 4
import tkinter as tk
from tkinter import ttk, messagebox

class RoboticsToolkit:
    def __init__(self, root):
        self.root = root
        self.root.title("JackBord Toolkit Version 4 - Power Calculator")
        self.root.geometry("500x450")

        # Tab Controller
        self.notebook = ttk.Notebook(root)
        self.tab_power = ttk.Frame(self.notebook)
        self.tab_units = ttk.Frame(self.notebook)
        self.tab_resistors = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_power, text="Power")
        self.notebook.add(self.tab_units, text="Units")
        self.notebook.add(self.tab_resistors, text="Resistors")
        self.notebook.pack(expand=1, fill="both")

        self.setup_power_logic_ui()

    def setup_power_logic_ui(self):
        # Power Calculator UI
        power_box = ttk.LabelFrame(self.tab_power, text=" Power Calculator (P = IV) ")
        power_box.pack(padx=20, pady=20, fill="x")

        # Voltage Input
        tk.Label(power_box, text="Voltage (V):").grid(row=0, column=0, padx=10, pady=10)
        self.voltage_entry = tk.Entry(power_box)
        self.voltage_entry.grid(row=0, column=1, padx=10, pady=10)

        # Current Input
        tk.Label(power_box, text="Current:").grid(row=1, column=0, padx=10, pady=10)
        self.current_entry = tk.Entry(power_box)
        self.current_entry.grid(row=1, column=1, padx=10, pady=10)

        # Unit Selection Dropdown (Refined Feature)
        self.unit_var = tk.StringVar(value="mA")
        self.unit_dropdown = ttk.Combobox(power_box, textvariable=self.unit_var, width=5, state="readonly")
        self.unit_dropdown['values'] = ("mA", "A")
        self.unit_dropdown.grid(row=1, column=2, padx=5)

        # Calculation Button
        self.calc_button = tk.Button(power_box, text="Calculate & Check Safety", 
                                     command=self.calculate_power)
        self.calc_button.grid(row=2, column=0, columnspan=3, pady=15)

        # Output Display
        self.result_label = tk.Label(self.tab_power, text="Enter values and click calculate.", 
                                     wraplength=400, font=("Arial", 11))
        self.result_label.pack(pady=20)

    def calculate_power(self):
        try:
            # Input Handling
            v = float(self.voltage_entry.get())
            raw_i = float(self.current_entry.get())
            unit = self.unit_var.get()

            # Converting to Amps if needed
            if unit == "mA":
                i_amps = raw_i / 1000
                i_ma = raw_i
            else:
                i_amps = raw_i
                i_ma = raw_i * 1000

            # Calculation (P = IV)
            p_watts = v * i_amps

            # Safety Limit Check (500mA)
            if i_ma > 500:
                result_text = f"DANGER: {i_ma}mA exceeds the 500mA JackBord limit!\nPower: {p_watts:.3f} W"
                self.result_label.config(text=result_text, fg="red", font=("Arial", 11, "bold"))
            else:
                result_text = f"SAFE: Circuit is within limits.\nPower: {p_watts:.3f} W\nCurrent: {i_amps} A"
                self.result_label.config(text=result_text, fg="green", font=("Arial", 11))

        except ValueError:
            messagebox.showerror("Input Error", "Please enter numeric values only.")

if __name__ == "__main__":
    root = tk.Tk()
    app = RoboticsToolkit(root)
    root.mainloop()
