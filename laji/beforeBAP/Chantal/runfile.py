import tkinter as tk
from tkinter import messagebox, ttk
import propar   # Bronkhorst MFC
import serial   # Cooling and Valve
import time 
import json
import os
import threading

class BronkhorstMFC:
    def __init__(self, port):
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
            messagebox.showerror("Error", "The Bronkhorst MFCs is not connected.")
            return False  # Operation failed
        ##

    def disconnect(self):
        self.connected = False
        self.instrument = None

class Koelingsblok:
    def __init__(self, port):
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
    def __init__(self, port):
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

class ProfileManager:
    def __init__(self, root, profiles_dir = 'profiles_onetab', dev_data_dir = 'devices_data'):
        #profiles_dir is the path where the profile will be saved
        self.root = root
        self.current_profile = None
        self.current_dev_data = None
        self.standard_profiles = {
            "Flow_Test": {
                "description": "Test flow rate changes",
                "steps": [
                    {"time": 0, "flow mfc1": 0.5, "flow mfc2": 0.5, "flow mfc3": 0.5,"temperature": 25, "valve": 1},
                    {"time": 10, "flow mfc1": 1.0, "flow mfc2": 0.5, "flow mfc3": 0.5,"temperature": 25, "valve": 1},
                    {"time": 20, "flow mfc1": 1.5, "flow mfc2": 0.5, "flow mfc3": 0.5,"temperature": 25, "valve": 1},
                    {"time": 30, "flow mfc1 ": 1.0, "flow mfc2": 0.5, "flow mfc3": 0.5, "temperature": 25, "valve": 1},
                    {"time": 40, "flow": 0.5, "flow mfc2": 0.5, "flow mfc3": 0.5, "temperature": 25, "valve": 1}
                ]
            }
        }

        self.dev_data = {
            "connections": {
                "mfc1_port": "COM1",
                "mfc2_port": "COM2",
                "mfc3_port": "COM3",
                "cooling_device_port": "COM4",
                "valve_port": "COM5",
                "profiles_dir": "profiles_onetab",
                "dev_data_dir": "devices_data"
            }
        }
        
        self.profiles_dir = profiles_dir
        self.dev_data_dir = dev_data_dir
        self.mfcs = [
            BronkhorstMFC(port=self.dev_data["connections"]["mfc1_port"]),
            BronkhorstMFC(port=self.dev_data["connections"]["mfc2_port"]),
            BronkhorstMFC(port=self.dev_data["connections"]["mfc3_port"])
            ]
        self.cooling = Koelingsblok(port=self.dev_data["connections"]["cooling_device_port"])
        self.valve = RVM(port=self.dev_data["connections"]["valve_port"])
        # Create profiles directory if it doesn't exist
        if not os.path.exists(profiles_dir):
            os.makedirs(profiles_dir)
            
        # Save standard profiles if they don't exist
        #https://www.geeksforgeeks.org/python-dictionary-values/
        for name, value in self.standard_profiles.items():
            #Obtaining the name of the profile and the value of the profile
            file_path = os.path.join(self.profiles_dir, f"{name}.json")
            
            #We want to overwrite an already existing profile
            if not os.path.exists(file_path):
                self.save_profile(name, value)
    
    def get_profiles(self):
        """Return a list of available profile names"""
        profiles = []
        #List all the files in directory
        for filename in os.listdir(self.profiles_dir):
            if filename.endswith('.json'):
                profiles.append(filename[:-5])  # Remove .json extension
        return sorted(profiles) #Returning in alphabetical order
    

    def load_profile(self, name):
        """Load a profile by name and set it as current profile"""
        file_path = os.path.join(self.profiles_dir, f"{name}.json")
        if os.path.exists(file_path):
            ## https://www.geeksforgeeks.org/reading-and-writing-json-to-a-file-in-python/
            with open(file_path, 'r') as openfile:
                self.current_profile = json.load(openfile)
                return self.current_profile
        return None
        
    def save_profile(self, name, profile_data):
        """Save a profile to disk"""
        file_path = os.path.join(self.profiles_dir, f"{name}.json")
        ## https://www.geeksforgeeks.org/reading-and-writing-json-to-a-file-in-python/
        with open(file_path, 'w') as outfile:
            json.dump(profile_data, outfile, indent=4)
        return True
    
    def delete_profile(self, name):
        """Delete a profile from disk"""
        file_path = os.path.join(self.profiles_dir, f"{name}.json")
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False

    def run_profile(self):
        """Run the current profile with the given device controllers"""
        # Ensuring that the MFC, cooling and valve are all connected
        print(self.mfcs[0].port, self.mfcs[1].port, self.mfcs[2].port, self.cooling.port, self.valve.port)
        print(self.mfcs[0].connected , self.mfcs[1].connected , self.mfcs[2].connected , self.cooling.connected , self.valve.connected)
        if not (self.mfcs[0].connected and self.mfcs[1].connected and self.mfcs[2].connected and self.cooling.connected and self.valve.connected):
            print("return")
            return False
        if not self.current_profile:
            messagebox.showerror("Error", "No profile loaded")
            return False
        steps = self.current_profile.get("steps", [])
        if not steps:
            messagebox.showerror("Error", "Profile has no steps")
            return False
        # Sort steps by time
        steps = sorted(steps, key=lambda x: x["time"])
        
        start_time = time.time()
        current_step_index = 0
        profile_complete = False
        while not profile_complete:
            elapsed_time = time.time() - start_time
            # Check if we need to move to next step
            if current_step_index < len(steps) - 1:
                next_step_time = steps[current_step_index + 1]["time"]
                if elapsed_time >= next_step_time:
                    current_step_index += 1
            
            # Get current step parameters
            current_step = steps[current_step_index]
            
            # Set devices to current step values
            self.mfcs[0].set_massflow(current_step["flow mfc1"])
            self.mfcs[1].set_massflow(current_step["flow mfc2"])
            self.mfcs[2].set_massflow(current_step["flow mfc3"])
            self.cooling.set_temperature(current_step["temperature"])
            self.valve.set_valve(current_step["valve"])
            
            print(current_step["flow mfc1"], current_step["flow mfc2"], current_step["flow mfc3"], current_step["temperature"], current_step["valve"])
            
            test = self.mfcs[0].get_massflow()
            test2 = self.mfcs[1].get_massflow()
            test3 = self.mfcs[2].get_massflow()
            test4 = self.cooling.get_temperature(1)
            test5= self.valve.current_valve_position()
            
            print(test, test2, test3, test4, test5, "\n \n")
            # #if update_callback is called then we need to update the status with the corresponding data
            # if update_callback:
            #         update_callback({
            #         "elapsed_time": elapsed_time,
            #         "current_step": current_step_index + 1,
            #         "total_steps": len(steps),
            #         "flow mfc1": current_step["flow mfc1"],
            #         "flow mfc2": current_step["flow mfc2"],
            #         "flow mfc3": current_step["flow mfc3"],
            #         "temperature": current_step["temperature"],
            #         "valve": current_step["valve"]
            #     })
            # Check if profile is complete
            if current_step_index == len(steps) - 1 and elapsed_time >= current_step["time"]:
                profile_complete = True
        
        return True
    
    ### Device data, such as paths, ports
    def save_dev_data(self, mfc1port, mfc2port, mfc3port, coolingport, valveport, filename):
        dev_data = {
            "connections": {
            "mfc1_port": mfc1port,
            "mfc2_port": mfc2port,
            "mfc3_port": mfc3port,
            "cooling_device_port": coolingport,
            "valve_port": valveport
        }
        }
        file_path = os.path.join(self.dev_data_dir, f"{filename}.json")
        ## https://www.geeksforgeeks.org/reading-and-writing-json-to-a-file-in-python/
        with open(file_path, 'w') as outfile:
            json.dump(dev_data, outfile, indent=4)
        return True
    
    def load_dev_data(self, name):
        """Load a profile by name and set it as current profile"""
        file_path = os.path.join(self.dev_data_dir, f"{name}.json")
        if os.path.exists(file_path):
            ## https://www.geeksforgeeks.org/reading-and-writing-json-to-a-file-in-python/
            with open(file_path, 'r') as openfile:
                self.current_dev_data = json.load(openfile)
                return self.current_dev_data
        return None
    
    def delete_dev_data(self, name):
        """Delete a profile from disk"""
        file_path = os.path.join(self.dev_data_dir, f"{name}.json")
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False
    
    def get_dev_data(self):
        """Return a list of available profile names"""
        data = []
        #List all the files in directory
        for filename in os.listdir(self.dev_data_dir):
            if filename.endswith('.json'):
                data.append(filename[:-5])  # Remove .json extension
        return sorted(data) #Returning in alphabetical order
    
class AutomatedSystemUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Automated System")
        self.root.geometry("1400x800")
        
        # Initialize the devices
        # self.mfcs = [BronkhorstMFC(port = 'COM1'),  BronkhorstMFC(port = 'COM2'), BronkhorstMFC(port = 'COM3')]
        # self.cooling = Koelingsblok()
        # self.valve = RVM()
        
        self.profilemanager = ProfileManager(self.root)
        
        ##Het volgende is niet zo logisch, alleen als je het niet zo doet, krijg je dus dat profilemanager en UI een andere bronkhorst te pakken gaan krijgen
        ##Daarnaast zijn de porten dan ook niet aligned aahh
        self.mfcs = self.profilemanager.mfcs
        self.cooling = self.profilemanager.cooling
        self.valve = self.profilemanager.valve
        
        # Header frame for connection and status
        header_frame = ttk.Frame(self.root)
        header_frame.pack(side='top', fill='x', padx=5, pady=5)
        
        # Connection status frame
        connection_frame = ttk.Frame(header_frame)
        connection_frame.pack(side='right', padx=10)
        
        # Connection status labels
        self.connection_mfc1_port_label = ttk.Label(connection_frame, 
                                                 text=f"MFC Port: {self.mfcs[0].port}, Connected: {self.mfcs[0].connected}")
        self.connection_mfc1_port_label.pack(fill='both', expand=True)
        
        self.connection_mfc2_port_label = ttk.Label(connection_frame, 
                                                 text=f"MFC Port: {self.mfcs[1].port}, Connected: {self.mfcs[1].connected}")
        self.connection_mfc2_port_label.pack(fill='both', expand=True)
        
        self.connection_mfc3_port_label = ttk.Label(connection_frame, 
                                                 text=f"MFC Port: {self.mfcs[2].port}, Connected: {self.mfcs[2].connected}")
        self.connection_mfc3_port_label.pack(fill='both', expand=True)
        
        # Cooling        
        self.connection_cooling_port_label = ttk.Label(connection_frame, 
                                                     text=f"Cooling Port: {self.cooling.port}, Connected: {self.cooling.connected}")
        self.connection_cooling_port_label.pack(fill='both', expand=True)
        
        self.connection_valve_port_label = ttk.Label(connection_frame, 
                                                  text=f"RVM Port: {self.valve.port}, Connected: {self.valve.connected}")
        self.connection_valve_port_label.pack(fill='both', expand=True)
        
        connect_all_button = ttk.Button(connection_frame, text = "Connect all devices", command = self.connect_all_devices)
        connect_all_button.pack(side='right', padx = 2)
        
        # Status bar, to show what has been adjusted
        # Status label
        self.status_var = tk.StringVar() 
        self.status_var.set("Status:")
        status_bar = ttk.Label(header_frame, text='Status', textvariable=self.status_var)
        status_bar.pack(fill='both', padx=5, pady=5)
        
        self.running_var_bar = tk.Label(header_frame, text="")
        self.running_var_bar.pack(side= 'bottom', fill='x')
        
        # Notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True)

        self.create_menu()
        self.create_device_tab()
        # self.create_MFC_tab()
        # self.create_cooling_tab()
        # self.create_valve_tab()
        self.create_profile_tab()
        
        if self.mfcs[0].connected and self.mfcs[1].connected and self.mfcs[2].connected and self.cooling.connected and self.valve.connected:
            self.update_run_var()
        
        
    def update_run_var(self):
        print("hoi")
        mass_flow_1 = self.mfcs[0].get_massflow()
        mass_flow_2 = self.mfcs[1].get_massflow()
        mass_flow_3 = self.mfcs[2].get_massflow()
        temperature = self.cooling.get_temperature(1)
        valve_position = self.valve.current_valve_position()

        self.running_var_bar.config(text=f"MFC 1 Mass Flow Rate: {mass_flow_1:.2f} mL/min | MFC 2 Mass Flow Rate: {mass_flow_2:.2f} mL/min | MFC 3 Mass Flow Rate: {mass_flow_3:.2f} mL/min | Temperature: {temperature:.2f} °C | Valve Position: {valve_position}")
        print("update_run_var", mass_flow_1, mass_flow_2, mass_flow_3, temperature, valve_position)
        # Schedule the next update (0.01 s)
        self.notebook.after(1, lambda: self.update_run_var)
        
    def create_menu(self):
        menu = tk.Menu(self.root)
        
        # Settings menu
        settings_menu = tk.Menu(menu, tearoff=0)
        settings_menu.add_command(label="Communication Settings", command=self.com_settings)
        menu.add_cascade(label="Settings", menu=settings_menu)
        
        self.root.config(menu=menu)
    
    def create_device_tab(self):
        device_tab = ttk.Frame(self.notebook)
        device_tab.pack(fill='both', expand=True)
        self.notebook.add(device_tab, text="Device Control")
        self.notebook.pack(expand=True, fill='both')
        
        ############	MFC		###########################
        self.mfc_frames = []
        self.massflow_vars = []
        self.current_massflow_labels = []
        self.target_massflow_labels = []
        
        all_mfc_frame = ttk.LabelFrame(device_tab)
        all_mfc_frame.pack(fill='x', padx=10, pady=5)
        
        for index in range(len(self.mfcs)):
            # Create a frame for the MFC
            mfc_frame = ttk.LabelFrame(all_mfc_frame, text=f'MFC {index+1}')
            mfc_frame.grid(row = 0, column = index, padx=10, pady=5)
            self.mfc_frames.append(mfc_frame)  # Store the frame reference

            # Label for mass flow rate
            massflow_label = tk.Label(mfc_frame, text="Mass flow rate (mL/min):")
            massflow_label.grid(row=0, column=0, padx=10, pady=10)

            # Entry field for mass flow rate
            massflow_var = tk.DoubleVar()
            massflow_entry = tk.Entry(mfc_frame, textvariable=massflow_var)
            massflow_entry.grid(row=0, column=1, padx=10, pady=10)
            self.massflow_vars.append(massflow_var)  # Store the variable reference

            # Button to set the mass flow rate
            # lambda: anonymous function means that the function is without a name. 
            # using lambda, such that it doesn't run the function when initiating the program, and passes the value index to the function
            # https://www.geeksforgeeks.org/using-lambda-in-gui-programs-in-python/
            set_massflow_button = tk.Button(mfc_frame, text="Set mass flow rate", command=lambda i = index : self.set_MFCmassflow(i))
            set_massflow_button.grid(row=1, column=0, columnspan=2, pady=10)

            # Label to display the current flow rate
            current_massflow_label = tk.Label(mfc_frame, text="Current mass flow rate: Not available")
            current_massflow_label.grid(row=2, column=0, padx=10, pady=10)
            self.current_massflow_labels.append(current_massflow_label)  # Store the label reference

            # Label to display the target flow rate
            target_massflow_label = tk.Label(mfc_frame, text=f"Target mass flow rate: {self.mfcs[index].targetmassflow:.2f} mL/min")
            target_massflow_label.grid(row=2, column=1, padx=10, pady=10)
            self.target_massflow_labels.append(target_massflow_label)  # Store the label reference

            # Connect button
            MFC_connect_button = tk.Button(mfc_frame, text="Connect", command=lambda i = index :self.connect_MFC(i))
            MFC_connect_button.grid(row=3, column=0, padx=10, pady=10)

            # Disconnect button
            MFC_disconnect_button = tk.Button(mfc_frame, text="Disconnect", command= lambda i = index : self.disconnect_MFC(i))
            MFC_disconnect_button.grid(row=3, column=1, padx=10, pady=10)

        ############	COOLING		###########################
        cooling_frame = ttk.LabelFrame(device_tab, text='Cooling')
        cooling_frame.pack(fill='x', padx=10, pady=5)

		# label for the temp
        temperature_label = tk.Label(cooling_frame, text="Temperature (°C):")
        temperature_label.grid(row=0, column=0, padx=10, pady=10)
        
        # entry field for temp
        self.temperature_var = tk.DoubleVar()
        temperature_entry = tk.Entry(cooling_frame, textvariable=self.temperature_var)
        temperature_entry.grid(row=0, column=1, padx=10, pady=10)
        
        # button to set the temp
        set_temperature_button = tk.Button(cooling_frame, text="Set temperature", command=self.set_temperature)
        set_temperature_button.grid(row=1, column=0, columnspan=2, pady=10)
        
        # Label to display the current temp
        self.current_temperature_label = tk.Label(cooling_frame, text="Current temperature: Not available")
        self.current_temperature_label.grid(row=2, column=0, padx=10, pady=10)
        
        # Label to display the target temp
        self.target_temperature_label = tk.Label(cooling_frame, text=f"Target temperature: {self.cooling.targettemperature:.2f} °C")
        self.target_temperature_label.grid(row=2, column=1, padx=10, pady=10)
    
        # Connect button
        cooling_connect_button = tk.Button(cooling_frame, text="Connect", command=self.connect_cooling)
        cooling_connect_button.grid(row=3, column=0, padx=10, pady=10)
        
        # Disconnect button
        cooling_disconnect_button = tk.Button(cooling_frame, text="Disconnect", command=self.disconnect_cooling)
        cooling_disconnect_button.grid(row=3, column=1, padx=10, pady=10)

        ############	VALVE		###########################
        valve_frame = ttk.LabelFrame(device_tab, text='Valve')
        valve_frame.pack(fill='x', padx=10, pady=5)
        
        # Valve position control
        ttk.Label(valve_frame, text="Valve Position:").grid(row=0, column=0, padx=10, pady=10)
        self.valve_pos_var = tk.IntVar(value=1)
        ttk.Combobox(valve_frame, textvariable=self.valve_pos_var, values=[1, 2], width=5).grid(row=0, column=1, padx=10, pady=10)
        
        # button to set the position of the valve
        set_valve_button = tk.Button(valve_frame, text="Set valve", command=self.set_valve)
        set_valve_button.grid(row=1, column=0, columnspan=2, pady=10)
        
        # Label to display the current position of the valve
        self.current_valve_label = tk.Label(valve_frame, text="Current position of the valve: Not available")
        self.current_valve_label.grid(row=2, column=0, padx=10, pady=10)
        
        # Connect button
        valve_connect_button = tk.Button(valve_frame, text="Connect", command=self.connect_valve)
        valve_connect_button.grid(row=3, column=0, padx=10, pady=10)
        
        # Disconnect button
        valve_disconnect_button = tk.Button(valve_frame, text="Disconnect", command=self.disconnect_valve)
        valve_disconnect_button.grid(row=3, column=1, padx=10, pady=10)
        
    # def create_MFC_tab(self):
    #     MFC_tab = ttk.Frame(self.notebook)
    #     MFC_tab.pack(fill='both', expand=True)
    #     self.notebook.add(MFC_tab, text="Bronkhorst MFC")
        
    #     # label for the mass flow rate
    #     massflow_label = tk.Label(MFC_tab, text="Mass flow rate (mL/min):")
    #     massflow_label.grid(row=0, column=0, padx=10, pady=10)
        
    #     # entry field for mass flow rate 
    #     self.massflow_var = tk.DoubleVar()
    #     massflow_entry = tk.Entry(MFC_tab, textvariable=self.massflow_var)
    #     massflow_entry.grid(row=0, column=1, padx=10, pady=10)
        
    #     # button to set the mass flow rate
    #     set_massflow_button = tk.Button(MFC_tab, text="Set mass flow rate", command=self.set_MFCmassflow)
    #     set_massflow_button.grid(row=1, column=0, columnspan=2, pady=10)
        
    #     # Label to display the current flow rate
    #     self.current_massflow_label = tk.Label(MFC_tab, text="Current mass flow rate: Not available")
    #     self.current_massflow_label.grid(row=2, column=0, padx=10, pady=10)
        
    #     # Label to display the target flow rate
    #     self.target_massflow_label = tk.Label(MFC_tab, text=f"Target mass flow rate: {self.MFC.targetmassflow:.2f} mL/min")
    #     self.target_massflow_label.grid(row=2, column=1, padx=10, pady=10)
        
    #     # Connect button
    #     MFC_connect_button = tk.Button(MFC_tab, text="Connect", command=self.connect_MFC)
    #     MFC_connect_button.grid(row=3, column=0, padx=10, pady=10)
        
    #     # Disconnect button
    #     MFC_disconnect_button = tk.Button(MFC_tab, text="Disconnect", command=self.disconnect_MFC)
    #     MFC_disconnect_button.grid(row=3, column=1, padx=10, pady=10)

        # Connection info label at the bottom
        # MFC_tab_connection_info_label = ttk.Label(MFC_tab, text="Current connection ports: ")
        # MFC_tab_connection_info_label.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

        # MFC_tab_MFC_connection_info_label = ttk.Label(MFC_tab)
        # MFC_tab_MFC_connection_info_label.grid(row=5, column=0, columnspan=2, padx=10, pady=5)
        # MFC_tab_cooling_connection_info_label = ttk.Label(MFC_tab)
        # MFC_tab_cooling_connection_info_label.grid(row=6, column=0, columnspan=2, padx=10, pady=5)
        # MFC_tab_valve_connection_info_label = ttk.Label(MFC_tab)
        # MFC_tab_valve_connection_info_label.grid(row=7, column=0, columnspan=2, padx=10, pady=5)

        # # Label to show the current port for MFC at the bottom
        # self.MFC_tab_MFC_current_port_label = ttk.Label(MFC_tab, text=f"MFC Port: {self.MFC.port}, Connected: {self.MFC.connected}")
        # self.MFC_tab_MFC_current_port_label.grid(row=5, column=1, columnspan=2, padx=10, pady=5)
        # self.MFC_tab_cooling_current_port_label = ttk.Label(MFC_tab, text=f"Cooling Port: {self.cooling.port}, Connected: {self.cooling.connected}")
        # self.MFC_tab_cooling_current_port_label.grid(row=6, column=1, columnspan=2, padx=10, pady=5)
        # self.MFC_tab_valve_current_port_label = ttk.Label(MFC_tab, text=f"RVM Port: {self.valve.port}, Connected: {self.valve.connected}")
        # self.MFC_tab_valve_current_port_label.grid(row=7, column=1, columnspan=2, padx=10, pady=5)
       
    # def create_cooling_tab(self):
    #     cooling_tab = ttk.Frame(self.notebook)
    #     cooling_tab.pack(fill='both', expand=True)
    #     self.notebook.add(cooling_tab, text="Torrey Pines IC20XR Digital Chilling/Heating Dry Baths")
        
    #     # label for the mass flow rate
    #     temperature_label = tk.Label(cooling_tab, text="Temperature (°C):")
    #     temperature_label.grid(row=0, column=0, padx=10, pady=10)
        
    #     # entry field for mass flow rate 
    #     self.temperature_var = tk.DoubleVar()
    #     temperature_entry = tk.Entry(cooling_tab, textvariable=self.temperature_var)
    #     temperature_entry.grid(row=0, column=1, padx=10, pady=10)
        
    #     # button to set the mass flow rate
    #     set_temperature_button = tk.Button(cooling_tab, text="Set temperature", command=self.set_temperature)
    #     set_temperature_button.grid(row=1, column=0, columnspan=2, pady=10)
        
    #     # Label to display the current flow rate
    #     self.current_temperature_label = tk.Label(cooling_tab, text="Current temperature: Not available")
    #     self.current_temperature_label.grid(row=2, column=0, padx=10, pady=10)
        
    #     # Label to display the target flow rate
    #     self.target_temperature_label = tk.Label(cooling_tab, text=f"Target temperature: {self.cooling.targettemperature:.2f} °C")
    #     self.target_temperature_label.grid(row=2, column=1, padx=10, pady=10)
    
    #     # Connect button
    #     cooling_connect_button = tk.Button(cooling_tab, text="Connect", command=self.connect_cooling)
    #     cooling_connect_button.grid(row=3, column=0, padx=10, pady=10)
        
    #     # Disconnect button
    #     cooling_disconnect_button = tk.Button(cooling_tab, text="Disconnect", command=self.disconnect_cooling)
    #     cooling_disconnect_button.grid(row=3, column=1, padx=10, pady=10)
        
        # # Connection info label at the bottom
        # cooling_tab_connection_info_label = ttk.Label(cooling_tab, text="Current connection ports: ")
        # cooling_tab_connection_info_label.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

        # cooling_tab_MFC_connection_info_label = ttk.Label(cooling_tab)
        # cooling_tab_MFC_connection_info_label.grid(row=5, column=0, columnspan=2, padx=10, pady=5)
        # cooling_tab_cooling_connection_info_label = ttk.Label(cooling_tab)
        # cooling_tab_cooling_connection_info_label.grid(row=6, column=0, columnspan=2, padx=10, pady=5)
        # cooling_tab_valve_connection_info_label = ttk.Label(cooling_tab)
        # cooling_tab_valve_connection_info_label.grid(row=7, column=0, columnspan=2, padx=10, pady=5)


        # # Label to show the current port for MFC at the bottom
        # self.cooling_tab_MFC_current_port_label = ttk.Label(cooling_tab, text=f"MFC Port: {self.MFC.port}, Connected: {self.MFC.connected}")
        # self.cooling_tab_MFC_current_port_label.grid(row=5, column=1, columnspan=2, padx=10, pady=5)
        # self.cooling_tab_cooling_current_port_label = ttk.Label(cooling_tab, text=f"Cooling Port: {self.cooling.port}, Connected: {self.cooling.connected}")
        # self.cooling_tab_cooling_current_port_label.grid(row=6, column=1, columnspan=2, padx=10, pady=5)
        # self.cooling_tab_valve_current_port_label = ttk.Label(cooling_tab, text=f"RVM Port: {self.valve.port}, Connected: {self.valve.connected}")
        # self.cooling_tab_valve_current_port_label.grid(row=7, column=1, columnspan=2, padx=10, pady=5)     
    
    # def create_valve_tab(self):
    #     valve_tab = ttk.Frame(self.notebook)
    #     valve_tab.pack(fill='both', expand=True)
    #     self.notebook.add(valve_tab, text="RVM Industrial Microfluidic Rotary Valve")
        
    #     # Valve position control
    #     ttk.Label(valve_tab, text="Valve Position:").grid(row=0, column=0, padx=10, pady=10)
    #     self.valve_pos_var = tk.IntVar(value=1)
    #     ttk.Combobox(valve_tab, textvariable=self.valve_pos_var, values=[1, 2], width=5).grid(row=0, column=1, padx=10, pady=10)
        
    #     # button to set the position of the valve
    #     set_valve_button = tk.Button(valve_tab, text="Set valve", command=self.set_valve)
    #     set_valve_button.grid(row=1, column=0, columnspan=2, pady=10)
        
    #     # Label to display the current position of the valve
    #     self.current_valve_label = tk.Label(valve_tab, text="Current position of the valve: Not available")
    #     self.current_valve_label.grid(row=2, column=0, padx=10, pady=10)
        
    #     # Connect button
    #     valve_connect_button = tk.Button(valve_tab, text="Connect", command=self.connect_valve)
    #     valve_connect_button.grid(row=3, column=0, padx=10, pady=10)
        
    #     # Disconnect button
    #     valve_disconnect_button = tk.Button(valve_tab, text="Disconnect", command=self.disconnect_valve)
    #     valve_disconnect_button.grid(row=3, column=1, padx=10, pady=10)
        
        # Connection info label at the bottom
        # valve_tab_connection_info_label = ttk.Label(valve_tab, text="Current connection ports: ")
        # valve_tab_connection_info_label.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

        # valve_tab_MFC_connection_info_label = ttk.Label(valve_tab)
        # valve_tab_MFC_connection_info_label.grid(row=5, column=0, columnspan=2, padx=10, pady=5)
        # valve_tab_cooling_connection_info_label = ttk.Label(valve_tab)
        # valve_tab_cooling_connection_info_label.grid(row=6, column=0, columnspan=2, padx=10, pady=5)
        # valve_tab_valve_connection_info_label = ttk.Label(valve_tab)
        # valve_tab_valve_connection_info_label.grid(row=7, column=0, columnspan=2, padx=10, pady=5)

        # # Label to show the current port for MFC at the bottom
        # self.valve_tab_MFC_current_port_label = ttk.Label(valve_tab, text=f"MFC Port: {self.MFC.port}, Connected: {self.MFC.connected}")
        # self.valve_tab_MFC_current_port_label.grid(row=5, column=1, columnspan=2, padx=10, pady=5)
        # self.valve_tab_cooling_current_port_label = ttk.Label(valve_tab, text=f"Cooling Port: {self.cooling.port}, Connected: {self.cooling.connected}")
        # self.valve_tab_cooling_current_port_label.grid(row=6, column=1, columnspan=2, padx=10, pady=5)
        # self.valve_tab_valve_current_port_label = ttk.Label(valve_tab, text=f"RVM Port: {self.valve.port}, Connected: {self.valve.connected}")
        # self.valve_tab_valve_current_port_label.grid(row=7, column=1, columnspan=2, padx=10, pady=5)
        
    def create_profile_tab(self):
        profile_tab = ttk.Frame(self.notebook)
        profile_tab.pack(fill = 'both', expand = True)
        self.notebook.add(profile_tab, text = 'Profile Management')
        
        ## Split into two frames
        list_frame = ttk.Frame(profile_tab)
        list_frame.pack(side= 'left', fill = 'both', expand=True, padx=5, pady=5)
        
        edit_frame = ttk.Frame(profile_tab)
        edit_frame.pack(side= 'right', fill= 'both', expand=True, padx=5, pady=5)
        
        ### Left frame / list frame
        ## Profile listbox with scrollbar
        # https://www.pythontutorial.net/tkinter/tkinter-listbox/#adding-a-scrollbar-to-the-listbox
        # Making an empty profile listbox
        self.profile_listbox = tk.Listbox(list_frame, selectmode = tk.SINGLE)
        self.profile_listbox.pack(fill= 'both', expand=True, padx=5, pady=5)
    
        # Putting all the profiles in the profile listbox
        self.update_profile_list()
        
        #Adding a scrollbar to the profile listbox
        v_scrollbar = ttk.Scrollbar(self.profile_listbox, orient = tk.VERTICAL, command = self.profile_listbox.yview)
        
        self.profile_listbox['yscrollcommand'] = v_scrollbar.set
        v_scrollbar.pack(side='right', fill='y')
        
        ##Adding the buttons to the left frame (list frame)
        # Profile list buttons
        button_frame = ttk.Frame(list_frame)
        button_frame.pack(fill='x', padx=5, pady=5)
        
        load_button = ttk.Button(button_frame, text="Load", command=self.load_profile)
        load_button.pack(side='left', padx=3, expand=True)
        
        delete_button = ttk.Button(button_frame, text="Delete", command=self.delete_profile)
        delete_button.pack(side='left', padx=3, expand=True)
        
        ##Right frame / edit frame
        # Profile info
        info_frame = ttk.Frame(edit_frame)
        info_frame.pack(fill='both', padx=5, pady=5)
        
        self.new_profile_label = ttk.Label(info_frame, text="")
        self.new_profile_label.pack(side = 'left', padx=5, expand=True, fill='x')
        
        profile_name_label = ttk.Label(info_frame, text="Name:").pack(side='left')
        self.name_var = tk.StringVar()
        name_entry = ttk.Entry(info_frame, textvariable=self.name_var)
        name_entry.pack(side='left', padx=5, expand=True, fill='x')
        
        profile_desc_label = ttk.Label(info_frame, text="Description:").pack(side='left')
        self.desc_var = tk.StringVar()
        desc_entry = ttk.Entry(info_frame, textvariable=self.desc_var)
        desc_entry.pack(side='left', padx=5, expand=True, fill='x')
        
        new_profile_btn = ttk.Button(info_frame, text = 'New Profile', command = self.create_new_profile)
        new_profile_btn.pack(side='right', padx=3, expand=True)
        
        # Steps in the right/frame
        steps_frame = ttk.Frame(edit_frame)
        steps_frame.pack(fill = 'both' , expand=True, padx=5, pady=5)
        
        #https://tk-tutorial.readthedocs.io/en/latest/tree/tree.html
        self.steps_tree = ttk.Treeview(
            steps_frame, 
            columns=("time", "flow mfc1", "flow mfc2", "flow mfc3", "temp", "valve"), 
            show="headings"
        )
        self.steps_tree.heading("time", text="Time (s)")
        self.steps_tree.heading("flow mfc1", text="Flow MFC 1 (mL/min)")
        self.steps_tree.heading("flow mfc2", text="Flow MFC 2 (mL/min)")
        self.steps_tree.heading("flow mfc3", text="Flow MFC 3 (mL/min)")
        self.steps_tree.heading("temp", text="Temperature (°C)")
        self.steps_tree.heading("valve", text="Valve Position (1 or 2)")
        
        self.steps_tree.column("time", width=80, anchor=tk.CENTER)
        self.steps_tree.column("flow mfc1", width=100, anchor=tk.CENTER)
        self.steps_tree.column("flow mfc2", width=100, anchor=tk.CENTER)
        self.steps_tree.column("flow mfc3", width=100, anchor=tk.CENTER)
        self.steps_tree.column("temp", width=100, anchor=tk.CENTER)
        self.steps_tree.column("valve", width=80, anchor=tk.CENTER)
        
        self.steps_tree.pack(fill = 'both' , expand=True)
        
        step_controls_frame = ttk.Frame(edit_frame)
        step_controls_frame.pack(fill='x', padx=5, pady=5)
        
        self.profile_time_label = ttk.Label(step_controls_frame, text="Time (s):").pack(side='left')
        self.step_time_var = tk.IntVar()
        step_time_entry = ttk.Entry(step_controls_frame, textvariable=self.step_time_var, width=8)
        step_time_entry.pack(side='left', padx=2)
        
        self.profile_mfc1_label = ttk.Label(step_controls_frame, text="Flow MFC 1 (mL/min):").pack(side='left')
        self.step_flow1_var = tk.DoubleVar()
        step_flow1_entry = ttk.Entry(step_controls_frame, textvariable=self.step_flow1_var, width=8)
        step_flow1_entry.pack(side='left', padx=2)

        self.profile_mfc2_label = ttk.Label(step_controls_frame, text="Flow MFC 2 (mL/min):").pack(side='left')
        self.step_flow2_var = tk.DoubleVar()
        step_flow2_entry = ttk.Entry(step_controls_frame, textvariable=self.step_flow2_var, width=8)
        step_flow2_entry.pack(side='left', padx=2)

        self.profile_mfc3_label = ttk.Label(step_controls_frame, text="Flow MFC 3 (mL/min):").pack(side='left')
        self.step_flow3_var = tk.DoubleVar()
        step_flow3_entry = ttk.Entry(step_controls_frame, textvariable=self.step_flow3_var, width=8)
        step_flow3_entry.pack(side='left', padx=2)
        
        self.profile_mfc4_label = ttk.Label(step_controls_frame, text="Temperature (°C):").pack(side='left')
        self.step_temp_var = tk.DoubleVar()
        step_temp_entry = ttk.Entry(step_controls_frame, textvariable=self.step_temp_var, width=8)
        step_temp_entry.pack(side='left', padx=2)
        
        self.profile_valve_label =  ttk.Label(step_controls_frame, text="Valve Position:").pack(side='left')
        self.step_valve_var = tk.IntVar() #integer variable, since the valve should be position on 1/2
        step_valve_combo = ttk.Combobox(
            step_controls_frame, 
            textvariable=self.step_valve_var, 
            values=[1, 2], 
            width=5
        )
        step_valve_combo.pack(side='left', padx=2)
        
        # Step buttons
        step_buttons_frame = ttk.Frame(edit_frame)
        step_buttons_frame.pack(fill='both')
        
        add_step_button = ttk.Button(step_buttons_frame, text="Add Step", command=self.add_step)
        add_step_button.pack(side='left', padx=2)
        
        remove_step_button = ttk.Button(step_buttons_frame, text="Remove Step", command=self.remove_step)
        remove_step_button.pack(side='left', padx=2)
        
        clear_steps_button = ttk.Button(step_buttons_frame, text="Clear All Steps", command=self.clear_steps)
        clear_steps_button.pack(side='left', padx=2)
        
        # Save and run buttons
        action_buttons_frame = ttk.Frame(edit_frame)
        action_buttons_frame.pack(fill='both')
        
        save_button = ttk.Button(action_buttons_frame, text="Save Profile", command=self.save_profile)
        save_button.pack(side='left', padx=2)
        
        run_button = ttk.Button(action_buttons_frame, text="Run Profile", command=self.run_profile)
        run_button.pack(side='left', padx=2)
        
        self.stop_button = ttk.Button(action_buttons_frame, text="Stop", command=self.stop_profile)
        self.stop_button.pack(side='left', padx=2)
        self.stop_button.config(state=tk.DISABLED)
        
        # # Status bar, to show what has been adjusted
        # self.status_var = tk.StringVar() 
        # self.status_bar = ttk.Label(edit_frame, textvariable=self.status_var)
        # self.status_bar.pack(fill='both', padx=5, pady=5)
        
        # Initialize variables
        self.current_loaded_profile = None
        
    def connect_MFC(self, index):
        if self.mfcs[index].connect():
            #messagebox.showinfo("Connection", "MFC successfully connected.")
            #updating the connection info
            self.update_connection_devices()
            self.status_var.set(f"MFC {index + 1} connected")
        else:
            messagebox.showinfo("Connection Failed", f"MFC {index + 1} is not connected")

    def disconnect_MFC(self, index):
        self.mfcs[index].disconnect()
        #messagebox.showinfo("Disconnected", "MFC disconnected successfully.")
        #updating the connection info
        self.update_connection_devices()
        self.status_var.set(f"MFC {index + 1} disconnected")
    
    def connect_cooling(self):  
        if self.cooling.connect():
            #messagebox.showinfo("Connection", "Torrey Pines IC20XR Digital Chilling/Heating Dry Baths successfully connected.")
            #updating the connection info
            self.update_connection_devices()
            self.status_var.set(f"Torrey Pines IC20XR Digital Chilling/Heating Dry Baths connected")
        else:
            messagebox.showinfo("Connection Failed", "Cooling is not connected")
         
    def disconnect_cooling(self):
        self.cooling.disconnect()
        #messagebox.showinfo("Disconnected", "Torrey Pines IC20XR Digital Chilling/Heating Dry Baths disconnected successfully.")
        #updating the connection info
        self.update_connection_devices()
        self.status_var.set(f"Torrey Pines IC20XR Digital Chilling/Heating Dry Baths disconnected")

    def connect_valve(self):  
        if self.valve.connect():
            #messagebox.showinfo("Connection", "RVM Industrial Microfluidic Rotary valve is successfully connected.")
            #updating the connection info
            self.update_connection_devices()
            self.status_var.set(f"RVM Industrial Microfluidic Rotary valve connected")
        else:
            messagebox.showinfo("Connection Failed", "RVM is not connected")
         
    def disconnect_valve(self):
        self.valve.disconnect()
        #messagebox.showinfo("Disconnected", "RVM Industrial Microfluidic Rotary valve is disconnected successfully.")
        #updating the connection info
        self.update_connection_devices()
        self.status_var.set(f"RVM Industrial Microfluidic Rotary valve disconnected")

    def connect_all_devices(self):
        self.connect_MFC(index = 0)
        self.connect_MFC(index = 1)
        self.connect_MFC(index = 2)
        self.connect_cooling()
        self.connect_valve()
        self.status_var.set(f"MFC, Torrey Pines IC20XR Digital Chilling/Heating Dry Baths and RVM Industrial Microfluidic Rotary valve connected")
   
    def update_connection_devices(self):
		# #Labels at MFC tab
        # self.MFC_tab_MFC_current_port_label.config(text=f"MFC Port: {self.MFC.port}, Connected: {self.MFC.connected}")
        # self.MFC_tab_valve_current_port_label.config(text=f"RVM Port: {self.valve.port}, Connected: {self.valve.connected}")
        # self.MFC_tab_cooling_current_port_label.config (text=f"Cooling Port: {self.cooling.port}, Connected: {self.cooling.connected}")
        
		# #Labels at Cooling tab
        # self.cooling_tab_MFC_current_port_label.config(text=f"MFC Port: {self.MFC.port}, Connected: {self.MFC.connected}")
        # self.cooling_tab_valve_current_port_label.config(text=f"RVM Port: {self.valve.port}, Connected: {self.valve.connected}")
        # self.cooling_tab_cooling_current_port_label.config(text=f"Cooling Port: {self.cooling.port}, Connected: {self.cooling.connected}")

		# #Labels at Valve Tab
        # self.valve_tab_MFC_current_port_label.config(text=f"MFC Port: {self.MFC.port}, Connected: {self.MFC.connected}")
        # self.valve_tab_valve_current_port_label.config(text=f"RVM Port: {self.valve.port}, Connected: {self.valve.connected}")
        # self.valve_tab_cooling_current_port_label.config (text=f"Cooling Port: {self.cooling.port}, Connected: {self.cooling.connected}")
        
        #Labels at the Header
        self.connection_mfc1_port_label.config (text=f"MFC 1 Port: {self.mfcs[0].port}, Connected: {self.mfcs[0].connected}")
        self.connection_mfc2_port_label.config (text=f"MFC 2 Port: {self.mfcs[1].port}, Connected: {self.mfcs[1].connected}")
        self.connection_mfc3_port_label.config (text=f"MFC 3 Port: {self.mfcs[2].port}, Connected: {self.mfcs[2].connected}")
        self.connection_cooling_port_label.config(text=f"Cooling Port: {self.cooling.port}, Connected: {self.cooling.connected}")
        self.connection_valve_port_label.config(text=f"RVM Port: {self.valve.port}, Connected: {self.valve.connected}")
    
        
    def com_settings(self):
        #Opens een top level window
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Connection Settings")
        settings_window.geometry("800x500")
        
        #this forces all focus on the top level until the toplevel is closed
        settings_window.grab_set()
        
        # Labels and Entry widgets for paths and port settings
        dirpath_frame = tk.LabelFrame(settings_window, text="Dev and Data Directory:")
        dirpath_frame.pack(side ='right', fill="both", padx=10, pady=10) 
        
        ttk.Label(dirpath_frame, text="Dev Directory:").grid(row=0, column=0, padx=5, pady=5)
        self.dev_data_dir_var = tk.StringVar(value=self.mfcs[0].port)
        dev_data_dir_entry = ttk.Entry(dirpath_frame, textvariable=self.profilemanager.dev_data_dir)
        dev_data_dir_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(dirpath_frame, text="Profiles Directory:").grid(row=1, column=0, padx=5, pady=5)
        self.prof_data_dir_var = tk.StringVar(value=self.mfcs[1].port)
        prof_data_dir_entry = ttk.Entry(dirpath_frame, textvariable=self.profilemanager.profiles_dir)
        prof_data_dir_entry.grid(row=1, column=1, padx=5, pady=5)

        # Bronkhorst MFC settings
        MFC_frame = ttk.LabelFrame(settings_window, text="Bronkhorst MFC")
        MFC_frame.pack(fill="both", padx=10, pady=10)
        
        ttk.Label(MFC_frame, text="Port:").grid(row=0, column=0, padx=5, pady=5)
        self.MFC1_port_var = tk.StringVar(value=self.mfcs[0].port)
        MFC1_port_entry = ttk.Entry(MFC_frame, textvariable=self.MFC1_port_var)
        MFC1_port_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(MFC_frame, text="Port:").grid(row=1, column=0, padx=5, pady=5)
        self.MFC2_port_var = tk.StringVar(value=self.mfcs[1].port)
        MFC2_port_entry = ttk.Entry(MFC_frame, textvariable=self.MFC2_port_var)
        MFC2_port_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(MFC_frame, text="Port:").grid(row=2, column=0, padx=5, pady=5)
        self.MFC3_port_var = tk.StringVar(value=self.mfcs[2].port)
        MFC3_port_entry = ttk.Entry(MFC_frame, textvariable=self.MFC3_port_var)
        MFC3_port_entry.grid(row=2, column=1, padx=5, pady=5)
        
        # Cooling settings
        cooling_frame = ttk.LabelFrame(settings_window, text="Torrey Pines IC20XR Digital Chilling/Heating Dry Baths")
        cooling_frame.pack(fill="both", padx=10, pady=10)
        
        ttk.Label(cooling_frame, text="Port:").grid(row=3, column=0, padx=5, pady=5)
        self.cooling_port_var = tk.StringVar(value=self.cooling.port)
        cooling_port_entry = ttk.Entry(cooling_frame, textvariable=self.cooling_port_var)
        cooling_port_entry.grid(row=3, column=1, padx=5, pady=5)
        
        # valve settings
        valve_frame = ttk.LabelFrame(settings_window, text="RVM Industrial Microfluidic Rotary valve ")
        valve_frame.pack(fill="both", padx=10, pady=10)
        
        ttk.Label(valve_frame, text="Port:").grid(row=4, column=0, padx=5, pady=5)
        self.valve_port_var = tk.StringVar(value=self.valve.port)
        valve_port_entry = ttk.Entry(valve_frame, textvariable=self.valve_port_var)
        valve_port_entry.grid(row=4, column=1, padx=5, pady=5)
            
        save_button = ttk.Button(settings_window, text="Save", command=self.save_settings)
        save_button.pack(pady=10)
        
    def save_settings(self):
        self.mfcs[0].port = self.MFC1_port_var.get()
        self.mfcs[1].port = self.MFC2_port_var.get()
        self.mfcs[2].port = self.MFC3_port_var.get()
        self.cooling.port = self.cooling_port_var.get()
        self.valve.port = self.valve_port_var.get()
        profiles_dir = self.profilemanager.profiles_dir.get()
        devdata_dir = self.profilemanager.dev_data_dir.get()
        
        # Ensuring the profilemanager has the same ports
        self.profilemanager.save_dev_data(self.mfcs[0].port, self.mfcs[1].port, self.mfcs[2].port, self.cooling.port, self.valve.port, filename = 'hoi')
        
        self.update_connection_devices()
        self.status_var.set("Port connections are updated.")

    def set_MFCmassflow(self, index):
        massflowrate = self.massflow_vars[index].get()
        if self.mfcs[index].set_massflow(massflowrate):
            self.target_massflow_labels[index].config(text=f"Target mass flow rate: {self.mfcs[index].targetmassflow} mL/min")
            self.update_massflow(index)
        else:
            self.status_var.set("MFC: Failed to set mass flow rate.")
            
    def update_massflow(self, index):
        current_flow = self.mfcs[index].get_massflow()
        # self.update_run_var()
        if current_flow is not None:
            self.current_massflow_labels[index].config(text=f"Current mass flow rate: {current_flow:.2f} mL/min")
        else:
            self.status_var.set("Failed to read mass flow rate.")
        
        # Passing the index to the function by using lambda
        # Lambda are anonymous function means that the function is without a name
        # https://www.geeksforgeeks.org/using-lambda-in-gui-programs-in-python/
        self.root.after(1000, lambda: self.update_massflow(index)) #updating the MFC flow rate reading each 1s
        
    def set_temperature(self):
        temperature = self.temperature_var.get()
        if self.cooling.set_temperature(temperature):
            self.target_temperature_label.config(text=f"Target temperature: {self.cooling.targettemperature:.2f} °C")
            self.update_temperature()
        else:
            self.status_var.set("Cooling: Failed to set the temperature.")
    
    def update_temperature(self):
        current_temp = self.cooling.get_temperature(1)
        # self.update_run_var()
        if current_temp is not None:
            self.current_temperature_label.config(text=f"Current temperature: {current_temp:.2f} °C")
        else:
            self.status_var.set("Failed to read the temperature.")
        
        #Updating temperature every 1s; otherwise the simulation/reading the data won't work. It would only happen one time.
        #https://www.geeksforgeeks.org/python-after-method-in-tkinter/
        self.notebook.after(1000, self.update_temperature) 
        
    def set_valve(self):
        position = self.valve_pos_var.get()
        if self.valve.set_valve(position):
            self.update_valve()

    def update_valve(self):
        current_position = self.valve.current_valve_position()
        # self.update_run_var()
        if current_position is not None:
            self.current_valve_label.config(text=f"Current position of the valve: {current_position}")
        else:
            self.status_var.set("Failed to read the position of the valve.")
    
    def update_profile_list(self):
        """Refresh the list of available profiles"""
        #https://youtu.be/Vm0ivVxNaA8
        
        #Delete all the items from the listbox
        self.profile_listbox.delete(0, tk.END)
        
        #Add all the profiles to the listbox
        for profile in self.profilemanager.get_profiles():
            self.profile_listbox.insert(tk.END, profile)  #listbox.insert(index, element)

    def load_profile(self):
        """Load the selected profile into the editor"""
        #https://pythonassets.com/posts/listbox-in-tk-tkinter/
        selection = self.profile_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a profile to load")
            return
        
        #To ensure that you only select the first selected
        profile_name = self.profile_listbox.get(selection[0])
        profile = self.profilemanager.load_profile(profile_name)
        
        self.new_profile_label.config(text = "")
        
        if profile:
            self.current_loaded_profile = profile_name
            #Update the name of the profile
            self.name_var.set(profile_name)
            #Update the description in the field
            self.desc_var.set(profile.get("description", ""))
            
            # Clear the existing steps
            for item in self.steps_tree.get_children():
                self.steps_tree.delete(item)
            
            # Add new steps
            for step in profile.get("steps", []):
                self.steps_tree.insert("", tk.END, values=(
                    step["time"],
                    step["flow mfc1"],
                    step["flow mfc2"],
                    step["flow mfc3"],
                    step["temperature"],
                    step["valve"]
                ))
            
            self.status_var.set(f"Loaded profile: {profile_name}")
        
    def delete_profile(self):
        """Delete the selected profile"""
        #https://pythonassets.com/posts/listbox-in-tk-tkinter/
        selection = self.profile_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a profile to delete")
            return
            
        profile_name = self.profile_listbox.get(selection[0]) #To ensure that you only select the first selected
        
        if messagebox.askyesno("Confirm", f"Delete profile '{profile_name}'?"):
            if self.profilemanager.delete_profile(profile_name):
                #Updating the new profile list
                self.update_profile_list() 
                #Changing the status
                self.status_var.set(f"Deleted profile: {profile_name}")
            else:
                messagebox.showerror("Error", f"Failed to delete the profile: '{profile_name}'")
                
    def create_new_profile(self):
		#Clearing all input fields and steps
        self.name_var.set("")
        self.desc_var.set("")
        self.step_time_var.set("0")
        self.step_flow1_var.set("0")
        self.step_flow2_var.set("0")
        self.step_flow3_var.set("0")
        self.step_temp_var.set("0")
        self.step_valve_var.set("0")
        
        for item in self.steps_tree.get_children():
            self.steps_tree.delete(item)
        
        self.new_profile_label.config(text = "New profile", foreground = "green")
        
    def add_step(self):
        """Add a new step to the current profile"""
        try:
            time_val = int(self.step_time_var.get())
            flow1_val = float(self.step_flow1_var.get())
            flow2_val = float(self.step_flow2_var.get())
            flow3_val = float(self.step_flow3_var.get())
            temp_val = float(self.step_temp_var.get())
            valve_val = int(self.step_valve_var.get())
            
            if time_val < 0:
                raise ValueError("Time cannot be negative")
            if valve_val not in [1, 2]:
                raise ValueError("Position of the valve must be 1 or 2")
            
            # Check if the time already exists
            for child in self.steps_tree.get_children():
                if int(self.steps_tree.item(child, "values")[0]) == time_val:
                    if not messagebox.askyesno("Confirm", f"Step at time {time_val}s already exists. Overwrite?"):
                        return #if True, thus no then return
                    self.steps_tree.delete(child)
                    break
            
            self.steps_tree.insert("", tk.END, values=(time_val, flow1_val, flow2_val, flow3_val, temp_val, valve_val))
            
        except ValueError as error:
            messagebox.showerror("Error", f"Invalid input: {error}")
    
    def remove_step(self):
        """Remove the selected step"""
        selection = self.steps_tree.selection()
        if selection:
            self.steps_tree.delete(selection)
    
    def clear_steps(self):
        """Clear all steps"""
        if messagebox.askyesno("Confirm", "Clear all the steps?"):
            #Obtain all the steps and delete all the steps
            for item in self.steps_tree.get_children():
                self.steps_tree.delete(item)
    
    def save_profile(self):
        """Save the current profile"""
        #Getting the name
        name = self.name_var.get().strip()
        
        #Ensuring that the name isn't empty
        if not name:
            messagebox.showwarning("Warning", "Profile name cannot be empty")
            return
        
        # Collect steps from the profile
        steps = []
        for child in self.steps_tree.get_children():
            #To obtain all the values of the steps
            values = self.steps_tree.item(child, "values")
            steps.append({
                "time": int(values[0]),
                "flow mfc1": float(values[1]),
                "flow mfc2": float(values[2]),
                "flow mfc3": float(values[3]),
                "temperature": float(values[4]),
                "valve": int(values[5])
            })
        
        # Sort steps by time
        #https://docs.python.org/3/howto/sorting.html
        steps = sorted(steps, key=lambda steps: steps["time"])
        
        # Create the profile data
        profile_data = {
            "description": self.desc_var.get(),
            "steps": steps
        }
        
        if self.profilemanager.save_profile(name, profile_data):
            self.update_profile_list()
            self.status_var.set(f"Saved profile: {name}")
        else:
            messagebox.showerror("Error", f"Failed to save profile '{name}'")
    
    def run_profile(self):
        """Run the current profile"""    
        
        if not (self.mfcs[0].connected and self.mfcs[1].connected and self.mfcs[2].connected and self.cooling.connected and self.valve.connected):
            self.status_var.set("One or more devices are not connected")
            return False
          
        #Get the name of the profile without spaces, such that the .json file can be loaded later
        name = self.name_var.get().strip()
        
        #Checking whether the name is empty
        if not name:
            messagebox.showwarning("Warning", "Please load or create a profile first")
            return

        # Load the profile that needs to be runned
        profile = self.profilemanager.load_profile(name)
        if not profile:
            messagebox.showerror("Error", f"Failed to load profile: '{name}'")
            return
        
        #Enabling the stop button, since you can now stop a running profile
        self.stop_button.config(state=tk.NORMAL) 
        
        # Start profile in a separate thread, such that the UI doesn't freeze until it finishes
        # And you'll still be able to see what happens, e.g. popup of not connection
        self.profile_thread = threading.Thread(
            target=self.run_profile_thread,
            args=(profile,),    
            daemon=True         # Stops threading by pressing an event, e.g. pressing on stop button
        )
        self.profile_thread.start()
    
    def run_profile_thread(self, profile):
        """Thread function to run the profile"""
        try:
            print(self.mfcs[0].port, self.mfcs[1].port, self.mfcs[2].port, self.cooling.port, self.valve.port)
            print(self.mfcs[0].connected , self.mfcs[1].connected , self.mfcs[2].connected , self.cooling.connected , self.valve.connected)
            # Displaying which profile is running
            self.status_var.set(f"Running profile: {self.name_var.get()}")
            self.profilemanager.run_profile()
            # self.notebook.after(0, lambda: self.update_run_status)
            self.notebook.after(0, self.profile_complete)

        except Exception as e:
            self.notebook.after(0, lambda: self.profile_error(str(e)))
    
    # def update_run_status(self, status):
    #     """Update UI with current run status"""
    #     elapsed = status["elapsed_time"]
    #     step = status["current_step"]
    #     total = status["total_steps"]
    #     self.status_var.set(
    #         f"Running: {elapsed:.1f}s | Step {step}/{total} | "
    #         f"Flow mfc1: {status['flow mfc1']} mL/min | "
    #         f"Flow mfc2: {status['flow mfc2']} mL/min | "
    #         f"Flow mfc3: {status['flow mfc3']} mL/min | "
    #         f"Temp: {status['temperature']}°C | "
    #         f"Valve: {status['valve']}"
    #     )
    
    def profile_complete(self):
        """Called when profile completes successfully"""
        self.stop_button.config(state=tk.DISABLED)
        self.status_var.set("Profile run completed")
    
    def profile_error(self, error):
        """Called when profile run encounters an error"""
        self.stop_button.config(state=tk.DISABLED)
        messagebox.showerror("Error", f"Profile run failed: {error}")
        self.status_var.set("Profile run failed")
    
    def stop_profile(self):
        """Stop the currently running profile"""
        self.stop_button.config(state=tk.DISABLED)
        self.status_var.set("Profile run stopped by user")
    
        
def main():
    root = tk.Tk()
    app = AutomatedSystemUI(root)
    root.mainloop()
    
if __name__ == "__main__":
    main()
