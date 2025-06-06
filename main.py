import tkinter as tk
from ui import AutomatedSystemUI

##To use this application
# install the following packages: pip install bronkhorst-propar, pyserial, matplotlib, pandas 

if __name__ == "__main__":
    root = tk.Tk()
    
    root.state("zoomed")
    
    app = AutomatedSystemUI(root)
    root.mainloop()