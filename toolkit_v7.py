# Robotics & Electronics Toolkit Version 7
import tkinter as tk
from tkinter import ttk, messagebox

class RoboticsToolkit:
    def __init__(self, root):
        self.root = root
        self.root.title("JackBord Toolkit Version 7 - Resistors Tab")
        self.root.geometry("550x800")

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
        self.setup_units_ui()

        # Colour data for resistor calculations
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

        # Unit Selection Dropdown
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

    def setup_units_ui(self):
        # Information Box: This helps students with the theory while they use the tool
        info_box = ttk.LabelFrame(self.tab_units, text=" Metric Prefix Reference ")
        info_box.pack(padx=20, pady=10, fill="x")

        prefix_data = (
            "Mega (M)  = 1,000,000 (10^6)\n"
            "Kilo (k)  = 1,000 (10^3)\n"
            "Base      = 1 (10^0)\n"
            "Milli (m) = 0.001 (10^-3)\n"
            "Micro (μ) = 0.000001 (10^-6)"
        )
        
        info_label = tk.Label(info_box, text=prefix_data, justify="left", 
                              font=("Courier", 10), padx=10, pady=10)
        info_label.pack()

        # Units Conversion UI
        unit_box = ttk.LabelFrame(self.tab_units, text=" Metric Prefix Converter ")
        unit_box.pack(padx=20, pady=20, fill="x")

        tk.Label(unit_box, text="Enter Value:").grid(row=0, column=0, padx=10, pady=10)
        self.unit_input = tk.Entry(unit_box)
        self.unit_input.grid(row=0, column=1, padx=10, pady=10)

        # Defining the Prefixes and their Multipliers
        self.prefixes = {
            "Micro (μ)": 1e-6,
            "Milli (m)": 1e-3,
            "Base (None)": 1,
            "Kilo (k)": 1e3,
            "Mega (M)": 1e6
        }

        # Dropdowns for "From" and "To"
        tk.Label(unit_box, text="From:").grid(row=1, column=0)
        self.from_unit = ttk.Combobox(unit_box, values=list(self.prefixes.keys()), state="readonly")
        self.from_unit.set("Base (None)")
        self.from_unit.grid(row=1, column=1, pady=5)

        tk.Label(unit_box, text="To:").grid(row=2, column=0)
        self.to_unit = ttk.Combobox(unit_box, values=list(self.prefixes.keys()), state="readonly")
        self.to_unit.set("Milli (m)")
        self.to_unit.grid(row=2, column=1, pady=5)

        # Calculation Button
        self.convert_btn = tk.Button(unit_box, text="Convert Units", command=self.convert_units)
        self.convert_btn.grid(row=3, column=0, columnspan=2, pady=15)

        # Output Display
        self.unit_result = tk.Label(self.tab_units, text="Result: --", font=("Arial", 12, "bold"))
        self.unit_result.pack(pady=10)

    def convert_units(self):
        try:
            # Conversion Logic
            val = float(self.unit_input.get())
            from_mult = self.prefixes[self.from_unit.get()]
            to_mult = self.prefixes[self.to_unit.get()]

            # Math: (Value * Source Multiplier) / Target Multiplier
            # Example: 1 Kilo to Milli -> (1 * 1000) / 0.001 = 1,000,000
            result = (val * from_mult) / to_mult

            self.unit_result.config(text=f"Result: {result:g} {self.to_unit.get().split(' ')[1]}", fg="blue")

        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid number.")

    def setup_resistor_ui(self):
        ref_box = ttk.LabelFrame(self.tab_resistors, text=" Resistor Colour Code Reference ")
        ref_box.pack(padx=20, pady=10, fill="x")

        # Table For Resistor Colour Codes
        ref_text =  "Colour  | Digit | Multiplier | Tolerance\n"
        ref_text += "-------|-------|------------|----------\n"
        ref_text += "Black  |   0   | x1         | --\n"
        ref_text += "Brown  |   1   | x10        | ±1%\n"
        ref_text += "Red    |   2   | x100       | ±2%\n"
        ref_text += "Orange |   3   | x1k        | --\n"
        ref_text += "Yellow |   4   | x10k       | --\n"
        ref_text += "Green  |   5   | x100k      | --\n"
        ref_text += "Blue   |   6   | x1M        | --\n"
        ref_text += "Violet |   7   | --         | --\n"
        ref_text += "Gray   |   8   | --         | --\n"
        ref_text += "White  |   9   | --         | --\n"
        ref_text += "Gold   |   --  | --         | ±5%\n"
        ref_text += "Silver |   --  | --         | ±10%"

        ref_label = tk.Label(ref_box, text=ref_text, justify="left", 
                     font=("Courier", 9), padx=10, pady=10)
        ref_label.pack()

        # Mode Selection (4-band or 5-band)
        mode_frame = ttk.LabelFrame(self.tab_resistors, text=" Select Resistor Type ")
        mode_frame.pack(padx=20, pady=10, fill="x")

        self.resistor_mode = tk.StringVar(value="4")
        tk.Radiobutton(mode_frame, text="4-Band Resistor", variable=self.resistor_mode, 
                       value="4", command=self.toggle_bands).pack(side="left", padx=20)
        tk.Radiobutton(mode_frame, text="5-Band Resistor", variable=self.resistor_mode, 
                       value="5", command=self.toggle_bands).pack(side="left", padx=20)

        # Dropdown Frame
        self.band_frame = ttk.LabelFrame(self.tab_resistors, text=" Select Band Colours ")
        self.band_frame.pack(padx=20, pady=10, fill="x")

        # Digit 1
        tk.Label(self.band_frame, text="Band 1:").grid(row=0, column=0, pady=5)
        self.b1 = ttk.Combobox(self.band_frame, values=list(self.colors.keys()), state="readonly")
        self.b1.grid(row=0, column=1)

        # Digit 2
        tk.Label(self.band_frame, text="Band 2:").grid(row=1, column=0, pady=5)
        self.b2 = ttk.Combobox(self.band_frame, values=list(self.colors.keys()), state="readonly")
        self.b2.grid(row=1, column=1)

        # Digit 3 (Only for 5-band)
        self.b3_label = tk.Label(self.band_frame, text="Band 3:")
        self.b3 = ttk.Combobox(self.band_frame, values=list(self.colors.keys()), state="readonly")
        
        # Multiplier
        tk.Label(self.band_frame, text="Multiplier:").grid(row=3, column=0, pady=5)
        self.b_mult = ttk.Combobox(self.band_frame, values=list(self.multipliers.keys()), state="readonly")
        self.b_mult.grid(row=3, column=1)

        # Tolerance
        tk.Label(self.band_frame, text="Tolerance:").grid(row=4, column=0, pady=5)
        self.b_tol = ttk.Combobox(self.band_frame, values=list(self.tolerances.keys()), state="readonly")
        self.b_tol.grid(row=4, column=1)

        # Output
        tk.Button(self.tab_resistors, text="Calculate Resistance", command=self.calc_resistor).pack(pady=10)
        self.res_output = tk.Label(self.tab_resistors, text="Results will appear here...", font=("Arial", 12, "bold"))
        self.res_output.pack(pady=10)

        self.toggle_bands() # Set initial state (sets up the tab before resistor tab is selected)

    def toggle_bands(self):
        """Hides or shows the 3rd digit band based on selection"""
        if self.resistor_mode.get() == "4":
            self.b3_label.grid_remove()
            self.b3.grid_remove()
        else:
            self.b3_label.grid(row=2, column=0, pady=5)
            self.b3.grid(row=2, column=1)

    def calc_resistor(self):
        try:
            d1 = str(self.colors[self.b1.get()])
            d2 = str(self.colors[self.b2.get()])
            mult = self.multipliers[self.b_mult.get()]
            tol = self.tolerances[self.b_tol.get()]

            if self.resistor_mode.get() == "5":
                d3 = str(self.colors[self.b3.get()])
                base_value = int(d1 + d2 + d3)
            else:
                base_value = int(d1 + d2)

            total_ohms = base_value * mult
            
            # Format display (Ohms, kOhms, MOhms)
            display_val = f"{total_ohms:g} Ω"
            if total_ohms >= 1000000:
                display_val = f"{total_ohms/1000000:g} MΩ"
            elif total_ohms >= 1000:
                display_val = f"{total_ohms/1000:g} kΩ"

            # Calculate tolerance range
            variation = total_ohms * (tol / 100)
            lower = total_ohms - variation
            upper = total_ohms + variation

            self.res_output.config(text=f"Value: {display_val} ±{tol}%\nRange: {lower:g}Ω to {upper:g}Ω", fg="blue")

        except Exception:
            messagebox.showerror("Error", "Please select a colour for all bands.")

if __name__ == "__main__":
    root = tk.Tk()
    app = RoboticsToolkit(root)
    root.mainloop()
