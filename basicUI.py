import tkinter as tk
from tkinter import messagebox, ttk
import propar   # Bronkhorst MFC
import serial   # Cooling and Valve
import time 
import json
import os

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
        #     messagebox.showerror("Error", "The Bronkhorst MFC is not connected.")
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
        #     messagebox.showerror("Error", "The Bronkhorst MFC is not connected.")
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
            messagebox.showerror("Error","The Bronkhorst MFC is not connected.")
            return False  # Operation failed

    def set_massflow(self, value: float):
        ##the following should be connected when connected with Bronkhorst MFC
        #if self.connected and self.instrument is not None:  # device is connected and assigned
        
        if self.connected:
            try:
                if value < 0:
                    messagebox.showwarning("Mass flow rate can't be negative", f"The mass flow rate can't be negative.")
                    return False             
                elif value > self.maxmassflow:
                    messagebox.showwarning("Value exceeds the maximum mass flow rate", f"The mass flow rate may not exceed {self.maxmassflow:.2f} mL/min. The mass flow rate will be set to {self.maxmassflow:.2f} mL/min.")
                    self.targetmassflow = self.maxmassflow
                    ##the following should be connected when connected with Bronkhorst MFC
                    #self.instrument.writeParameter(206, self.maxmassflow)
                    return True
                else:
                    self.targetmassflow = value
                    ##the following should be connected when connected with Bronkhorst MFC
                    #self.instrument.writeParameter(206, value) #Fsetpoint
                return True  # successful operation
            except Exception as err:
                messagebox.showerror("Error",
                    f"An error occurred while setting the mass flow rate: {err}"
                )
                return False  # Operation failed
        else:
            messagebox.showerror("Error", "The Bronkhorst MFC is not connected.")
            return False  # Operation failed
        ##

    def disconnect(self):
        self.connected = False
        self.instrument = None

class Koelingsblok:
    def __init__(self, port = 'COM2'):
        self.port = port
        self.connected = False
        self.instrument = None
        self.temperature = 0
        self.targettemperature = 0
        self.dummy = 0;
    
    def connect(self):
        
        # ##the following should be connected when connected with the Torrey Pines IC20XR Digital Chilling/Heating Dry Baths
        # # p24: 9600 baud, 1 stop bit, no parity, no hardware handshake, 100ms delay after each command sent (after \r)
        # # 100 ms delay, so a timeout of 1s should be enough
        # try:
        #     self.instrument = serial.Serial(self.port, 9600, timeout = 1)
        #     self.connected = True
        #     return self.connected
        # except Exception as err:
        #     messagebox.showerror("Error",
        #         f"An error occurred while connecting the Torrey Pines IC20XR Digital Chilling/Heating Dry Baths: {err}"
        #     )
        # return False  # Operation failed
        # ##
        
        ##the following is used only for simulation
        self.connected = True
        return self.connected
        ##
    
    def disconnect(self):
        self.connected = False
        self.instrument = None
        
    def get_temperature(self, dummy):
    
        # ##the following should be connected when connected with the Torrey Pines IC20XR Digital Chilling/Heating Dry Baths
        # if self.connected and self.instrument is not None: 
        #     try:
        #         # sending a request to read the temperature; The current plate temperature will be returned in a text string terminated by <CR><LF>, e.g. 14.3\r
        #         self.instrument.write(b"p\r")  
        #         # 100ms delay after each command sent (after \r)
        #         time.sleep(0.1)  
        #         self.response = self.instrument.read_until(b"\r").decode().strip()  # reads until \r
        #         return self.response
        #     except Exception as err:
        #         messagebox.showerror("Error",
        #             f"An error occurred while getting the temperature: {err}"
        #         )
        #         return False  # Operation failed
        # else:
        #     return False #Operation failed
        # ##
        
            ##the following is used only for simulation
            if dummy == 0:
                return self.temperature
            elif dummy == 1:                
                if self.connected:
                    try:
                        if self.temperature < self.targettemperature:
                            self.temperature += (self.targettemperature - self.temperature)/10
                            return self.temperature
                        elif self.temperature > self.targettemperature:
                            self.temperature -= (self.targettemperature - self.temperature)/10
                            return self.temperature
                        else:
                            return self.temperature
                    except Exception as err:
                        messagebox.showerror("Error",
                            f"An error occurred while reading the temperature: {err}"
                        )
                        return False
                else:
                    messagebox.showerror("Error","The Torrey Pines IC20XR Digital Chilling/Heating Dry Baths is not connected.")
                    return False  # Operation failed
        ##

    def set_temperature(self, value: float):

        ##the following should be connected when connected with the Torrey Pines IC20XR Digital Chilling/Heating Dry Baths
        #if self.connected and self.instrument is not None: 
        if self.connected:
            current_temp = self.get_temperature(0)
            try:
                #the cooling system can only lower the temperature by 30 degrees below ambient
                min_temp = current_temp - 30
                if value < min_temp:
                    messagebox.showwarning("Value exceeds the minimum temperature", f"The ambient temperature is {current_temp:.2f}. The temperature may not exceed {min_temp:.2f} °C")
                    self.targettemperature = min_temp
                    ##the following should be connected when connected with the Torrey Pines IC20XR Digital Chilling/Heating Dry Baths
                    # self.instrument.write(b"n" + str(min_temp).encode() + "\r") 
                    
                    #if the above does not work, try: 
                    # self.instrument.write(f"n{value}\r".encode()) 
                    # 100ms delay after each command sent (after \r)
                    time.sleep(0.1) 
                    return True
                else:
                    self.targettemperature = value
                    ##the following should be connected when connected with the Torrey Pines IC20XR Digital Chilling/Heating Dry Baths
                    # self.instrument.write(b"n" + str(value).encode() + "\r") 
                    
                    #if the above does not work, try: self.instrument.write(f"n{value}\r".encode()) 
                    # 100ms delay after each command sent (after \r)
                    time.sleep(0.1) 
                    return True
            except Exception as err:
                messagebox.showerror("Error",
                    f"An error occurred while setting the temperature: {err}"
                )
                return False  # Operation failed
        else:
            messagebox.showerror("Error", "The Torrey Pines IC20XR Digital Chilling/Heating Dry Baths is not connected.")
            return False #Operation failed

class RVM:
    def __init__(self, port = "COM3"):
        self.port = port
        self.connected = False
        self.instrument = None
        self.currentposition = 0

    def connect(self):
        # ##the following should be connected when connected with Bronkhorst MFC
        # try:
        #     self.instrument = serial.Serial(self.port, 9600, 8, None, 1, 1000)
        #     # Baudrate = 9600, Data bits = 8, Parity = None, Stop bit = 1, Timeout = 1000 sec!!!!;
        #     ##TIMEOUT SHOULD BE CHANGED AFTER WE KNOW WHAT KIND OF RVM IT IS!!!!
        #     self.connected = True
        # except Exception as err:
        #     messagebox.showerror("Error",
        #         f"An error occurred while connecting the RVM Industrial Microfluidic Rotary Valve: {err}"
        #     )
        # return False  # Operation failed
        # ##
        
        ##the following is used only for simulation
        self.connected = True
        return self.connected
        ##
    
    def disconnect(self):
        self.connected = False
        self.instrument = None
    
    def initialize_valve(self):
        #when the instrument is connected use the following
        #if self.connected and self.instrument is not None:
        
        if self.connected:
            try:
                self.instrument.write(b"/1ZR\r")
                self.currentposition = 1
                return True
            except Exception as err:
                messagebox.showerror("Error",
                    f"An error occurred while initializing the valve: {err}"
                )
                return False
        else:
            return False #Operation Failed
    
    def set_valve(self, position: int):
        #when the instrument is connected use the following
        #if self.connected and self.instrument is not None:
        
        if self.connected:
            if position != 1 and position != 2:
                messagebox.showerror("Error",
                    f"The position of the valve can only be 1 or 2, but received: {position}"
                )
                return False
            
            try:
                #self.instrument.write(b"/1b" + str(position).encode() + "R\r")
                #if the above does not work, try: 
                # self.instrument.write(f"/1b{position}R\r".encode()) 
                self.currentposition = position
                return True
            except Exception as err:
                messagebox.showerror("Error",
                    f"An error occurred while setting the position of the valve: {err}"
                )
                return False  # Operation failed
        else:
            messagebox.showerror("Error", "RVM Industrial Microfluidic Rotary Valve is not connected.")
            return False #Operation failed

    def current_valve_position(self):
        # Following when connected to the devices
        # self.instrument.write(b"/1?6R\r")  
        ##TIMEOUT SHOULD BE CHANGED AFTER WE KNOW WHAT KIND OF RVM IT IS!!!!
        #time.sleep(0.1)  
        
        # Read response
        #valve_position =  self.instrument.readline().decode().strip()
        
        ##this is pure to simulate
        valve_position = self.currentposition
        return valve_position

class MicrofluidicGasSupplySystemUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Microfluidic Gas Supply System")
        self.root.geometry("1000x700")
        
        # Initialize the devices
        self.MFC = BronkhorstMFC()
        self.cooling = Koelingsblok()
        self.valve = RVM()
        self.profiledata = ProfileData()
        
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True)

        self.create_menu()
        self.create_MFC_tab()
        self.create_cooling_tab()
        self.create_valve_tab()
 
    def create_menu(self):
        menu = tk.Menu(self.root)
        
        # Settings menu
        settings_menu = tk.Menu(menu, tearoff=0)
        settings_menu.add_command(label="Communication Settings", command=self.com_settings)
        menu.add_cascade(label="Settings", menu=settings_menu)
        
        self.root.config(menu=menu)
        
    def create_MFC_tab(self):
        MFC_tab = ttk.Frame(self.notebook)
        MFC_tab.pack(fill='both', expand=True)
        self.notebook.add(MFC_tab, text="Bronkhorst MFC")
        
        # label for the mass flow rate
        massflow_label = tk.Label(MFC_tab, text="Mass flow rate (mL/min):")
        massflow_label.grid(row=0, column=0, padx=10, pady=10)
        
        # entry field for mass flow rate 
        self.massflow_var = tk.DoubleVar()
        massflow_entry = tk.Entry(MFC_tab, textvariable=self.massflow_var)
        massflow_entry.grid(row=0, column=1, padx=10, pady=10)
        
        # button to set the mass flow rate
        set_massflow_button = tk.Button(MFC_tab, text="Set mass flow rate", command=self.set_MFCmassflow)
        set_massflow_button.grid(row=1, column=0, columnspan=2, pady=10)
        
        # Label to display the current flow rate
        self.current_massflow_label = tk.Label(MFC_tab, text="Current mass flow rate: Not available")
        self.current_massflow_label.grid(row=2, column=0, padx=10, pady=10)
        
        # Label to display the target flow rate
        self.target_massflow_label = tk.Label(MFC_tab, text=f"Target mass flow rate: {self.MFC.targetmassflow:.2f} mL/min")
        self.target_massflow_label.grid(row=2, column=1, padx=10, pady=10)
        
        # Connect button
        MFC_connect_button = tk.Button(MFC_tab, text="Connect", command=self.connect_MFC)
        MFC_connect_button.grid(row=3, column=0, padx=10, pady=10)
        
        # Disconnect button
        MFC_disconnect_button = tk.Button(MFC_tab, text="Disconnect", command=self.disconnect_MFC)
        MFC_disconnect_button.grid(row=3, column=1, padx=10, pady=10)
        
        # Connection info label at the bottom
        MFC_connection_info_label = ttk.Label(MFC_tab, text="Current connection ports: ")
        MFC_connection_info_label.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

        # Label to show the current port for MFC at the bottom
        self.MFC_current_port_label = ttk.Label(MFC_tab, text=f"MFC Port: {self.MFC.port}, Connected: {self.MFC.connected}")
        self.MFC_current_port_label.grid(row=5, column=0, columnspan=2, padx=10, pady=5)

    def create_cooling_tab(self):
        cooling_tab = ttk.Frame(self.notebook)
        cooling_tab.pack(fill='both', expand=True)
        self.notebook.add(cooling_tab, text="Torrey Pines IC20XR Digital Chilling/Heating Dry Baths")
        
        # label for the mass flow rate
        temperature_label = tk.Label(cooling_tab, text="Temperature (°C):")
        temperature_label.grid(row=0, column=0, padx=10, pady=10)
        
        # entry field for mass flow rate 
        self.temperature_var = tk.DoubleVar()
        temperature_entry = tk.Entry(cooling_tab, textvariable=self.temperature_var)
        temperature_entry.grid(row=0, column=1, padx=10, pady=10)
        
        # button to set the mass flow rate
        set_temperature_button = tk.Button(cooling_tab, text="Set temperature", command=self.set_temperature)
        set_temperature_button.grid(row=1, column=0, columnspan=2, pady=10)
        
        # Label to display the current flow rate
        self.current_temperature_label = tk.Label(cooling_tab, text="Current temperature: Not available")
        self.current_temperature_label.grid(row=2, column=0, padx=10, pady=10)
        
        # Label to display the target flow rate
        self.target_temperature_label = tk.Label(cooling_tab, text=f"Target temperature: {self.cooling.targettemperature:.2f} °C")
        self.target_temperature_label.grid(row=2, column=1, padx=10, pady=10)
    
        # Connect button
        cooling_connect_button = tk.Button(cooling_tab, text="Connect", command=self.connect_cooling)
        cooling_connect_button.grid(row=3, column=0, padx=10, pady=10)
        
        # Disconnect button
        cooling_disconnect_button = tk.Button(cooling_tab, text="Disconnect", command=self.disconnect_cooling)
        cooling_disconnect_button.grid(row=3, column=1, padx=10, pady=10)
        
        # Connection info label at the bottom
        cooling_connection_info_label = ttk.Label(cooling_tab, text="Current connection ports: ")
        cooling_connection_info_label.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

        # Label to show the current port for cooling at the bottom
        self.cooling_current_port_label = ttk.Label(cooling_tab, text=f"Cooling Port: {self.cooling.port}, Connected: {self.cooling.connected}")
        self.cooling_current_port_label.grid(row=5, column=0, columnspan=2, padx=10, pady=5)
    
    def create_valve_tab(self):
        valve_tab = ttk.Frame(self.notebook)
        valve_tab.pack(fill='both', expand=True)
        self.notebook.add(valve_tab, text="RVM Industrial Microfluidic Rotary Valve")
        
        # label for the mass flow rate
        valve_label = tk.Label(valve_tab, text="Position of the Valve:")
        valve_label.grid(row=0, column=0, padx=10, pady=10)
        
        # entry field for mass flow rate 
        self.valve_pos_var = tk.DoubleVar()
        valve_pos_entry = tk.Entry(valve_tab, textvariable=self.valve_pos_var)
        valve_pos_entry.grid(row=0, column=1, padx=10, pady=10)
        
        # button to set the position of the valve
        set_valve_button = tk.Button(valve_tab, text="Set valve", command=self.set_valve)
        set_valve_button.grid(row=1, column=0, columnspan=2, pady=10)
        
        # Label to display the current position of the valve
        self.current_valve_label = tk.Label(valve_tab, text="Current position of the valve: Not available")
        self.current_valve_label.grid(row=2, column=0, padx=10, pady=10)
        
        # Connect button
        valve_connect_button = tk.Button(valve_tab, text="Connect", command=self.connect_valve)
        valve_connect_button.grid(row=3, column=0, padx=10, pady=10)
        
        # Disconnect button
        valve_disconnect_button = tk.Button(valve_tab, text="Disconnect", command=self.disconnect_valve)
        valve_disconnect_button.grid(row=3, column=1, padx=10, pady=10)
        
        # Connection info label at the bottom
        valve_connection_info_label = ttk.Label(valve_tab, text="Current connection ports: ")
        valve_connection_info_label.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

        # Label to show the current port for valve at the bottom
        self.valve_current_port_label = ttk.Label(valve_tab, text=f"RVM Port: {self.valve.port}, Connected: {self.valve.connected}")
        self.valve_current_port_label.grid(row=5, column=0, columnspan=2, padx=10, pady=5)
        
    def connect_MFC(self):
        if self.MFC.connect():
            messagebox.showinfo("Connection", "MFC successfully connected.")
            #updating the connection info
            self.MFC_current_port_label.config(text=f"MFC Port: {self.MFC.port}, Connected: {self.MFC.connected}") 
    
    def disconnect_MFC(self):
        self.MFC.disconnect()
        messagebox.showinfo("Disconnected", "MFC disconnected successfully.")
        #updating the connection info
        self.MFC_current_port_label.config(text=f"MFC Port: {self.MFC.port}, Connected: {self.MFC.connected}") 
    
    def connect_cooling(self):  
        if self.cooling.connect():
            messagebox.showinfo("Connection", "Torrey Pines IC20XR Digital Chilling/Heating Dry Baths successfully connected.")
            #updating the connection info
            self.cooling_current_port_label.config(text=f"Cooling Port: {self.cooling.port}, Connected: {self.cooling.connected}") 
            
    def disconnect_cooling(self):
        self.cooling.disconnect()
        messagebox.showinfo("Disconnected", "Torrey Pines IC20XR Digital Chilling/Heating Dry Baths disconnected successfully.")
        #updating the connection info
        self.cooling_current_port_label.config(text=f"Cooling Port: {self.cooling.port}, Connected: {self.cooling.connected}") 

    def connect_valve(self):  
        if self.valve.connect():
            messagebox.showinfo("Connection", "RVM Industrial Microfluidic Rotary valve is successfully connected.")
            #updating the connection info
            self.valve_current_port_label.config(text=f"RVM Port: {self.valve.port}, Connected: {self.valve.connected}") 
            
    def disconnect_valve(self):
        self.valve.disconnect()
        messagebox.showinfo("Disconnected", "RVM Industrial Microfluidic Rotary valve is disconnected successfully.")
        #updating the connection info
        self.valve_current_port_label.config(text=f"RVM Port: {self.valve.port}, Connected: {self.valve.connected}") 
             
    def com_settings(self):
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Connection Settings")
        settings_window.geometry("400x300")
        #this forces all focus on the top level until Toplevel is closed
        settings_window.grab_set()
        
        # Bronkhorst MFC settings
        MFC_frame = ttk.LabelFrame(settings_window, text="Bronkhorst MFC")
        MFC_frame.pack(fill="both", padx=10, pady=10)
        
        ttk.Label(MFC_frame, text="Port:").grid(row=0, column=0, padx=5, pady=5)
        MFC_port_var = tk.StringVar(value=self.MFC.port)
        MFC_port_entry = ttk.Entry(MFC_frame, textvariable=MFC_port_var)
        MFC_port_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Cooling settings
        cooling_frame = ttk.LabelFrame(settings_window, text="Torrey Pines IC20XR Digital Chilling/Heating Dry Baths")
        cooling_frame.pack(fill="both", padx=10, pady=10)
        
        ttk.Label(cooling_frame, text="Port:").grid(row=1, column=0, padx=5, pady=5)
        cooling_port_var = tk.StringVar(value=self.cooling.port)
        cooling_port_entry = ttk.Entry(cooling_frame, textvariable=cooling_port_var)
        cooling_port_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # valve settings
        valve_frame = ttk.LabelFrame(settings_window, text="RVM Industrial Microfluidic Rotary valve ")
        valve_frame.pack(fill="both", padx=10, pady=10)
        
        ttk.Label(valve_frame, text="Port:").grid(row=2, column=0, padx=5, pady=5)
        valve_port_var = tk.StringVar(value=self.valve.port)
        valve_port_entry = ttk.Entry(valve_frame, textvariable=valve_port_var)
        valve_port_entry.grid(row=2, column=1, padx=5, pady=5)
        
        def save_settings():
            #updating the connection info
            self.MFC.port = MFC_port_var.get()
            self.cooling.port = cooling_port_var.get()
            self.valve.port = valve_port_var.get()

            self.MFC_current_port_label.config(text=f"MFC Port: {self.MFC.port}, Connected: {self.MFC.connected}") 
            self.cooling_current_port_label.config(text=f"Cooling Port: {self.cooling.port}, Connected: {self.cooling.connected}") 
            self.valve_current_port_label.config(text=f"RVM Port: {self.valve.port}, Connected: {self.valve.connected}")  
            
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
        
    def set_temperature(self):
        temperature = self.temperature_var.get()
        if self.cooling.set_temperature(temperature):
            self.target_temperature_label.config(text=f"Target temperature: {self.cooling.targettemperature:.2f} °C")
            self.update_temperature()
        else:
            self.current_temperature_label.config(text="Failed to set the temperature.")
    
    def update_temperature(self):
        current_temp = self.cooling.get_temperature(1)
        if current_temp is not None:
            self.current_temperature_label.config(text=f"Current temperature: {current_temp:.2f} °C")
        else:
            self.current_temperature_label.config(text="Failed to read the temperature.")
        
        self.root.after(1000, self.update_temperature) #updating the temperature each 1s.
        
    def set_valve(self):
        position = self.valve_pos_var.get()
        if self.valve.set_valve(position):
            self.update_valve()

    def update_valve(self):
        current_position = self.valve.current_valve_position()
        if current_position is not None:
            self.current_valve_label.config(text=f"Current position of the valve: {current_position}")
        else:
            self.current_valve_label.config(text="Failed to read the position of the valve.")

def main():
    root = tk.Tk()
    app = MicrofluidicGasSupplySystemUI(root)
    root.mainloop()
    
if __name__ == "__main__":
    main()
