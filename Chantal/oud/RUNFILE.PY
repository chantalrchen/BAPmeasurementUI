import tkinter as tk
from tkinter import messagebox, ttk
import propar   # Bronkhorst MFC
import serial   # Cooling and Valve
import time 
import json
import os
import threading

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
                self.massflow += (self.targetmassflow - self.massflow) * 0.1
                if abs(self.massflow - self.targetmassflow) < 0.001:
                    self.massflow = self.targetmassflow
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
            messagebox.showerror("Error", "The Bronkhorst MFCs is not connected.")
            return False  # Operation failed
        ##

    def disconnect(self):
        self.connected = False
        self.instrument = None

class Koelingsblok:
    def __init__(self, port = 'COM4'):
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
                        self.temperature += (self.targettemperature - self.temperature) * 0.1
                        if abs(self.temperature - self.targettemperature) < 0.001:
                            self.temperature = self.targettemperature
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

    def set_temperature(self, value: float, temp_ambient):

        ##the following should be connected when connected with the Torrey Pines IC20XR Digital Chilling/Heating Dry Baths
        #if self.connected and self.instrument is not None: 
        if self.connected:
            try:
                #the cooling system can only lower the temperature by 30 degrees below ambient
                min_temp = temp_ambient - 30
                print(temp_ambient, min_temp)
                if value < min_temp:
                    print("hoi")
                    messagebox.showwarning("Value exceeds the minimum temperature", f"The ambient temperature is {temp_ambient:.2f}. The temperature may not exceed {min_temp:.2f} °C")
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
    def __init__(self, port = "COM5"):
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


class ProfileManagerBase:
    def __init__(self, name, profiles_dir, device):
        self.name = name
        self.profiles_dir = os.path.join(profiles_dir, f"profiles_{name.lower()}")
        self.device = device
        self.current_profile = None
        self.standard_profiles = self._get_default_profiles()

        if not os.path.exists(self.profiles_dir):
            os.makedirs(self.profiles_dir)

        for name, value in self.standard_profiles.items():
            file_path = os.path.join(self.profiles_dir, f"{name}.json")
            if not os.path.exists(file_path):
                self.save_profile(name, value)

    def _get_default_profiles(self):
        return {}

    def get_profiles(self):
        return sorted([f[:-5] for f in os.listdir(self.profiles_dir) if f.endswith('.json')])

    def load_profile(self, name):
        file_path = os.path.join(self.profiles_dir, f"{name}.json")
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                self.current_profile = json.load(file)
                return self.current_profile
        return None

    def save_profile(self, name, profile_data):
        file_path = os.path.join(self.profiles_dir, f"{name}.json")
        with open(file_path, 'w') as file:
            json.dump(profile_data, file, indent=4)
        return True

    def delete_profile(self, name):
        file_path = os.path.join(self.profiles_dir, f"{name}.json")
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False

    def run_profile(self, temp_ambient=None):
        if not self.device.connected:
            messagebox.showerror("Error", f"{self.name} device is not connected")
            return False

        if not self.current_profile:
            messagebox.showerror("Error", "No profile loaded")
            return False

        steps = sorted(self.current_profile.get("steps", []), key=lambda x: x["time"])
        if not steps:
            messagebox.showerror("Error", "Profile has no steps")
            return False

        start_time = time.time()
        current_index = 0

        while current_index < len(steps):
            elapsed = time.time() - start_time
            if current_index < len(steps) - 1 and elapsed >= steps[current_index + 1]["time"]:
                current_index += 1

            step = steps[current_index]
            self.apply_step(step, temp_ambient)

            if current_index == len(steps) - 1 and elapsed >= step["time"]:
                break

        return True

    def apply_step(self, step, temp_ambient):
        pass  # Implement in subclasses


class MFCProfileManager(ProfileManagerBase):
    def __init__(self):
        mfcs = [BronkhorstMFC("COM1"), BronkhorstMFC("COM2"), BronkhorstMFC("COM3")]
        super().__init__("MFC", "profiles_onetab", mfcs)
        self.mfcs = mfcs  # Store for access in UI

    def _get_default_profiles(self):
        return {
            "Flow_Test MFC": {
                "description": "Test flow rate changes",
                "steps": [
                    {"time": 0, "flow mfc1": 0.5, "flow mfc2": 0.5, "flow mfc3": 0.5},
                    {"time": 10, "flow mfc1": 1.0, "flow mfc2": 0.5, "flow mfc3": 0.5},
                    {"time": 20, "flow mfc1": 1.5, "flow mfc2": 0.5, "flow mfc3": 0.5},
                    {"time": 30, "flow mfc1": 1.0, "flow mfc2": 0.5, "flow mfc3": 0.5},
                    {"time": 40, "flow mfc1": 0.5, "flow mfc2": 0.5, "flow mfc3": 0.5}
                ]
            }
        }

    def apply_step(self, step, temp_ambient=None):
        for i, key in enumerate(["flow mfc1", "flow mfc2", "flow mfc3"]):
            if key in step:
                self.device[i].set_massflow(step[key])


class CoolingProfileManager(ProfileManagerBase):
    def __init__(self):
        cooling = Koelingsblok("COM4")
        super().__init__("Cooling", "profiles_onetab", cooling)
        self.cooling = cooling
    def _get_default_profiles(self):
        return {
            "Flow_Test COOLING": {
                "description": "Test cooling profile",
                "steps": [
                    {"time": 0, "temperature": 25},
                    {"time": 10, "temperature": 25},
                    {"time": 20, "temperature": 25},
                    {"time": 30, "temperature": 25},
                    {"time": 40, "temperature": 25}
                ]
            }
        }

    def apply_step(self, step, temp_ambient=None):
        if "temperature" in step and temp_ambient is not None:
            self.device.set_temperature(step["temperature"], temp_ambient)


class ValveProfileManager(ProfileManagerBase):
    def __init__(self):
        valve = RVM("COM5")
        super().__init__("Valve", "profiles_onetab", valve)
        self.valve = valve
    def _get_default_profiles(self):
        return {
            "Flow_Test VALVE": {
                "description": "Test valve switching",
                "steps": [
                    {"time": 0, "valve": 1},
                    {"time": 10, "valve": 1},
                    {"time": 20, "valve": 1},
                    {"time": 30, "valve": 1},
                    {"time": 40, "valve": 1}
                ]
            }
        }

    def apply_step(self, step, temp_ambient=None):
        if "valve" in step:
            self.device.set_valve(step["valve"])

class AutomatedSystemUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Automated System")
        self.root.geometry("1400x800")

        # Initialize managers
        self.mfc_manager = MFCProfileManager()
        self.cooling_manager = CoolingProfileManager()
        self.valve_manager = ValveProfileManager()

        # Device references
        self.mfcs = self.mfc_manager.mfcs
        self.cooling = self.cooling_manager.cooling
        self.valve = self.valve_manager.valve

        self.ambient_temp = None

        # Create UI layout
        self.setup_ui()

        # Periodic update for device readings
        self.update_readings()

    def setup_ui(self):
        # Header
        header = ttk.Frame(self.root)
        header.pack(fill='x', padx=10, pady=5)

        self.status_var = tk.StringVar(value="Status: Idle")
        ttk.Label(header, textvariable=self.status_var).pack(side='left')

        # Ambient temperature input
        temp_frame = ttk.Frame(header)
        temp_frame.pack(side='right')
        ttk.Label(temp_frame, text="Ambient Temp (C):").pack(side='left')
        self.ambient_temp_var = tk.DoubleVar()
        ttk.Entry(temp_frame, textvariable=self.ambient_temp_var, width=5).pack(side='left')
        ttk.Button(temp_frame, text="Set", command=self.set_ambient_temp).pack(side='left')

        # Tabs
        self.tabs = ttk.Notebook(self.root)
        self.tabs.pack(fill='both', expand=True)

        self.create_profile_tab("MFC", self.mfc_manager, ["time", "flow mfc1", "flow mfc2", "flow mfc3"])
        self.create_profile_tab("Cooling", self.cooling_manager, ["time", "temperature"])
        self.create_profile_tab("Valve", self.valve_manager, ["time", "valve"])

    def set_ambient_temp(self):
        try:
            self.ambient_temp = self.ambient_temp_var.get()
            self.status_var.set(f"Ambient temperature set to {self.ambient_temp:.2f} °C")
        except tk.TclError:
            messagebox.showerror("Error", "Invalid ambient temperature")

    def create_profile_tab(self, name, manager, fields):
        frame = ttk.Frame(self.tabs)
        self.tabs.add(frame, text=f"{name} Profiles")

        left = ttk.Frame(frame)
        left.pack(side='left', fill='y')
        right = ttk.Frame(frame)
        right.pack(side='right', fill='both', expand=True)

        # Profile list
        listbox = tk.Listbox(left)
        listbox.pack(fill='y', expand=True)
        for profile in manager.get_profiles():
            listbox.insert(tk.END, profile)

        def load():
            selected = listbox.curselection()
            if selected:
                name = listbox.get(selected[0])
                manager.load_profile(name)
                self.status_var.set(f"Loaded {name} profile")

        def run():
            if self.ambient_temp is None:
                messagebox.showerror("Error", "Set ambient temperature first")
                return
            threading.Thread(target=manager.run_profile, args=(self.ambient_temp,), daemon=True).start()
            self.status_var.set(f"Running {name} profile")

        ttk.Button(left, text="Load", command=load).pack(fill='x')
        ttk.Button(left, text="Run", command=run).pack(fill='x')

        # Step view (read-only)
        tree = ttk.Treeview(right, columns=fields, show='headings')
        for field in fields:
            tree.heading(field, text=field)
            tree.column(field, width=100)
        tree.pack(fill='both', expand=True)

    def update_readings(self):
        # This function can be enhanced to show live updates
        self.root.after(1000, self.update_readings)

def main():
    root = tk.Tk()
    app = AutomatedSystemUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()
