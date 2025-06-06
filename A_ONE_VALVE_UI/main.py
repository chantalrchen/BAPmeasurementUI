import tkinter as tk
from A_ONE_VALVE_UI.uiscrollable import AutomatedSystemUI
# from uiscrollable_2valves import AutomatedSystemUI
if __name__ == "__main__":
    root = tk.Tk()
    
    root.state("zoomed")
    
    app = AutomatedSystemUI(root)
    root.mainloop()


##VRAGEN
##ALS VALVE POSITION OP UIT STAAT, MOET HET DAN OOK NOG CONCENTRATIE GEVEN?
    