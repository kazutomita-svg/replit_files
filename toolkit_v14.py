# Robotics & Electronics Toolkit Version 14 - Finished Version
"""
An educational GUI application designed to teach fundamental electronics concepts.

This toolkit includes the following features:
  - Power Calculator: Calculates electrical power (P = IV) with safety limits for JackBord
  - Unit Converter: Converts between prefixes (Micro, Milli, Base, Kilo, Mega)
  - Resistor Calculator: Identifies resistor values using colour band codes
  - Mastery Quiz: Tests students' understanding and tracks history of quiz attempts
  - Help & Documentation: User guide and reference material for all modules

External libraries used:
  - tkinter: Python GUI toolkit for building the user interface
  - random: For shuffling quiz options
  - datetime: For timestamping quiz attempts
  - os: For file operations (quiz history log)
"""

import os
import random
import tkinter as tk
from datetime import datetime
from tkinter import messagebox, ttk


class RoboticsToolkit:
    """
    Class for the Robotics & Electronics Toolkit.

    This class manages the tabbed GUI interface and all calculator,
    converter, and quiz functionality. It creates a user-friendly
    environment for learning and practicing electronics concepts.

    Things it has:
        root (tk.Tk): The main tkinter window
        notebook (ttk.Notebook): Tab container for different tools
        tab_power (ttk.Frame): Tab for power calculations
        tab_units (ttk.Frame): Tab for unit conversions
        tab_resistors (ttk.Frame): Tab for resistor colour code calculations
        tab_quiz (ttk.Frame): Tab for mastery quiz and history
        tab_help (ttk.Frame): Tab for documentation
        colors (dict): Resistor colour-to-digit mapping
        multipliers (dict): Resistor colour-to-multiplier mapping
        tolerances (dict): Resistor colour-to-tolerance mapping
        quiz_questions (list): 10 quiz questions with options and answers
        score (int): Current quiz attempt score
    """

    def __init__(self, main_window):
        """
        Starting up the Robotics & Electronics Toolkit application.

        Sets up the main window, creates five tabs with different
        tools/calculators, and loads all UI components.
        """
        self.root = main_window
        self.root.title("JackBord Toolkit Version 14 - Finished Version")
        self.root.geometry("650x850")

        # JackBord Theme Colours
        self.jb_blue = "#1E88E5"
        self.jb_dark_blue = "#1565C0"
        self.jb_yellow = "#FFD54F"
        self.jb_white = "#F8F8F8"

        self.root.configure(bg=self.jb_white)

        # ttk Styling
        self.style = ttk.Style()

        self.style.configure("TNotebook", background=self.jb_white)

        self.style.configure(
            "TNotebook.Tab", padding=[10, 5], font=("Arial", 10, "bold")
        )

        self.style.configure("TLabelframe", background=self.jb_white)

        self.style.configure(
            "TLabelframe.Label",
            background=self.jb_white,
            foreground=self.jb_dark_blue,
            font=("Arial", 10, "bold"),
        )

        # Initialize tabbed interface (Tab Controller)
        # Behaviour:Using tabs separates the modules so there is no clutter
        self.notebook = ttk.Notebook(self.root)
        self.tab_power = ttk.Frame(self.notebook)
        self.tab_units = ttk.Frame(self.notebook)
        self.tab_resistors = ttk.Frame(self.notebook)
        self.tab_quiz = ttk.Frame(self.notebook)
        self.tab_help = ttk.Frame(self.notebook)

        # Register tabs with notebook and set tab labels
        # Job: Organize calculator tabs for easy navigation
        self.notebook.add(self.tab_power, text="Power")
        self.notebook.add(self.tab_units, text="Units")
        self.notebook.add(self.tab_resistors, text="Resistors")
        self.notebook.add(self.tab_quiz, text="Quiz & History")
        self.notebook.add(self.tab_help, text="Help & Documentation")
        self.notebook.pack(expand=1, fill="both")

        # Resistor colour code reference data
        # Job: Maps colour names to their numeric and multiplier values for resistor calculations
        self.colors = {
            "Black": 0,
            "Brown": 1,
            "Red": 2,
            "Orange": 3,
            "Yellow": 4,
            "Green": 5,
            "Blue": 6,
            "Violet": 7,
            "Gray": 8,
            "White": 9,
        }
        # Multiplier values in powers of 10 for resistor band calculations
        self.multipliers = {
            "Black": 1,
            "Brown": 10,
            "Red": 100,
            "Orange": 1000,
            "Yellow": 10000,
            "Green": 100000,
            "Blue": 1000000,
        }
        # Tolerance percentages for tolerance bands
        self.tolerances = {"Brown": 1, "Red": 2, "Gold": 5, "Silver": 10}

        # GUI colours
        self.jb_white = "#f8f8f8"

        # Quiz question bank and answers
        # Job: Stores 10 questions covering power, units, resistors, and safety
        # Behaviour: Questions are randomized during quiz to prevent memorization and test
        # deeper understanding. Each question has 4 multiple-choice options and one correct answer.
        self.quiz_questions = [
            {
                "q": "What is the formula for Power?",
                "o": ["P = I/V", "P = IV", "P = V/I", "P = I+V"],
                "a": "P = IV",
            },
            {
                "q": "What is the limit for current on a JackBord pin?",
                "o": ["100mA", "500mA", "1A", "5A"],
                "a": "500mA",
            },
            {
                "q": "How many Ohms is 1.5kΩ?",
                "o": ["150", "1500", "15000", "1.5"],
                "a": "1500",
            },
            {
                "q": "Which prefix represents 10^-6?",
                "o": ["Milli (m)", "Kilo (k)", "Micro (μ)", "Mega (M)"],
                "a": "Micro (μ)",
            },
            {
                "q": "A resistor with Brown, Black, Red bands is how many Ohms?",
                "o": ["100Ω", "1kΩ", "10kΩ", "110Ω"],
                "a": "1kΩ",
            },
            {
                "q": "What colour represents a '2' in the digit bands?",
                "o": ["Red", "Orange", "Brown", "Black"],
                "a": "Red",
            },
            {
                "q": "If Voltage is 10V and Current is 0.2A, what is the Power?",
                "o": ["2W", "50W", "0.02W", "20W"],
                "a": "2W",
            },
            {
                "q": "What does a Gold tolerance band mean?",
                "o": ["±1%", "±5%", "±10%", "±2%"],
                "a": "±5%",
            },
            {
                "q": "Convert 5,000,000Ω to Mega-Ohms.",
                "o": ["50MΩ", "0.5MΩ", "5MΩ", "500MΩ"],
                "a": "5MΩ",
            },
            {
                "q": "Which current is safer for the JackBord?",
                "o": ["600mA", "200mA", "1.2A", "0.8A"],
                "a": "200mA",
            },
        ]

        # Quiz state variables
        # Job: Tracks progress through current quiz attempt
        self.current_q_index = 0  # Current question number (0-9)
        self.score = 0  # Current attempt score (0-10)

        # Initialize all UI components for each tab
        self.setup_power_logic_ui()
        self.setup_units_ui()
        self.setup_resistor_ui()
        self.setup_quiz_ui()
        self.setup_help_ui()

    # Button Styling
    def style_button(self, button):
        """
        Apply JackBord styling to tkinter buttons.
        """

        button.configure(
            bg=self.jb_blue,
            fg=self.jb_yellow,
            activebackground=self.jb_dark_blue,
            activeforeground="white",
            font=("Arial", 10, "bold"),
            relief="raised",
            bd=2,
        )

    def setup_power_logic_ui(self):
        """
        Power Calculator tab interface and controls.

        Creates input fields for voltage and current, unit selector, and a calculation button.
        Displays results with safety warnings if current exceeds JackBord limits (500mA).

        Job: Creates the user interface for electrical power calculations
        Behaviour: Power calculation is necessary for circuit safety. The 500mA limit
        warning prevents damage to the JackBord by highlighting unsafe conditions.
        """
        # Create main container for power calculator widgets
        power_box = ttk.LabelFrame(self.tab_power, text=" Power Calculator (P = IV) ")
        power_box.pack(padx=20, pady=20, fill="x")

        # Voltage input field (in Volts)
        # Job: Accepts user input for voltage value
        tk.Label(
            power_box,
            text="Voltage (V):",
            bg=self.jb_white,
            fg=self.jb_dark_blue,
            font=("Arial", 10, "bold"),
        ).grid(row=0, column=0, padx=10, pady=10)
        self.voltage_entry = tk.Entry(power_box)
        self.voltage_entry.grid(row=0, column=1, padx=10, pady=10)

        # Current input field with unit selector (milliamps or amps)
        # Job: Accepts user input for current value
        # Behaviour: Supporting both mA and A units improves usability and reduces input errors
        tk.Label(
            power_box,
            text="Current:",
            bg=self.jb_white,
            fg=self.jb_dark_blue,
            font=("Arial", 10, "bold"),
        ).grid(row=1, column=0, padx=10, pady=10)
        self.current_entry = tk.Entry(power_box)
        self.current_entry.grid(row=1, column=1, padx=10, pady=10)

        # Unit selection dropdown for current (milliamps or amps)
        # Job: Allows user to specify current unit
        self.unit_var = tk.StringVar(value="mA")
        self.unit_dropdown = ttk.Combobox(
            power_box, textvariable=self.unit_var, width=5, state="readonly"
        )
        self.unit_dropdown["values"] = ("mA", "A")
        self.unit_dropdown.grid(row=1, column=2, padx=5)

        # Calculation button
        # Job: Initiates power calculation and safety check
        self.calc_button = tk.Button(
            power_box, text="Calculate & Check Safety", command=self.calculate_power
        )
        self.calc_button.grid(row=2, column=0, columnspan=3, pady=15)
        self.style_button(self.calc_button)  # Apply JackBord styling to the button

        # Output display area for results and warnings
        # Job: Shows calculated power value and safety status
        self.result_label = tk.Label(
            self.tab_power,
            text="Enter values and click calculate.",
            fg=self.jb_dark_blue,
            wraplength=400,
            font=("Arial", 11),
        )
        self.result_label.pack(pady=20)

    def calculate_power(self):
        """
        Perform power calculation (P = IV) and check circuit safety.

        Retrieves voltage and current inputs, converts units as needed, calculates
        electrical power, and checks if current exceeds the 500mA JackBord safety limit.
        Displays results with colour-coded warnings (red for danger, green for safe).

        Formula: Power (watts) = Voltage (volts) * Current (amps)

        Error Handling:
            messagebox.showerror: If non-numeric input is provided
        """
        try:
            # Parse user inputs from entry fields
            v = float(self.voltage_entry.get())
            raw_i = float(self.current_entry.get())
            unit = self.unit_var.get()

            # Unit conversion: convert current to both Amps and milliamps for calculation
            # Job: Ensures consistent unit handling regardless of user selection
            # Behaviour: Power formula uses Amps, but safety limits use milliamps
            if unit == "mA":
                i_amps = raw_i / 1000  # Convert milliamps to amps
                i_ma = raw_i
            else:
                i_amps = raw_i
                i_ma = raw_i * 1000  # Convert amps to milliamps

            # Calculation using P=IV formula
            # Job: Calculate electrical power
            p_watts = v * i_amps

            # Safety limit check
            # Job: Prevent damage by warning when current exceeds limit
            # Behaviour: 500mA is the maximum safe current for JackBord
            if i_ma > 500:
                result_text = (
                    f"DANGER: {i_ma}mA exceeds the 500mA JackBord "
                    f"limit!\nPower: {p_watts:.3f} W"
                )
                self.result_label.config(
                    text=result_text, fg="red", font=("Arial", 11, "bold")
                )
            else:
                result_text = (
                    f"SAFE: Circuit is within limits.\nPower: "
                    f"{p_watts:.3f} W\nCurrent: {i_amps} A"
                )
                self.result_label.config(
                    text=result_text, fg="green", font=("Arial", 11)
                )

        except ValueError:
            # Handle invalid input
            messagebox.showerror("Input Error", "Please enter numeric values only.")

    def setup_units_ui(self):
        """
        Unit Converter tab interface.

        Creates a reference display of prefixes with their powers of 10, and
        sets up conversion controls allowing users to convert values between
        different scales (Micro, Milli, Base, Kilo, Mega).

        Job: Implements the learning of prefixes and conversion functionality
        Behaviour: Understanding metric prefixes is crucial for working with values.
        """
        # Information display box for prefix reference
        # Job: Shows metric prefix chart
        # Behaviour: Having reference material reinforces learning
        # by keeping formulas in view while working
        info_box = ttk.LabelFrame(self.tab_units, text=" Metric Prefix Reference ")
        info_box.pack(padx=20, pady=10, fill="x")

        # Prefix reference chart with powers of 10
        # Behaviour: Both forms shown to support different learning styles
        prefix_data = (
            "Mega (M)  = 1,000,000 (10^6)\n"
            "Kilo (k)  = 1,000 (10^3)\n"
            "Base      = 1 (10^0)\n"
            "Milli (m) = 0.001 (10^-3)\n"
            "Micro (μ) = 0.000001 (10^-6)"
        )

        info_label = tk.Label(
            info_box,
            text=prefix_data,
            justify="left",
            font=("Courier", 10),
            padx=10,
            pady=10,
            bg=self.jb_white,
            fg=self.jb_dark_blue,
        )
        info_label.pack()

        # Conversion tool UI
        # Job: Provides interactive unit conversion interface
        unit_box = ttk.LabelFrame(self.tab_units, text=" Metric Prefix Converter ")
        unit_box.pack(padx=20, pady=20, fill="x")

        # Input field for value to be converted
        tk.Label(
            unit_box,
            text="Enter Value:",
            bg=self.jb_white,
            fg=self.jb_dark_blue,
            font=("Arial", 10, "bold"),
        ).grid(row=0, column=0, padx=10, pady=10)
        self.unit_input = tk.Entry(unit_box)
        self.unit_input.grid(row=0, column=1, padx=10, pady=10)

        # Define prefix multiplier
        # Job: Assigns prefix names to their scientific notation values
        self.prefixes = {
            "Micro (μ)": 1e-6,
            "Milli (m)": 1e-3,
            "Base (None)": 1,
            "Kilo (k)": 1e3,
            "Mega (M)": 1e6,
        }

        # Source unit selection dropdown
        # Job: Specifies the original prefix of the value to be converted
        tk.Label(unit_box, text="From:", bg=self.jb_white).grid(row=1, column=0)
        self.from_unit = ttk.Combobox(
            unit_box, values=list(self.prefixes.keys()), state="readonly"
        )
        self.from_unit.set("Base (None)")  # Default: no prefix
        self.from_unit.grid(row=1, column=1, pady=5)

        # Target unit selection dropdown
        # Job: Specifies the prefix after conversion
        tk.Label(unit_box, text="To:", bg=self.jb_white).grid(row=2, column=0)
        self.to_unit = ttk.Combobox(
            unit_box, values=list(self.prefixes.keys()), state="readonly"
        )
        self.to_unit.set("Milli (m)")  # Default: convert to millis
        self.to_unit.grid(row=2, column=1, pady=5)

        # Conversion button
        # Job: Initiates unit conversion calculation
        self.convert_btn = tk.Button(
            unit_box, text="Convert Units", command=self.convert_units
        )
        self.convert_btn.grid(row=3, column=0, columnspan=2, pady=15)
        self.style_button(self.convert_btn)  # Apply JackBord styling to the button

        # Conversion result display
        # Job: Shows the converted value with specified prefix
        self.unit_result = tk.Label(
            self.tab_units,
            text="Result: --",
            font=("Arial", 12, "bold"),
            fg=self.jb_dark_blue,
        )
        self.unit_result.pack(pady=10)

    def convert_units(self):
        """
        Perform prefix conversion.

        Converts a value from one prefix to another using the formula:
        (value * source_multiplier) / target_multiplier

        Eg: 1 Kilo (1000) to Milli (0.001) → (1 * 1000) / 0.001 = 1,000,000

        Job: Perform unit conversion calculations

        Error handling:
            messagebox.showerror: If non-numeric input is provided
        """
        try:
            #  Take input values
            val = float(self.unit_input.get())
            from_mult = self.prefixes[self.from_unit.get()]
            to_mult = self.prefixes[self.to_unit.get()]

            # Math: (Value * Source Multiplier) / Target Multiplier
            # Example: 1 Kilo to Milli -> (1 * 1000) / 0.001 = 1,000,000
            # Behaviour: This method handles all prefix combinations in a single formula
            result = (val * from_mult) / to_mult

            # Display result with formatted number and target unit symbol
            self.unit_result.config(
                text=f"Result: {result:g} {self.to_unit.get().split(' ')[1]}", fg="blue"
            )

        except ValueError:
            # Error handling for invalid input
            messagebox.showerror("Input Error", "Please enter a valid number.")

    def setup_resistor_ui(self):
        """
        Resistor Calculator tab interface.

        Creates a colour code reference chart, mode selector (4-band vs 5-band),
        dropdown menus for band colour selection, and calculation controls.
        Displays calculated resistance value and tolerance range.

        Job: Implements resistor colour code calculation interface
        Behaviour: Visual reference and interactive selection help students identify
        physical resistors and calculating their values.
        """
        # Reference chart for resistor colour codes
        # Job: Display colour code reference table
        # Behaviour: Having the reference visible during colour selection
        # helps students understand what each colour represents
        ref_box = ttk.LabelFrame(
            self.tab_resistors, text=" Resistor Colour Code Reference "
        )
        ref_box.pack(padx=20, pady=10, fill="x")

        # Formatted reference table showing resistor colour code standards
        # Behaviour: Table format makes quick lookups easy
        ref_text = "Colour | Digit | Multiplier | Tolerance\n"
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

        ref_label = tk.Label(
            ref_box,
            text=ref_text,
            justify="left",
            font=("Courier", 9),
            padx=10,
            pady=10,
            bg=self.jb_white,
            fg=self.jb_dark_blue,
        )  # Courier font for aligned columns
        ref_label.pack()

        # Mode selection interface for different resistor bands
        # Job: Allow users to switch between 4-band and 5-band resistor calculations
        # Behaviour: Supporting both resistors helps students understand the differences
        mode_frame = ttk.LabelFrame(self.tab_resistors, text=" Select Resistor Type ")
        mode_frame.pack(padx=20, pady=10, fill="x")

        # Radio buttons for resistor band configuration
        # Job: Track selected resistor type (4-band or 5-band)
        self.resistor_mode = tk.StringVar(value="4")
        tk.Radiobutton(
            mode_frame,
            text="4-Band Resistor",
            variable=self.resistor_mode,
            value="4",
            bg=self.jb_white,
            command=self.toggle_bands,
        ).pack(side="left", padx=20)
        tk.Radiobutton(
            mode_frame,
            text="5-Band Resistor",
            variable=self.resistor_mode,
            value="5",
            bg=self.jb_white,
            command=self.toggle_bands,
        ).pack(side="left", padx=20)

        # Colour band selection box
        # Job: Contains dropdown controls for each resistor band
        # Behaviour: Dropdown selection to account for the large number of colour options
        self.band_frame = ttk.LabelFrame(
            self.tab_resistors, text=" Select Band Colours "
        )
        self.band_frame.pack(padx=20, pady=10, fill="x")

        # First digit band
        # Job: Select colour for primary digit value
        # Behaviour: 4-band and 5-band both start with first
        # digit bands, so this control is always visible
        tk.Label(self.band_frame, text="Band 1:", bg=self.jb_white).grid(
            row=0, column=0, pady=5
        )
        self.b1 = ttk.Combobox(
            self.band_frame, values=list(self.colors.keys()), state="readonly"
        )
        self.b1.grid(row=0, column=1)

        # Second digit band
        # Job: Select colour for secondary digit value
        # Behaviour: 4-band and 5-band both have a second
        # digit band, so this control is always visible
        tk.Label(self.band_frame, text="Band 2:", bg=self.jb_white).grid(
            row=1, column=0, pady=5
        )
        self.b2 = ttk.Combobox(
            self.band_frame, values=list(self.colors.keys()), state="readonly"
        )
        self.b2.grid(row=1, column=1)

        # Third digit band (only used for 5-band resistors)
        # Job: Select colour for tertiary digit value
        # Behaviour: 5-band resistors have an extra digit,
        # so this control is shown/hidden based on selected mode
        self.b3_label = tk.Label(self.band_frame, text="Band 3:", bg=self.jb_white)
        self.b3 = ttk.Combobox(
            self.band_frame, values=list(self.colors.keys()), state="readonly"
        )

        # Multiplier band
        # Job: Select colour for multiplier (power of 10)
        # Behaviour: The multiplier band scales the base value by factors of 10
        tk.Label(self.band_frame, text="Multiplier:", bg=self.jb_white).grid(
            row=3, column=0, pady=5
        )
        self.b_mult = ttk.Combobox(
            self.band_frame, values=list(self.multipliers.keys()), state="readonly"
        )
        self.b_mult.grid(row=3, column=1)

        # Tolerance band (accuracy of the resistor)
        # Job: Select colour for tolerance (±%)
        # Behaviour: Tolerance shows how closely the actual resistance matches the label
        tk.Label(self.band_frame, text="Tolerance:", bg=self.jb_white).grid(
            row=4, column=0, pady=5
        )
        self.b_tol = ttk.Combobox(
            self.band_frame, values=list(self.tolerances.keys()), state="readonly"
        )
        self.b_tol.grid(row=4, column=1)

        # Calculation and output controls
        # Job: Start calculation and display results
        self.calc_resistor_btn = tk.Button(
            self.tab_resistors, text="Calculate Resistance", command=self.calc_resistor
        )
        self.style_button(self.calc_resistor_btn)
        self.calc_resistor_btn.pack(pady=10)
        self.res_output = tk.Label(
            self.tab_resistors,
            text="Results will appear here...",
            font=("Arial", 12, "bold"),
            fg=self.jb_dark_blue,
        )
        self.res_output.pack(pady=10)

        # Initialize UI based on selected mode (4-band or 5-band)
        # Behaviour: Called before user interaction to set initial state
        self.toggle_bands()

    def toggle_bands(self):
        """
        Show or hide the third digit band based on resistor mode selection.

        Job: Dynamically show/hide based on resistor type
        Behaviour: 4-band resistors don't have a third digit, so hiding the control
        prevents confusion and reduces unnecessary input fields.
        When user switches modes, this function is automatically called to update the interface.
        """
        if self.resistor_mode.get() == "4":
            self.b3_label.grid_remove()
            self.b3.grid_remove()
        else:
            self.b3_label.grid(row=2, column=0, pady=5)
            self.b3.grid(row=2, column=1)

    def calc_resistor(self):
        """
        Calculate resistor value and tolerance range from selected colour bands.

        Converts selected band colours to their numeric values, combines digits,
        applies multiplier, and calculates resistance range based on tolerance.

        Formula:
            Base Value = d1 * 10 + d2 (4-band) or d1 * 100 + d2 * 10 + d3 (5-band)
            Total Ohms = Base Value * Multiplier
            Tolerance Range = Total Ohms ± (Total Ohms * tolerance%)

        Job: Perform colour code to resistance value calculation and display results
        Behaviour: Showing the calculated resistance value and tolerance range
        to the user helps them understand the component's specifications.

        Error handling:
            messagebox.showerror: If not all bands are selected
        """
        try:
            # Extract digit values from colour selections
            d1 = str(self.colors[self.b1.get()])
            d2 = str(self.colors[self.b2.get()])
            mult = self.multipliers[self.b_mult.get()]
            tol = self.tolerances[self.b_tol.get()]

            # Combine digit bands into base value
            # Job: Form the base resistance number from digit bands
            # Behaviour: In 4-band mode, digits are 2 figures; in 5-band, 3 figures
            if self.resistor_mode.get() == "5":
                d3 = str(self.colors[self.b3.get()])
                base_value = int(d1 + d2 + d3)  # 3-digit number for 5-band resistors
            else:
                base_value = int(d1 + d2)  # 2-digit number for 4-band resistors

            # Apply multiplier to get final resistance in Ohms
            # Job: Scale base value by power of 10 from multiplier band
            total_ohms = base_value * mult

            # Format output with appropriate unit (Ω, kΩ, MΩ)
            # Job: Display resistance in readable format
            # Behaviour: Large resistance values are more readable when shown in kΩ or MΩ
            display_val = f"{total_ohms:g} Ω"
            if total_ohms >= 1000000:
                display_val = f"{total_ohms / 1000000:g} MΩ"
            elif total_ohms >= 1000:
                display_val = f"{total_ohms / 1000:g} kΩ"

            # Calculate tolerance range
            # Job: Calculate min/max resistance from tolerance percentage
            # Behaviour: Real resistors vary from calculated values; tolerance bands allow
            # users to check if measured resistance is within specification
            variation = total_ohms * (tol / 100)
            lower = total_ohms - variation
            upper = total_ohms + variation

            # Display results with tolerance range
            self.res_output.config(
                text=f"Value: {display_val} ±{tol}%\nRange: {lower:g}Ω to {upper:g}Ω",
                fg="blue",
            )

        except (KeyError, ValueError, TypeError):
            # Ensure all bands are selected before calculation
            messagebox.showerror("Error", "Please select a colour for all bands.")

    def setup_quiz_ui(self):
        """
        Quiz & History tab interface.

        Creates question display area with multiple-choice buttons, controls for
        starting quiz, progress indicator, and a history log viewer
        that reads/writes quiz results to a file.

        Job: Implements test to check learning with learning progress tracking
        Behaviour: Quizzes reinforce learning through active recall. History
        tracking allows students to review their progression over time.
        """
        # Quiz section title
        tk.Label(
            self.tab_quiz,
            text="Mastery Quiz: Electronics Basics",
            font=("Arial", 14, "bold"),
            fg=self.jb_dark_blue,
        ).pack(pady=10)

        # Question display container
        # Job: Shows current question text during quiz
        self.quiz_frame = ttk.LabelFrame(self.tab_quiz, text=" Question ")
        self.quiz_frame.pack(padx=20, pady=10, fill="both", expand=True)

        self.q_label = tk.Label(
            self.quiz_frame,
            text="Click 'Start Quiz' to begin!",
            font=("Arial", 11),
            wraplength=450,
            bg=self.jb_white,
            fg=self.jb_dark_blue,
        )
        self.q_label.pack(pady=20)

        # Multiple choice answer buttons container
        # Job: Display four answer options for each question
        # Behaviour: Four options provide reasonable difficulty
        self.ans_frame = tk.Frame(self.quiz_frame)
        self.ans_frame.pack(pady=10)

        self.ans_buttons = []
        for i in range(4):
            btn = tk.Button(
                self.ans_frame,
                text="",
                width=30,
                command=lambda i=i: self.check_answer(i),
            )
            self.style_button(btn)  # Apply JackBord styling to the button
            btn.pack(pady=2)
            self.ans_buttons.append(btn)
            btn.config(state="disabled")  # Disabled until quiz starts

        # Quiz start button and progress display
        # Job: Show score and question count + trigger quiz start
        # Behaviour: Allow users to start when ready and helps them track performance
        self.start_btn = tk.Button(
            self.tab_quiz, text="Start Quiz", command=self.start_quiz
        )
        self.style_button(self.start_btn)  # Apply JackBord styling to the button
        self.start_btn.pack(pady=5)
        self.progress_label = tk.Label(
            self.tab_quiz, text="Question 0 of 10 | Score: 0"
        )
        self.progress_label.pack()

        # History tracking and review section
        # Job: Display previous quiz attempts from log file
        # Behaviour: Historical data helps students see
        # progression and identify areas for improvement
        hist_box = ttk.LabelFrame(
            self.tab_quiz, text=" Quiz Attempt History (Log File) "
        )
        hist_box.pack(padx=20, pady=10, fill="both", expand=True)

        self.history_text = tk.Text(
            hist_box, height=8, state="disabled", font=("Courier", 9)
        )
        self.history_text.pack(padx=10, pady=5, fill="both", expand=True)

        # History management buttons
        btn_row = tk.Frame(hist_box)
        btn_row.pack(pady=5)
        self.refresh_btn = tk.Button(
            btn_row, text="Refresh History", command=self.load_history
        )
        self.style_button(self.refresh_btn)
        self.refresh_btn.pack(side="left", padx=5)
        self.clear_btn = tk.Button(
            btn_row, text="Clear History File", command=self.clear_history_file
        )
        self.style_button(self.clear_btn)
        self.clear_btn.pack(side="left", padx=5)

        self.load_history()  # Load existing history

    def start_quiz(self):
        """
        Start a new quiz attempt.

        Resets score and question index, enables answer buttons,
        disables start/restart button, and displays the first question.

        Job: Prepare the UI for quiz interaction
        """
        self.current_q_index = 0  # Start at question 0
        self.score = 0  # Reset score to 0
        for btn in self.ans_buttons:
            btn.config(state="normal")  # Enable all answer buttons
        self.start_btn.config(state="disabled")  # Prevent multiple quiz starts
        self.show_question()  # Display first question

    def show_question(self):
        """
        Display current question and shuffle its answer options.

        Shows the current question text and shuffles its four answer options
        into the answer buttons. When all questions are answered, saves the
        result and ends the quiz.

        Job: Display quiz question and randomized options for each attempt
        Behaviour: Shuffling options prevents pattern recognition and ensures
        students understand concepts rather than memorizing option positions.
        """
        if self.current_q_index < len(self.quiz_questions):
            # Retrieve current question data
            q_data = self.quiz_questions[self.current_q_index]
            self.q_label.config(text=f"Q{self.current_q_index + 1}: {q_data['q']}")

            # Randomize answer order to prevent position-based guessing
            # Job: Shuffle answer options for variety
            # Behaviour: Different orderings on repeated attempts for genuine understanding
            options = list(q_data["o"])
            random.shuffle(options)

            # Update button labels with shuffled options
            for i, opt in enumerate(options):
                self.ans_buttons[i].config(text=opt)

            # Update progress display
            self.progress_label.config(
                text=f"Question {self.current_q_index + 1} of 10 | Score: {self.score}"
            )
        else:
            # Save and show results after quiz is completed
            self.save_result_to_file()
            self.end_quiz()

    def check_answer(self, idx):
        """
        Check selected answer and advance to next question.

        Compares user's selected answer button text against the correct answer.
        Adds to score if correct, then moves to the next question.

        Integer:
            idx (int): Index of clicked answer button (0-3)

        Job: Process answer selection and track score
        Behaviour: Button index is converted to button text because answer options
        are shuffled, so the correct answer position varies by question.
        """
        # Check if selected button text matches the correct answer
        if (
            self.ans_buttons[idx].cget("text")
            == self.quiz_questions[self.current_q_index]["a"]
        ):
            self.score += 1  # Adds to score on correct answer

        # Advance to next question
        self.current_q_index += 1
        self.show_question()  # Display next question or end quiz if finished

    def end_quiz(self):
        """
        Display quiz results and status.

        Shows pass/fail status and percentage score in colour-coded message.
        Disables answer buttons, re-enables start button for restart, and refreshes
        the history display to display the current attempt.

        Job: Displays quiz outcome and status feedback
        Behaviour: 70% pass threshold (7/10). Colour coding for
        displaying status (green=success, red=needs improvement).
        """
        # Determine pass/fail based on standard (70%)
        pass_mark = 7  # 70% of 10 questions is standard threshold for passing
        percent = (self.score / 10) * 100

        # Display result message with appropriate feedback and colour
        if self.score >= pass_mark:
            msg = f"PASS! You scored {percent}%\nYou are ready to use the JackBord."
            color = "green"
        else:
            msg = (
                f"FAIL. You scored {percent}%\nYou need at "
                f"least 70% to pass. Please review the tabs and "
                f"try again."
            )
            color = "red"

        # Update UI to show results
        self.q_label.config(text=msg, fg=color, font=("Arial", 12, "bold"))

        # Disable answer buttons and clear their text
        for btn in self.ans_buttons:
            btn.config(text="", state="disabled")

        # Re-enable start button for quiz retake
        self.start_btn.config(state="normal", text="Retake Quiz")

        # Refresh history display to show new attempt
        self.load_history()

    def save_result_to_file(self):
        """
        Append current quiz attempt result to history log file.

        Records timestamp, score, and pass/fail status in 'quiz_log.txt'.
        Uses append mode instead of writing mode to preserve all historical attempts.

        Job: Check quiz results and save to .txt file
        Behaviour: Allows students to track progress over time.
        File-based logging is simple, and allows for application restarts.
        """
        # Generate timestamped entry with score and pass/fail status
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        status = "PASS" if self.score >= 7 else "FAIL"
        entry = f"[{timestamp}] Score: {self.score}/10 | {status}\n"

        # Append entry to log file (creates one if it doesn't exist)
        with open("quiz_log.txt", "a", encoding="utf-8") as file:
            file.write(entry)

    def load_history(self):
        """
        Load and display quiz attempt history from log file.

        Reads quiz_log.txt if it exists and displays all previous attempts.
        If no history file exists, displays a placeholder message.

        Job: Retrieve and render persistent quiz data
        Behaviour: Displaying history helps students track their learning trajectory
        and see improvement over multiple quiz attempts.
        """
        # Enable text widget for editing (display mode)
        self.history_text.config(state="normal")
        self.history_text.delete("1.0", tk.END)  # Clear previous content

        # Read and display history file if it exists
        if os.path.exists("quiz_log.txt"):
            with open("quiz_log.txt", "r", encoding="utf-8") as file:
                self.history_text.insert(tk.END, file.read())
        else:
            # Message if no attempts yet
            self.history_text.insert(tk.END, "No history found.")

        # Disable text widget for viewing only which prevents accidental editing
        self.history_text.config(state="disabled")

    def clear_history_file(self):
        """
        Clear all quiz attempt history from log file.

        Prompts user for confirmation before deleting quiz_log.txt content.
        After confirmation, overwrites file with empty content and refreshes display.

        Job: Allow users to reset quiz history
        Behaviour: Confirmation window prevents accidental data loss.
        Resetting history can be useful for fresh starts.
        """
        # Ask user for confirmation before destructive operation
        if messagebox.askyesno("Confirm", "Wipe the history log?"):
            # Overwrite file with empty content to clear history
            open("quiz_log.txt", "w", encoding="utf-8").close()
            # Refresh display to show empty history
            self.load_history()

    def setup_help_ui(self):
        """
        Help & Documentation tab

        Creates a read-only text display with user guide covering the main tools:
        Power Calculator, Unit Converter, Resistor Calculator, and Mastery Quiz.

        Job: Provides help and documentation
        Behaviour: In-app documentation reduces the need for external resources.
        """
        # Documentation container
        help_box = ttk.LabelFrame(self.tab_help, text=" Help & Documentation ")
        help_box.pack(padx=20, pady=20, fill="both", expand=True)

        # Read-only text widget for documentation display
        help_text = tk.Text(
            help_box,
            wrap="word",
            bg=self.jb_white,
            fg=self.jb_dark_blue,
            font=("Arial", 10),
            relief="flat",
        )
        help_text.pack(fill="both", expand=True, padx=10, pady=10)

        # Comprehensive user guide with tool descriptions
        doc_text = (
            "JACKBORD TOOLKIT USER DOCUMENTATION\n\n"
            "1. POWER CALCULATOR:\n"
            "Enter Voltage (V) and Current (I). Choose mA or A.\n"
            "The tool calculates Power (W) and warns you if "
            "the current exceeds the 500mA JackBord limit.\n\n"
            "2. UNIT CONVERTER:\n"
            "Convert values between Micro, Milli, Base, Kilo, and Mega.\n"
            "Useful for resistor values and converting units.\n\n"
            "3. RESISTOR CALCULATOR:\n"
            "Select 4-band or 5-band mode. Choose the colour bands that match a resistor\n"
            "to calculate its resistance and tolerance range.\n\n"
            "4. MASTERY QUIZ:\n"
            "Answer 10 questions to test your electronics "
            "knowledge. A score of 7/10 (70%) or more\n"
            "earns a PASS. All attempts are saved to "
            "quiz_log.txt for review."
        )

        # Insert documentation and disable editing
        help_text.insert(tk.END, doc_text)
        help_text.config(
            state="disabled"
        )  # Read-only prevents any accidental modifications


if __name__ == "__main__":
    root = tk.Tk()
    app = RoboticsToolkit(root)
    root.mainloop()  # Begin event loop - application runs until window is closed
