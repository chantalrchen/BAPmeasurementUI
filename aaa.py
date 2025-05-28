import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.geometry("1000x400")
root.title("Scrollable UI Example")

# Main container
main_frame = tk.Frame(root)
main_frame.pack(fill="both", expand=1)

# Canvas for scrolling
canvas = tk.Canvas(main_frame)
canvas.pack(side="left", fill="both", expand=1)

# Scrollbar
scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
scrollbar.pack(side="right", fill="y")

# Configure canvas and scrollbar
canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

# Frame inside canvas
scrollable_frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

# Add a bunch of widgets inside the scrollable frame
for i in range(50):
    ttk.Label(scrollable_frame, text=f"Widget {i+1}").pack(pady=5)

root.mainloop()
