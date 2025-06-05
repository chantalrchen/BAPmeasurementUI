import tkinter as tk
# from ui import AutomatedSystemUI
from uiscrollable import AutomatedSystemUI

if __name__ == "__main__":
    root = tk.Tk()
    
    root.state("zoomed")
    
    app = AutomatedSystemUI(root)
    root.mainloop()


##VRAGEN
##ALS VALVE POSITION OP UIT STAAT, MOET HET DAN OOK NOG CONCENTRATIE GEVEN?
    