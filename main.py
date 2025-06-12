import tkinter as tk
from ui import AutomatedSystemUI
import tkinter.messagebox
from tkinter import font
import tkinter.ttk as ttk
# This code has been written by C.R. Chen and F.Lin for the BAP project E-nose.

##To use this application
# install the following packages: pip install bronkhorst-propar, pyserial, matplotlib 

def on_closing():
    """ Messagebox to ask the user whether they want to close the app before exiting it to prevent accident closure 

    Reference: https://stackoverflow.com/questions/26168967/invalid-command-name-while-executing-after-script
    """
    response= tkinter.messagebox.askyesno('Exit','Are you sure you want to exit?')
    if response:
        root.withdraw()
        root.quit()
        
if __name__ == "__main__":
    root = tk.Tk()
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    #When opening the UI ensuring it is full screen
    root.state("zoomed")

#    # Lettertype voor standaard tkinter widgets
#     default_font = font.nametofont("TkDefaultFont")
#     default_font.configure(family="Arial", size=10)
#     root.option_add("*Font", default_font)

#     # Lettertype voor ttk widgets (zoals ttk.Label, ttk.Entry, etc.)
#     style = ttk.Style()
#     style.configure(".", font=("Arial", 10))

#     root.option_add("*Font", default_font)

    app = AutomatedSystemUI(root)
    root.mainloop()