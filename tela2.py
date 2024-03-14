import tkinter as tk
from tkinter import ttk

def submit_data():
    # Get input values and process data here
    pass

root = tk.Tk()
root.title("Data Entry Form")

# Frame for the form elements
form_frame = ttk.LabelFrame(root, text="Data Entry Form")
form_frame.grid(column=0, row=0, padx=10, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))

# First Name
first_name_label = ttk.Label(form_frame, text="First Name:")
first_name_label.grid(column=0, row=0, padx=5, pady=5, sticky=tk.W)
first_name_entry = ttk.Entry(form_frame)
first_name_entry.grid(column=1, row=0, padx=5, pady=5, sticky=(tk.W, tk.E))

# Last Name
last_name_label = ttk.Label(form_frame, text="Last Name:")
last_name_label.grid(column=0, row=1, padx=5, pady=5, sticky=tk.W)
last_name_entry = ttk.Entry(form_frame)
last_name_entry.grid(column=1, row=1, padx=5, pady=5, sticky=(tk.W, tk.E))

# Email
email_label = ttk.Label(form_frame, text="Email:")
email_label.grid(column=0, row=2, padx=5, pady=5, sticky=tk.W)
email_entry = ttk.Entry(form_frame)
email_entry.grid(column=1, row=2, padx=5, pady=5, sticky=(tk.W, tk.E))

# Phone Number
phone_label = ttk.Label(form_frame, text="Phone Number:")
phone_label.grid(column=0, row=3, padx=5, pady=5, sticky=tk.W)
phone_entry = ttk.Entry(form_frame)
phone_entry.grid(column=1, row=3, padx=5, pady=5, sticky=(tk.W, tk.E))

# Submit Button
submit_button = ttk.Button(form_frame, text="Submit", command=submit_data)
submit_button.grid(column=1, row=4, padx=5, pady=5, sticky=(tk.W, tk.E))

root.mainloop()