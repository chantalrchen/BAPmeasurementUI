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

class MFCProfileManager:
    def __init__(self, profiles_dir="profiles_onetab"):
        #profiles_dir is the path where the profile will be saved
        self.profiles_dir = os.path.join(profiles_dir, "profiles_mfc")
        self.current_profile = None
        self.standard_profiles = {
            "Flow_Test MFC": {
                "description": "Test flow rate changes",
                "steps": [
                    {"time": 0, "flow mfc1": 0.5, "flow mfc2": 0.5, "flow mfc3": 0.5},
                    {"time": 10, "flow mfc1": 1.0, "flow mfc2": 0.5, "flow mfc3": 0.5},
                    {"time": 20, "flow mfc1": 1.5, "flow mfc2": 0.5, "flow mfc3": 0.5},
                    {"time": 30, "flow mfc1 ": 1.0, "flow mfc2": 0.5, "flow mfc3": 0.5},
                    {"time": 40, "flow": 0.5, "flow mfc2": 0.5, "flow mfc3": 0.5}
                ]
            }
        }

        self.mfcs = [BronkhorstMFC(port = 'COM1'),  BronkhorstMFC(port = 'COM2'), BronkhorstMFC(port = 'COM3')]
        
        # Create profiles directory if it doesn't exist
        if not os.path.exists(self.profiles_dir):
            os.makedirs(self.profiles_dir)
            
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

    def run_profile(self, temp_ambient):
        """Run the current profile with the given device controllers"""
        # Ensuring that the MFC, cooling and valve are all connected
        # print(self.mfcs[0].port, self.mfcs[1].port, self.mfcs[2].port)
        # print(self.mfcs[0].connected , self.mfcs[1].connected , self.mfcs[2].connected)
        
        if temp_ambient is None:
            messagebox.showwarning("Warning", "Please set the ambient temperature first")
            
        if not (self.mfcs[0].connected and self.mfcs[1].connected and self.mfcs[2].connected):
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
        print(start_time)
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

            # Check if profile is complete
            if current_step_index == len(steps) - 1 and elapsed_time >= current_step["time"]:
                profile_complete = True
        
        return True

class CoolingProfileManager:
    def __init__(self, profiles_dir="profiles_onetab"):
        #profiles_dir is the path where the profile will be saved
        self.profiles_dir = os.path.join(profiles_dir, "profiles_cooling")
        self.current_profile = None
        self.standard_profiles = {
            "Flow_Test COOLING": {
                "description": "Test flow rate changes",
                "steps": [
                    {"time": 0, "temperature": 25},
                    {"time": 10, "temperature": 25},
                    {"time": 20, "temperature": 25},
                    {"time": 30, "temperature": 25},
                    {"time": 40, "temperature": 25}
                ]
            }
        }
        self.cooling = Koelingsblok()

        # Create profiles directory if it doesn't exist
        if not os.path.exists(self.profiles_dir):
            os.makedirs(self.profiles_dir)
            
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

    def run_profile(self, temp_ambient):
        """Run the current profile with the given device controllers"""
        # Ensuring that the MFC, cooling and valve are all connected

        if temp_ambient is None:
            messagebox.showwarning("Warning", "Please set the ambient temperature first")
            
        if not (self.cooling.connected):
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
        print(start_time)
        print("hoi")
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
            self.cooling.set_temperature(current_step["temperature"], temp_ambient)
            
            # Check if profile is complete
            if current_step_index == len(steps) - 1 and elapsed_time >= current_step["time"]:
                profile_complete = True
        
        return True

class ValveProfileManager:
    def __init__(self, profiles_dir="profiles_onetab"):
        #profiles_dir is the path where the profile will be saved
        self.profiles_dir = os.path.join(profiles_dir, "profiles_valve")
        self.current_profile = None
        self.standard_profiles = {
            "Flow_Test VALVE": {
                "description": "Test flow rate changes",
                "steps": [
                    {"time": 0, "valve": 1},
                    {"time": 10, "valve": 1},
                    {"time": 20, "valve": 1},
                    {"time": 30, "valve": 1},
                    {"time": 40, "valve": 1}
                ]
            }
        }

        self.valve = RVM()
        # Create profiles directory if it doesn't exist
        if not os.path.exists(self.profiles_dir):
            os.makedirs(self.profiles_dir)
            
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

    def run_profile(self, temp_ambient):
        """Run the current profile with the given device controllers"""
        # Ensuring that the MFC, cooling and valve are all connected
        
        if temp_ambient is None:
            messagebox.showwarning("Warning", "Please set the ambient temperature first")
            
        if not (self.valve.connected):
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
        print(start_time)
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
            self.valve.set_valve(current_step["valve"])
        
            # Check if profile is complete
            if current_step_index == len(steps) - 1 and elapsed_time >= current_step["time"]:
                profile_complete = True
        
        return True

class AutomatedSystemUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Automated System")
        self.root.geometry("1400x800")
              
        ##Het volgende is niet zo logisch, alleen als je het niet zo doet, krijg je dus dat profilemanager en UI een andere bronkhorst te pakken gaan krijgen
        ##Daarnaast zijn de porten dan ook niet aligned aahh
        
        self.mfcprofilemanager = MFCProfileManager()
        self.coolingprofilemanager = CoolingProfileManager()
        self.valveprofilemanager = ValveProfileManager()
        
        ##Het volgende is niet zo logisch, alleen als je het niet zo doet, krijg je dus dat profilemanager en UI een andere bronkhorst te pakken gaan krijgen
        ##Daarnaast zijn de porten dan ook niet aligned aahh
        self.mfcs = self.mfcprofilemanager.mfcs
        self.cooling = self.coolingprofilemanager.cooling
        self.valve = self.valveprofilemanager.valve
        
        
        # Header frame for connection and status
        header_frame = ttk.Frame(self.root)
        header_frame.pack(side='top', fill='x', padx=5, pady=5)
        
        # Connection status frame
        connection_frame = ttk.Frame(header_frame)
        connection_frame.pack(side='right', padx=10)
        
        ttk.Label(connection_frame, text="Device Connections", font=("Arial", 11, "bold")).pack(fill = 'both', expand = True)
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
        connect_all_button.pack(side='right', fill = 'both', expand = 'true')
        
        othervar_frame  = ttk.Frame(header_frame)
        othervar_frame.pack(side='right', padx=10)
        
        # Ambient temperature section
        ttk.Label(othervar_frame, text="Set Ambient Temperature", font=("Arial", 11, "bold")).pack(fill='both', expand=True)
        # Label and Entry for ambient temperature
        self.ambient_temp_label = tk.Label(othervar_frame, text=f"Ambient Temperature (°C): not set")
        self.ambient_temp_label.pack(fill='both', expand=True)
        self.ambient_temp = tk.DoubleVar()  # Use DoubleVar for floating-point values
        self.ambient_temp_entry = tk.Entry(othervar_frame, textvariable = self.ambient_temp)
        self.ambient_temp_entry.pack(fill='both', expand=True)
        ambient_temp_button = ttk.Button(othervar_frame, text = "Set ambient temperature", command = self.set_ambient_temp)
        ambient_temp_button.pack(fill='both', expand=True)
        
        # Status bar, to show what has been adjusted
        # Status label
        self.status_var = tk.StringVar() 
        self.status_var.set("Status:")
        status_bar = ttk.Label(header_frame, text='Status', textvariable=self.status_var)
        status_bar.pack(fill='both', padx=5, pady=5)
        
        self.running_var_bar = tk.Label(header_frame, text="")
        self.running_var_bar.pack(side= 'bottom', fill='x')
        
        self.profile_listboxes = {}
        self.profile_new_profile_label = {}
        self.profile_step_trees = {}
        self.profile_name_vars = {}
        self.profile_desc_vars = {}
        self.profile_labels = {}
        self.profile_step_vars = {}
        
        self.mfc_entry_fields = ["time", "flow mfc1", "flow mfc2", "flow mfc3"]
        self.cooling_entry_fields = ["time", "temperature"]
        self.valve_entry_fields = ["time", "valve"]

        # Notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True)
        
        self.create_menu()
        self.create_device_tab()
        # self.create_MFC_tab()
        # self.create_cooling_tab()
        # self.create_valve_tab()
        self.create_profile_tab(self.mfcprofilemanager, "MFC Profile Manager", self.mfc_entry_fields)
        self.create_profile_tab(self.coolingprofilemanager, "Cooling Profile Manager", self.cooling_entry_fields)
        self.create_profile_tab(self.valveprofilemanager, "Valve Profile Manager", self.valve_entry_fields)

                
    def set_ambient_temp(self):
        """
        Retrieve the ambient temperature from the entry box and set it.
        """
        try:
            # Get the value from the entry box
            self.ambient_temp = float(self.ambient_temp_entry.get())
            # Update the status bar to show the ambient temperature has been set
            self.ambient_temperature_label.config(text=f"Ambient temperature: {self.ambient_temp} °C")
            self.ambient_temp_label.config(text=f"Ambient temperature: {self.ambient_temp} °C")
            self.status_var.set(f"Ambient temperature set to {self.ambient_temp} °C")
        except ValueError:
            self.status_var.set("Invalid input! Enter a floating number for the ambient temperature.")
            messagebox.showerror("Invalid Input", "Please enter a floating number for ambient temperature.")
            
    def update_run_var(self):
 
        # Get mass flow rates from MFCs
        mass_flow_1 = f"{self.mfcs[0].get_massflow():.2f} mL/min" if self.mfcs[0].connected else "N/A"
        mass_flow_2 = f"{self.mfcs[1].get_massflow():.2f} mL/min" if self.mfcs[1].connected else "N/A"
        mass_flow_3 = f"{self.mfcs[2].get_massflow():.2f} mL/min" if self.mfcs[2].connected else "N/A"

        # Get temperature from cooling system
        temperature = f"{self.cooling.get_temperature(1):.2f} °C" if self.cooling.connected else "N/A"

        # Get valve position from valve
        valve_position = self.valve.current_valve_position() if self.valve.connected else "N/A"
        self.running_var_bar.config(text=f"MFC 1 Mass Flow Rate: {mass_flow_1} | MFC 2 Mass Flow Rate: {mass_flow_2} | MFC 3 Mass Flow Rate: {mass_flow_3} | Temperature: {temperature} | Valve Position: {valve_position}")

        # Schedule the next update
        self.notebook.after(10, lambda: self.update_run_var)
        
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

        # Label to display the ambient temp
        self.ambient_temperature_label = tk.Label(cooling_frame, text=f"Ambient temperature: Not set")
        self.ambient_temperature_label.grid(row=2, column=0, padx=10, pady=10)
        
        # Label to display the current temp
        self.current_temperature_label = tk.Label(cooling_frame, text="Current temperature: Not available")
        self.current_temperature_label.grid(row=2, column=1, padx=10, pady=10)
        
        # Label to display the target temp
        self.target_temperature_label = tk.Label(cooling_frame, text=f"Target temperature: {self.cooling.targettemperature:.2f} °C")
        self.target_temperature_label.grid(row=2, column=2, padx=10, pady=10)

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
    
    def create_profile_tab(self, profile_manager, tab_name, entry_fields):
        profile_tab = ttk.Frame(self.notebook)
        profile_tab.pack(fill = 'both', expand = True)
        self.notebook.add(profile_tab, text=tab_name)
        
        list_frame = tk.Listbox(profile_tab)
        list_frame.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        
        edit_frame = ttk.Frame(profile_tab)
        edit_frame.pack(side='right', fill='both', expand=True, padx=5, pady=5)

        ### Left frame / list frame
        ## Profile listbox with scrollbar
        # https://www.pythontutorial.net/tkinter/tkinter-listbox/#adding-a-scrollbar-to-the-listbox
        # Making an empty profile listbox
        
        
        self.profile_listboxes[tab_name] = tk.Listbox(list_frame, selectmode = tk.SINGLE)
        self.profile_listboxes[tab_name].pack(fill= 'both', expand=True, padx=5, pady=5)
        
        self.update_profile_list(profile_manager, tab_name)
        
        #Adding a scrollbar to the profile listbox
        v_scrollbar = ttk.Scrollbar(self.profile_listboxes[tab_name], orient = tk.VERTICAL, command = self.profile_listboxes[tab_name].yview)
        
        self.profile_listboxes[tab_name]['yscrollcommand'] = v_scrollbar.set
        v_scrollbar.pack(side='right', fill='y')
        
        ##Adding the buttons to the left frame (list frame)
        # Profile list buttons
        button_frame = ttk.Frame(list_frame)
        button_frame.pack(fill='x', padx=5, pady=5)
        
        load_button = ttk.Button(button_frame, text="Load", command=lambda: self.load_profile(profile_manager, tab_name))
        load_button.pack(side='left', padx=3, expand=True)
        
        delete_button = ttk.Button(button_frame, text="Delete", command= lambda: self.delete_profile)
        delete_button.pack(side='left', padx=3, expand=True)

        ##Right frame / edit frame
        # Profile info
        info_frame = ttk.Frame(edit_frame)
        info_frame.pack(fill='both', padx=5, pady=5)
        
        self.profile_new_profile_label[tab_name] = ttk.Label(info_frame, text="")
        self.profile_new_profile_label[tab_name].pack(side = 'left', padx=5, expand=True, fill='x')

        ##purpose idkkk?
        vars_dict = {field: tk.DoubleVar() if field != 'time' and field != 'valve' else tk.IntVar() for field in entry_fields}

        ttk.Label(info_frame, text="Name:").pack(side='left')
        self.profile_name_vars[tab_name] = tk.StringVar()
        name_entry = ttk.Entry(info_frame, textvariable=self.profile_name_vars[tab_name])
        name_entry.pack(side='left', padx=5, expand=True, fill='x')

        ttk.Label(info_frame, text="Description:").pack(side='left')
        self.desc_var = tk.StringVar()
        desc_entry = ttk.Entry(info_frame, textvariable=self.desc_var)
        desc_entry.pack(side='left', padx=5, expand=True, fill='x')
        
        new_profile_btn = ttk.Button(info_frame, text = 'New Profile', command = lambda: self.create_new_profile(tab_name))
        new_profile_btn.pack(side='right', padx=3, expand=True)
        
         # Steps in the right/frame
        steps_frame = ttk.Frame(edit_frame)
        steps_frame.pack(fill = 'both' , expand=True, padx=5, pady=5)

        tree = ttk.Treeview(steps_frame, columns=entry_fields, show="headings")
        for col in entry_fields:
            tree.heading(col, text=col.capitalize())
            tree.column(col, width=100, anchor=tk.CENTER)
        tree.pack(fill='both', expand=True)
        self.profile_step_trees[tab_name] = tree

        step_controls_frame = ttk.Frame(edit_frame)
        step_controls_frame.pack(fill='x', padx=5, pady=5)

        step_vars = {}
        for field in entry_fields:
            ttk.Label(step_controls_frame, text=f"{field.capitalize()}:").pack(side='left')
            var = tk.DoubleVar() if field != 'time' and field != 'valve' else tk.IntVar()
            ttk.Entry(step_controls_frame, textvariable=var, width=8).pack(side='left', padx=2)
            step_vars[field] = var

        self.profile_step_vars[tab_name] = step_vars

        step_buttons_frame = ttk.Frame(edit_frame)
        step_buttons_frame.pack(fill='both')

        ttk.Button(step_buttons_frame, text="Add Step", command=lambda: self.add_step(tab_name)).pack(side='left', padx=2)
        ttk.Button(step_buttons_frame, text="Remove Step", command=lambda: self.remove_step(tab_name)).pack(side='left', padx=2)
        ttk.Button(step_buttons_frame, text="Clear All Steps", command=lambda: self.clear_steps(tab_name)).pack(side='left', padx=2)

        action_buttons_frame = ttk.Frame(edit_frame)
        action_buttons_frame.pack(fill='both')

        ttk.Button(action_buttons_frame, text="Save Profile", command=lambda: self.save_profile(profile_manager, tab_name)).pack(side='left', padx=2)
        ttk.Button(action_buttons_frame, text="Run Profile", command=lambda: profile_manager.run_profile(self.ambient_temp)).pack(side='left', padx=2)

        self.current_loaded_profile = None        
        # #https://tk-tutorial.readthedocs.io/en/latest/tree/tree.html
        # self.profile_trees[tab_name] = ttk.Treeview(
        #     steps_frame, 
        #     columns= entry_fields, 
        #     show="headings"
        # )
        
        # def save_profile():
        #     profile_data = {
        #         "description": desc_var.get(),
        #         "steps": [{field: vars_dict[field].get() for field in entry_fields}]
        #     }
        #     profile_manager.save_profile(name_var.get(), profile_data)
        #     refresh_profiles()

        # def load_profile():
        #     selection = profile_listbox.curselection()
        #     if selection:
        #         profile_name = profile_listbox.get(selection[0])
        #         profile = profile_manager.load_profile(profile_name)
        #         if profile:
        #             name_var.set(profile_name)
        #             desc_var.set(profile.get("description", ""))
        #             for field in entry_fields:
        #                 vars_dict[field].set(profile["steps"][0].get(field, 0))

        # ttk.Button(edit_frame, text="Save Profile", command=save_profile).pack()
        # ttk.Button(edit_frame, text="Load Profile", command=load_profile).pack()
        
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
        settings_window.geometry("400x400")
        
        #this forces all focus on the top level until the toplevel is closed
        settings_window.grab_set()
        
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
        self.update_run_var()
        if current_flow is not None:
            self.current_massflow_labels[index].config(text=f"Current mass flow rate: {current_flow:.2f} mL/min")
        else:
            self.status_var.set("Failed to read mass flow rate.")
        
        # Passing the index to the function by using lambda
        # Lambda are anonymous function means that the function is without a name
        # https://www.geeksforgeeks.org/using-lambda-in-gui-programs-in-python/
        self.root.after(1000, lambda: self.update_massflow(index)) #updating the MFC flow rate reading each 1s
        
    def set_temperature(self):
        if self.cooling.connected == False:
            messagebox.showwarning("Device not connected", "The Torrey Pines IC20XR Digital Chilling/Heating Dry Baths is not connected")
            return False
        elif not isinstance(self.ambient_temp, (int, float)):
            messagebox.showwarning("Invalid Input", "Ambient Temperature has not been set yet or is an non-numeric value.")
            return False
        else:    
            try:
                temperature = float(self.temperature_var.get())
                self.cooling.set_temperature(temperature, self.ambient_temp)
                self.target_temperature_label.config(text=f"Target temperature: {self.cooling.targettemperature:.2f} °C")
                self.update_temperature()
                
                ##if non-floating number, tk.tclerror occurs
            except tk.TclError as e:
                messagebox.showerror("Invalid Input", f"Please enter a floating number for target temperature. {e}")
                
    def update_temperature(self):
        current_temp = self.cooling.get_temperature(1)
        self.update_run_var()
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
        self.update_run_var()
        if current_position is not None:
            self.current_valve_label.config(text=f"Current position of the valve: {current_position}")
        else:
            self.status_var.set("Failed to read the position of the valve.")
    
    def update_profile_list(self, profile_manager, tab_name):
        """Refresh the list of available profiles"""
        #https://youtu.be/Vm0ivVxNaA8
        listbox = self.profile_listboxes.get(tab_name)
        listbox.delete(0, tk.END)
        for profile in profile_manager.get_profiles():
            listbox.insert(tk.END, profile)
            
    def load_profile(self, profile_manager, tab_name):
        """Load the selected profile into the editor"""
        #https://pythonassets.com/posts/listbox-in-tk-tkinter/
        
        listbox = self.profile_listboxes.get(tab_name)
        selection = listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a profile to load")
            return
        
        #To ensure that you only select the first selected
        profile_name = listbox.get(selection[0])
        profile = profile_manager.load_profile(profile_name)
        
        new_profile_label = self.profile_new_profile_label.get(tab_name)
        new_profile_label.config(text = "")
        
        if profile:
            self.current_loaded_profile = profile_name
            #Update the name of the profile
            self.profile_name_vars[tab_name].set(profile_name)
            #Update the description in the field
            self.profile_desc_vars[tab_name].set(profile.get("description", ""))
            
            # Clear the existing steps
            tree = self.profile_step_trees[tab_name]
            tree_fields = tree["columns"]
            for item in tree.get_children():
                tree.delete(item)
            
            # Add steps dynamically based on columns
            for step in profile.get("steps", []):
                row_values = [step.get(field, "") for field in tree_fields]
                tree.insert("", tk.END, values=row_values)
            
            print(tree_fields)
            print(profile.get("steps", []))

            self.status_var.set(f"Loaded profile: {profile_name}")
        
    def delete_profile(self, profile_manager, tab_name):
        """Delete the selected profile"""
        #https://pythonassets.com/posts/listbox-in-tk-tkinter/
        listbox = self.profile_listboxes[tab_name]
        selection = listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a profile to delete")
            return
            
        profile_name = listbox.get(selection[0]) #To ensure that you only select the first selected
        
        if messagebox.askyesno("Confirm", f"Delete profile '{profile_name}'?"):
            if profile_manager.delete_profile(profile_name):
                #Updating the new profile list
                self.update_profile_list(profile_manager, tab_name) 
                #Changing the status
                self.status_var.set(f"Deleted profile: {profile_name}")
            else:
                messagebox.showerror("Error", f"Failed to delete the profile: '{profile_name}'")
                
    def create_new_profile(self, tab_name):
        self.profile_name_vars[tab_name].set("")
        self.profile_desc_vars[tab_name].set("")
        
        #Set all step variables in the profile to zero
        for var in self.profile_step_vars[tab_name].values():
            var.set("0")
        
        tree = self.profile_step_trees[tab_name]
        for item in tree.get_children():
            tree.delete(item)
    
        self.profile_new_profile_label[tab_name].config(text = "New profile", foreground = "green")
        
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
    
    def save_profile(self, profile_manager, tab_name):
        """Save the current profile"""
        #Getting the name
        name = self.profile_name_vars[tab_name].get().strip()
        
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
    
    def run_profile(self, profilemanager, tabname):
        """Run the current profile"""    
            
        if not (self.mfcs[0].connected and self.mfcs[1].connected and self.mfcs[2].connected and self.cooling.connected and self.valve.connected):
            messagebox.showwarning("Error", "One or more devices are not connected")
            return False
          
        #Get the name of the profile without spaces, such that the .json file can be loaded later
        name = self.name_var.get().strip()
        
        #Checking whether the name is empty
        if not name:
            messagebox.showwarning("Warning", "Please load or create a profile first")
            return

        # Load the profile that needs to be runned
        profile = profilemanager.load_profile(name)
        if not profile:
            messagebox.showerror("Error", f"Failed to load profile: '{name}'")
            return
        
        self.update_run_var()
        print("hiha")
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
            # Displaying which profile is running
            self.status_var.set(f"Running profile: {self.name_var.get()}")
            self.profilemanager.run_profile(self.ambient_temp)
            # self.notebook.after(0, lambda: self.update_run_status)
            self.notebook.after(0, self.profile_complete)

        except Exception as e:
            self.notebook.after(0, lambda: self.profile_error(str(e)))
    
    def profile_complete(self):
        """Called when profile completes successfully"""
        self.stop_button.config(state=tk.DISABLED)
        self.status_var.set("Profile run completed")
    
    def profile_error(self, error):
        """Called when profile run encounters an error"""
        self.stop_button.config(state=tk.DISABLED)
        messagebox.showerror("Error", f"Profile run failed: {error}")
        self.status_var.set("Profile run failed")
    
    def stop_profile(self, manager):
        """Stop the currently running profile"""
        self.stop_button.config(state=tk.DISABLED)
        self.status_var.set("Profile run stopped by user")
    
        
def main():
    root = tk.Tk()
    app = AutomatedSystemUI(root)
    root.mainloop()
    
if __name__ == "__main__":
    main()
