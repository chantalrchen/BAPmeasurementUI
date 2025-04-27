import tkinter as tk
from tkinter import messagebox, ttk
import propar   # Bronkhorst MFC
import serial   # Cooling and Valve
import time 

class BronkhorstMFC:
    def __init__(self, port = "COM1"):
        self.port = port
        self.connected = False
        self.instrument = None
        self.massflow = 0
        self.targetmassflow = 0
        self.maxmassflow = 2.0

    def connect(self):
        # ##the following should be connected when connected with Bronkhorst MFC
        # try:
        #     self.instrument = propar.instrument(self.port)
        #     self.connected = True
        #     self.ensure_units()
        #     return self.connected
        # except Exception as err:
        #     messagebox.showerror("Error",
        #         f"An error occurred while connecting the Bronkhorst MFC: {err}"
        #     )
        # return False  # Operation failed
        # ##
        
        ##the following is used just for simulating
        self.connected = True
        return self.connected
    
    def ensure_units(self):
        ##the following should be connected when connected with Bronkhorst MFC
        # if self.connected and self.instrument is not None:
        #     unit_index = self.instrument.readParameter(23)
        #     if unit_index != 2:
        #         self.instrument.writeParameter(23, 2)
        #     return True
        # else:
        #     messagebox.showerror("Error", "The device is not connected.")
        #     return False
        ##
        
        ##the following is used just for simulating
        return True
    
    def get_massflow(self):
        ##the following should be connected when connected with Bronkhorst MFC
        # if self.connected and self.instrument is not None:  # device is connected and assigned
        #     try:
        #         self.massflow = self.instrument.readParameter(205) #Fmeasure
        #         return self.massflow  # successful operation
        #     except Exception as err:
        #         messagebox.showerror("Error",
        #             f"An error occurred while reading the mass flow rate: {err}"
        #         )
        #         return False  # Operation failed
        # else:
        #     messagebox.showerror("Error", "The device is not connected.")
        #     return False  # Operation failed
        ##
        
        ##the following is used just for simulating
        if self.connected:
            try:
                if self.massflow < self.targetmassflow:
                    self.massflow += (self.targetmassflow - self.massflow)/10
                elif self.massflow > self.targetmassflow:
                    self.massflow -= (self.targetmassflow - self.massflow)/10
                return self.massflow
            except Exception as err:
                messagebox.showerror("Error",
                    f"An error occurred while reading the mass flow rate: {err}"
                )
                return False
        else:
            messagebox.showerror("Error","The device is not connected.")
            return False  # Operation failed

    def set_massflow(self, value):
        # ##the following should be connected when connected with Bronkhorst MFC
        # if self.connected and self.instrument is not None:  # device is connected and assigned
        #     try:
        #         if value > self.maxmassflow:
        #             messagebox.showwarning("Value exceeds the maximum mass flow rate", f"The mass flow rate may not exceed {self.maxmassflow} mL/min. The mass flow rate will be set to {self.maxmassflow} mL/min.")
        #             self.targetmassflow = self.maxmassflow
        #             self.instrument.writeParameter(206, self.maxmassflow)
        #         else:
        #             self.targetmassflow = value
        #             self.instrument.writeParameter(206, value) #Fsetpoint
        #         return True  # successful operation
        #     except Exception as err:
        #         messagebox.showerror("Error",
        #             f"An error occurred while setting the mass flow rate: {err}"
        #         )
        #         return False  # Operation failed
        # else:
        #     messagebox.showerror("Error", "The device is not connected.")
        #     return False  # Operation failed
        # ##
        
        ##the following is used only for simulation
        if self.connected:
            try:
                if value > self.maxmassflow:
                    messagebox.showwarning("Value exceeds the maximum mass flow rate", f"The mass flow rate may not exceed {self.maxmassflow} mL/min. The mass flow rate will be set to {self.maxmassflow} mL/min.")
                    self.targetmassflow = self.maxmassflow
                    return True
                else:
                    self.targetmassflow = value
                    return True
            except Exception as err:
                messagebox.showerror("Error",
                    f"An error occurred while setting the mass flow rate: {err}"
                )
                return False  # Operation failed
        else:
            messagebox.showerror("Error", "The device is not connected.")
            return False  # Operation failed

    def disconnect(self):
        self.connected = False
        self.instrument = None

class MicrofluidicGasSupplySystemUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Microfluidic Gas Supply System")
        self.root.geometry("1000x700")
        
        # Initialize the devices
        self.MFC = BronkhorstMFC()
        
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill = 'both', expand = True)
        
        # self.Cooling_tab = ttk.Frame(self.notebook)
        # self.Cooling_tab.pack(fill = 'both', expand = True)
        # self.notebook.add(self.Cooling_tab, text = "Torrey Pines IC20XR Digital Chilling/Heating Dry Baths")
        
        # self.RVM_tab = ttk.Frame(self.notebook)
        # self.RVM_tab.pack(fill = 'both', expand = True)
        # self.notebook.add(self.RVM_tab, text = "RVM Industrial Microfluidic Rotary Valve")
        
        self.create_menu()
        self.create_MFC_tab()
    
    def create_menu(self):
        menu = tk.Menu(self.root)
        
        # Settings menu
        settings_menu = tk.Menu(menu, tearoff=0)
        settings_menu.add_command(label="Communication Settings", command=self.com_settings)
        menu.add_cascade(label="Settings", menu=settings_menu)
        
        self.root.config(menu=menu)
        
    def create_MFC_tab (self):
        self.MFC_tab = ttk.Frame(self.notebook)
        self.MFC_tab.pack(fill = 'both', expand = True)
        self.notebook.add(self.MFC_tab, text = "Bronkhorst MFC")
        
        # label for the mass flow rate
        self.massflow_label = tk.Label(self.MFC_tab, text="Mass flow rate (mL/min):")
        self.massflow_label.grid(row=0, column=0, padx=10, pady=10)
        
        # entry field for mass flow rate 
        self.massflow_var = tk.DoubleVar()
        self.massflow_entry = tk.Entry(self.MFC_tab, textvariable=self.massflow_var)
        self.massflow_entry.grid(row=0, column=1, padx=10, pady=10)
        
        # button to set the mass flow rate
        self.set_massflow_button = tk.Button(self.MFC_tab, text="Set mass flow rate", command=self.set_MFCmassflow)
        self.set_massflow_button.grid(row=1, column=0, columnspan=2, pady=10)
        
        # Label to display the current flow rate
        self.current_massflow_label = tk.Label(self.MFC_tab, text="Current mass flow rate: Not available")
        self.current_massflow_label.grid(row=2, column=0, padx=10, pady=10)
        
        # Label to display the target flow rate
        self.target_massflow_label = tk.Label(self.MFC_tab, text=f"Target mass flow rate: {self.MFC.targetmassflow} mL/min")
        self.target_massflow_label.grid(row=2, column=1, padx=10, pady=10)
        
        #Connect button
        self.connect_button = tk.Button(self.MFC_tab, text="Connect", command=self.connect_devices)
        self.connect_button.grid(row=3, column=0, padx=10, pady=10)
        
        # Disconnect button
        self.disconnect_button = tk.Button(self.MFC_tab, text="Disconnect", command=self.disconnect_devices)
        self.disconnect_button.grid(row=3, column=1, padx=10, pady=10)
        
        # Connection info label at the bottom
        connection_info_label = ttk.Label(self.MFC_tab, text="Current connection ports: ")
        connection_info_label.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

        # Label to show the current port for MFC at the bottom
        self.current_port_label = ttk.Label(self.MFC_tab, text=f"MFC Port: {self.MFC.port}, Connected: {self.MFC.connected}")
        self.current_port_label.grid(row=5, column=0, columnspan=2, padx=10, pady=5)

        
    def connect_devices(self):
        if self.MFC.connect():
            messagebox.showinfo("Connection", "MFC successfully connected.")
            #updating the connection info
            self.current_port_label.config(text=f"MFC Port: {self.MFC.port}, Connected: {self.MFC.connected}") 
            
    def disconnect_devices(self):
        self.MFC.disconnect()
        messagebox.showinfo("Disconnected", "MFC disconnected successfully.")
        #updating the connection info
        self.current_port_label.config(text=f"MFC Port: {self.MFC.port}, Connected: {self.MFC.connected}") 

    def com_settings(self):
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Connection Settings")
        settings_window.geometry("400x300")
        #this forces all focus on the top level until Toplevel is closed
        settings_window.grab_set()
        
        # Bronkhorst MFC settings
        MFC_frame = ttk.LabelFrame(settings_window, text="Bronkhorst MFC")
        MFC_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(MFC_frame, text="Port:").grid(row=0, column=0, padx=5, pady=5)
        MFC_port_var = tk.StringVar(value=self.MFC.port)
        MFC_port_entry = ttk.Entry(MFC_frame, textvariable=MFC_port_var)
        MFC_port_entry.grid(row=0, column=1, padx=5, pady=5)
        
        def save_settings():
            self.MFC.port = MFC_port_var.get()
            #updating the connection info
            self.current_port_label.config(text=f"MFC Port: {self.MFC.port}, Connected: {self.MFC.connected}") 
    
        save_button = ttk.Button(settings_window, text="Save", command=save_settings)
        save_button.pack(pady=10)
        
    def set_MFCmassflow(self):
        massflowrate = self.massflow_var.get()
        if self.MFC.set_massflow(massflowrate):
            self.target_massflow_label.config(text=f"Target mass flow rate: {self.MFC.targetmassflow} mL/min")
            self.update_massflow()
        else:
            self.current_massflow_label.config(text="Failed to set mass flow rate.")
            
    def update_massflow(self):
        current_flow = self.MFC.get_massflow()
        if current_flow is not None:
            self.current_massflow_label.config(text=f"Current mass flow rate: {current_flow:.2f} mL/min")
        else:
            self.current_massflow_label.config(text="Failed to read mass flow rate.")
        
        self.root.after(1000, self.update_massflow) #updating the MFC flow rate reading each 1s
        
def main():
    root = tk.Tk()
    app = MicrofluidicGasSupplySystemUI(root)
    root.mainloop()
    
if __name__ == "__main__":
    main()


# #########################################
# ##Cooling: the cooling system can lower the temperature maximum by 30 \textcelsius below the ambient temperature
# Cooling_port = "COM2"
# Cooling_instrument = serial.Serial(
#     Cooling_port, 9600, timeout=1
# )  # p24: 9600 baud, 1 stop bit, no parity, no hardware handshake, 100ms delay after each command sent (after \r)
# # 100 ms delay, so a timeout of 1s should be enough

# # Reading the temperature
# Cooling_instrument.write(
#     b"p\r"
# )  # sending a request to read the temperature; The current plate temperature will be returned in a text string terminated by <CR><LF>, e.g. 14.3\r
# time.sleep(0.1)  # 100ms delay after each command sent (after \r)
# response = Cooling_instrument.read_until(b"\r").decode().strip()  # reads until \r


# # Setting the temperature
# Cooling_instrument.write(b"n20\r")  # setting the temperature to 20 degrees
# time.sleep(0.1)  # 100ms delay after each command sent (after \r)

# ####################################3
# ##Valve: 4-ports but actually only has 2 directions
# # Connecting the valve with the dedicated port
# RVM_port = "COM3"
# RVM_instrument = serial.Serial(
#     RVM_port, 9600, 8, None, 1, 1000
# )  # Baudrate = 9600, Data bits = 8, Parity = None, Stop bit = 1, Timeout = 1000 sec!!!!;
# ##TIMEOUT SHOULD BE CHANGED AFTER WE KNOW WHAT KIND OF RVM IT IS!!!!

# # Initializing the valve, Once it is done, the valve is positioned on port 1 (opened)
# RVM_instrument.write(b"/1ZR\r")

# # Position 1: connects port 1 - port 2 and port 3- port 4
# RVM_instrument.write(b"/1b1R\r")
# # Position 2: connects port 2 - port 3 and port 1 - port 4
# RVM_instrument.write(b"/1b2R\r")
