import tkinter as tk
from tkinter import filedialog
import myCleaner
import os
def on_create_file_click():
    source_file = source_file_var.get()
    dest_folder = dest_folder_var.get()
    selected_color = color_var.get()

    if source_file and dest_folder and selected_color:
        # Logic to remove selected color from PDF and create a new PDF
        dest_folder = os.path.join(dest_folder, "output.pdf")
        myCleaner.remove_color_from_pdf(source_file, dest_folder, selected_color)

        success_label.config(text="File created successfully", fg="green")
    else:
        success_label.config(text="Please select source file, destination folder, and color", fg="red")

def browse_source_file():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if file_path:
        source_file_var.set(file_path)

def browse_dest_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        dest_folder_var.set(folder_path)

# Create the main window
root = tk.Tk()
root.title("PDF Color Removal")
root.geometry("400x400")

# Source file selection box
source_file_var = tk.StringVar()
source_file_entry = tk.Entry(root, textvariable=source_file_var, width=30)
source_file_entry.pack(pady=10)

# Browse button for source file selection
browse_source_button = tk.Button(root, text="Browse Source", command=browse_source_file)
browse_source_button.pack(pady=10)

# Destination folder selection box
dest_folder_var = tk.StringVar()
dest_folder_entry = tk.Entry(root, textvariable=dest_folder_var, width=30)
dest_folder_entry.pack(pady=10)

# Browse button for destination folder selection
browse_dest_button = tk.Button(root, text="Browse Destination", command=browse_dest_folder)
browse_dest_button.pack(pady=10)

# Select menu with color options
color_var = tk.StringVar()
color_var.set("Select Color")  # Default selection

def on_color_change(*args):
    create_file_button.config(state="normal" if color_var.get() else "disabled")
    success_label.config(text="")

color_var.trace_add("write", on_color_change)

color_menu = tk.OptionMenu(root, color_var, "Red", "Blue", "Yellow")
color_menu.pack(pady=10)

# Create file button
create_file_button = tk.Button(root, text="Create File", command=on_create_file_click, state="disabled")
create_file_button.pack(pady=20)

# Success label
success_label = tk.Label(root, text="", fg="green")
success_label.pack(pady=10)

# Run the Tkinter event loop
root.mainloop()
