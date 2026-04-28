# Robotics & Electronics Toolkit Version 1
import tkinter as tk

# Setup the window
root = tk.Tk()
root.title("Robotics Toolkit V1 - Tkinter")
root.geometry("300x200")

# Output function when button is pressed
def on_click():
    # Changes the text of the label to show it's working
    status_label.config(text="This is Version 1", fg="green")

# Text label to show status
status_label = tk.Label(root, text="Press the button", font=("Arial", 12))
status_label.pack(pady=20)

# Button to trigger the output
test_button = tk.Button(root, text="Press this", command=on_click)
test_button.pack(pady=10)

# Start the code
root.mainloop()
