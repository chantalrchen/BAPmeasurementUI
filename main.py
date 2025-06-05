import tkinter as tk
# from uiscrollable import AutomatedSystemUI
from uiscrollable_2valves import AutomatedSystemUI
if __name__ == "__main__":
    root = tk.Tk()
    
    root.state("zoomed")
    
    app = AutomatedSystemUI(root)
    root.mainloop()


##VRAGEN
##ALS VALVE POSITION OP UIT STAAT, MOET HET DAN OOK NOG CONCENTRATIE GEVEN?
    