import tkinter as tk
from ui import AutomatedSystemUI
# from run import AutomatedSystemUI

if __name__ == "__main__":
    root = tk.Tk()

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    print(screen_width, screen_height)
    root.geometry(f"{screen_width}x{screen_height}")
    
    root.state("zoomed")
    
    app = AutomatedSystemUI(root)
    root.mainloop()
    