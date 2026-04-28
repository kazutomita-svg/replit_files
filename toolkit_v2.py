# Robotics & Electronics Toolkit Version 2
import tkinter as tk
from tkinter import ttk

# 1. Setup the window
root = tk.Tk()
root.title("Robotics Toolkit V2 - Tabbed Interface")
root.geometry("400x300")

# 2. Logic: Shared function for testing
def on_click(label_to_update):
    label_to_update.config(text="This is Version 2", fg="blue")

# 3. Create the Tab Controller (Notebook)
notebook = ttk.Notebook(root)
tab1 = ttk.Frame(notebook)
tab2 = ttk.Frame(notebook)

notebook.add(tab1, text="Tab 1")
notebook.add(tab2, text="Tab 2")
notebook.pack(expand=1, fill="both")

# --- Content for Tab 1 ---
label1 = tk.Label(tab1, text="This is Tab 1", font=("Arial", 12))
label1.pack(pady=20)
# Note: We use a 'lambda' so we can tell the function which label to change
btn1 = tk.Button(tab1, text="Press the button", command=lambda: on_click(label1))
btn1.pack(pady=10)

# --- Content for Tab 2 ---
label2 = tk.Label(tab2, text="This is Tab 2", font=("Arial", 12))
label2.pack(pady=20)
btn2 = tk.Button(tab2, text="Press the button", command=lambda: on_click(label2))
btn2.pack(pady=10)

# 4. Start the application
root.mainloop()
