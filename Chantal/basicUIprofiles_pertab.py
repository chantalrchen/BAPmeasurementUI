import tkinter as tk
from tkinter import messagebox, ttk
import propar   # Bronkhorst MFC
import serial   # Cooling and Valve
import time 
import json
import os
import threading
import amfTools

###
#MFC
class BronkhorstMFC:
    def __init__(self, port = "COM3"):
        self.port = port
        self.connected = False
        self.instrument = None
        # self.channel = channel
        self.massflow = 0
        self.targetmassflow = 0
        self.maxmassflow = 4.0
        
    def connect(self):
        # try:
        #     self.instrument = propar.instrument(self.port) # channel = self.channel)
        #     print("I am in the MFC connecting function. My port is ", self.port)
            
        #     ##toegevoegd om te checken whether it is really connected
        #     if self.get_massflow() is not False:
        #         self.connected = True
        #         self.initialize()
        #         return self.connected
        # except Exception as err:
        #     messagebox.showerror("Error",
        #         f"An error occurred while connecting the Bronkhorst MFC with port {self.port}: {err}"
        #     )
        # return False  


        ##FOR SIMULATION
        self.connected = True
        return self.connected
    
    # reset the value, fsetpoint = 0 
    def disconnect(self):
        # try:
        #     param = [{'proc_nr':33 , 'parm_nr': 3, 'parm_type': propar.PP_TYPE_FLOAT, 'data': 0}]
        #     self.instrument.write_parameters(param) #Fsetpoint
            
        # except Exception as err:
        #     messagebox.showerror("Error",
        #      f"An error occurred while disconnecting the Bronkhorst MFC: {err}")
     
        self.connected = False
        self.instrument = None
        
    
    def initialize(self):
        # try:
        #     # controlfunction, the instrument works as a flow controller or a pressure controller; manual flexi-flow
        #     param = [{'proc_nr':115 , 'parm_nr': 10, 'parm_type': propar.PP_TYPE_INT8, 'data': 0}]
        #     print("HI I AM IN MFC INITIALIZE FUNCTION MY CONNECTION IS", self.connected )
        #     self.instrument.write_parameters(param)


        # except Exception as err:
        #     messagebox.showerror("Error",
        #         f"An error occurred while initializing the Bronkhorst MFC with channel"# {self.channel}: {err}"
        #     )
        # return False  
    
        #FOR SIMULATION
        return True
  
    def get_massflow(self):
        ##the following should be connected when connected with Bronkhorst MFC
        # if self.connected and self.instrument is not None:  # device is connected and assigned
        #     try:
        #         param = [{'proc_nr':  33, 'parm_nr': 0, 'parm_type': propar.PP_TYPE_FLOAT}] #Fmeasure
        #         self.massflow = self.instrument.read_parameters(param)
        #         return self.massflow  
        #     except Exception as err:
        #         messagebox.showerror("Error",
        #             f"An error occurred while reading the mass flow rate: {err}"
        #         )
        #         return False  
        # else:
        #     messagebox.showerror("Error", "The Bronkhorst MFC is not connected.")
        #     return False  

        #FOR SIMULATION
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
            return False 

    def set_massflow(self, value: float):
        # ##the following should be connected when connected with Bronkhorst MFC
        # if self.connected and self.instrument is not None:  # device is connected and assigned
        if self.connected:
            try:
                # print("HI I AM IN THE SET_MASSFLOW LOOP AND SELF.CONNECTED IS", self.connected)
                # print(value, self.targetmassflow, self.maxmassflow)
                if value < 0:
                    messagebox.showwarning("Mass flow rate can't be negative", f"The mass flow rate can't be negative.")
                    return False             
                elif value > self.maxmassflow:
                    messagebox.showwarning("Value exceeds the maximum mass flow rate", f"The mass flow rate may not exceed {self.maxmassflow:.2f} mL/min. The mass flow rate will be set to {self.maxmassflow:.2f} mL/min.")
                    self.targetmassflow = self.maxmassflow
                    
                    # ####
                    # ##the following should be connected when connected with Bronkhorst MFC
                    # param = [{'proc_nr':33 , 'parm_nr': 3, 'parm_type': propar.PP_TYPE_FLOAT, 'data': self.maxmassflow}]
                    # self.instrument.write_parameters(param)
                    # print("HI IM NOW SETTING A MASSFLOW TO ", self.maxmassflow)
                    # ###
                    
                    return True
                else:
                    self.targetmassflow = value
                    
                    #####
                    ###the following should be connected when connected with Bronkhorst MFC
                    # param1 = [{'proc_nr':33 , 'parm_nr': 3, 'parm_type': propar.PP_TYPE_FLOAT, 'data': value}]
                    # self.instrument.write_parameters(param1) #Fsetpoint
                    # print("HI IM NOW SETTING A MASSFLOW TO ", value)
                    ####
                    
                    return True  
            except Exception as err:
                messagebox.showerror("Error",
                    f"An error occurred while setting the mass flow rate: {err}"
                )
                return False  
        else:
            messagebox.showerror("Error", "The Bronkhorst MFCs is not connected.")
            return False  
        ##

class Koelingsblok:
    def __init__(self, port = 'COM4'):
        self.port = port
        self.connected = False
        self.instrument = None
        self.temperature = 0
        self.targettemperature = 0
        self.dummy = 0
    
    def connect(self):
        
        # ##the following should be connected when connected with the Torrey Pines IC20XR Digital Chilling/Heating Dry Baths
        # # p24: 9600 baud, 1 stop bit, no parity, no hardware handshake, 100ms delay after each command sent (after \r)
        # # 100 ms delay, so a timeout of 1s should be enough
        # try:
        #     self.instrument = serial.Serial(self.port, 9600, timeout = 1)
        #     print("I am in the cooling connecting function. My port is ", self.port)
        #     self.connected = True
        #     return self.connected
        # except Exception as err:
        #     messagebox.showerror("Error",
        #         f"An error occurred while connecting the Torrey Pines IC20XR Digital Chilling/Heating Dry Baths: {err}"
        #     )
        # return False  # Operation failed
        # ##
        
        #the following is used only for simulation
        self.connected = True
        return self.connected
        ##
    
    # reset the MFC value, flow rate to 0
    def disconnect(self):
        # param = [{'proc_nr':33 , 'parm_nr': 3, 'parm_type': propar.PP_TYPE_FLOAT, 'data': 0}]
        # self.instrument.write_parameters(param) #Fsetpoint

        self.connected = False
        self.instrument = None
        
    def get_temperature(self):
    
        # # ##the following should be connected when connected with the Torrey Pines IC20XR Digital Chilling/Heating Dry Baths
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
        # # ##
        
            ##the following is used only for simulation
            # if dummy == 0:
            #     return self.temperature
            # elif dummy == 1:                
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
        # if self.connected and self.instrument is not None: 
        if self.connected:
            try:
                #the cooling system can only lower the temperature by 30 degrees below ambient
                min_temp = temp_ambient - 30
                if value < min_temp:
                    messagebox.showwarning("Value exceeds the minimum temperature", f"The ambient temperature is {temp_ambient:.2f}. The temperature may not exceed {min_temp:.2f} °C")
                    self.targettemperature = min_temp
                    
                    ###OFFICIAL
                    ##the following should be connected when connected with the Torrey Pines IC20XR Digital Chilling/Heating Dry Baths
                    # self.instrument.write(b"n" + str(min_temp).encode() + "\r") 
                    
                    #if the above does not work, try: 
                    # self.instrument.write(f"n{value}\r".encode()) 
                    # 100ms delay after each command sent (after \r)
                    time.sleep(0.1) 
                    return True
                else:
                    self.targettemperature = value
                    
                    ##OFFICIAL
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
            messagebox.showerror("Error", " The Torrey Pines IC20XR Digital Chilling/Heating Dry Baths is not connected.")
            return False #Operation failed

class RVM:
    def __init__(self, port = 'COM4'):
        self.port = port
        self.connected = False
        self.instrument = None
        self.currentposition = 1 #home status
        self.rotation_delay = 0.4  #the rotation time for 180 degree for RVMLP (1.5 s) and RVMFS (400 ms / 0.4s),

    def connect(self):
        # #Following should be 
        # try:
        #     product_list = amfTools.util.getProductList() # get the list of AMF products connected to the computer

        #     product : amfTools.Device = None
        #     self.instrument : amfTools.AMF = None
        #     for product in product_list:
        #         if "RVM" in product.deviceType:
        #             self.instrument = amfTools.AMF(product)
        #             break

        #     if self.instrument is None:
        #     # Try forced port connection if no RVM detected
        #        self.instrument = amfTools.AMF(self.port)


        #     self.instrument.connect() 
        #     self.connected = True
        #     print("connection",self.connected)
        #     self.initialize_valve()
        #     return True
    
        # except Exception as err:
        #     messagebox.showerror("Error",
        #             f"An error occurred while connecting RVM Industrial Microfluidic Rotary Valve: {err}")
        #     self.connected = False
        #     return False
        
       #SIMULATION the following is used only for simulation
        self.connected = True
        return self.connected
        #

    def disconnect(self):
        # if self.connected and self.instrument:
        #     try:
        #         self.instrument.disconnect()
        #         print("RVM disconnected.")
        #     except Exception as err: 
        #         messagebox.showerror("Error",
        #             f"An error occurred while disconnecting RVM Industrial Microfluidic Rotary Valve: {err}")
        self.connected = False

    #home status 
    def initialize_valve(self): 
        # if not self.connected:
        #     raise ConnectionError("RVM Industrial Microfluidic Rotary Valve is not connected.")
        
        # # Check if the product is homed (if not, home it)
        # try:
        #     if not self.instrument.getHomeStatus(): 
        #         self.instrument.home()
        #         time.sleep(self.rotation_delay)  # Give time for homing

        #     else:
        #         print("RVM Industrial Microfluidic Rotary Valve is already homed.")

        #     # Always move to position 1 after homing (default start position)
        #     self.instrument.valveShortestPath(1)
        #     time.sleep(self.rotation_delay) #give time for rotation
        #     self.currentposition = 1
        #     print("RVM Industrial Microfluidic Rotary Valve moved to position 1/ON State.")

        # except Exception as err:
        #     messagebox.showerror("Error",
        #          f"An error occurred while initializing the RVM Industrial Microfluidic Rotary Valve : {err}")
        
        ##For simulation
        self.currentposition = 1
            
    
    def set_valve(self, position: int):  
        if self.connected:
            if position != 1 and position != 2:
                messagebox.showerror("Error",
                    f"The position of the RVM Industrial Microfluidic Rotary Valve can only be 1 (ON) or 2 (OFF), but received: {position}"
                )
                return False
        else:
            messagebox.showerror("Error", "RVM Industrial Microfluidic Rotary Valve  is not connected.")
            return False #Operation failed
        
        ## check if is in position 1 then move to postion 2 otherwise give a warning
        if self.currentposition == 1:
            if position == 2:
                # Move to position 2
                try:
                    # ##VOOR SIMULATION UITZETTEN
                    # self.instrument.valveShortestPath(2)
                    # time.sleep(self.rotation_delay)
                    ###
                    
                    self.currentposition = 2
                    # print(f"RVM Industrial Microfluidic Rotary Valve moved to position 2/OFF state.")
                    return True
                except Exception as err:
                    messagebox.showerror("Error",
                        f"An error occurred while moving to position 2/OFF state : {err}")
            elif position == 1:
                # print(f"RVM Industrial Microfluidic Rotary Valve is already at position {self.currentposition}/OFF state")
                return False
            else:
                print(f"Invalid position: {position}")
                # return False
           
        elif self.currentposition == 2:
            if position == 1:
                # Move to position 1
                try:
                    ## VOOR SIMULATION UITZETTEN
                    # self.instrument.valveShortestPath(1)
                    # time.sleep(self.rotation_delay)
                    ###
                    
                    self.currentposition = 1
                    # print(f"RVM Industrial Microfluidic Rotary Valve moved to position 1/ON state")
                    return True
                except Exception as err:
                   messagebox.showerror("Error",
                        f"An error occurred while moving to position 1/ON tate : {err}")
            elif position == 2:
                return False
                # print(f"RVM Industrial Microfluidic Rotary Valve is already at position {self.currentposition}/ON state")
            else:
                print(f"Invalid position: {position}")


class MFCProfileManager:
    def __init__(self, profiles_dir="profiles_onetab"):
        #profiles_dir is the path where the profile will be saved
        self.profiles_dir = os.path.join(profiles_dir, "profiles_mfc")
        self.current_profile = None
        self.standard_profiles = {
            "Flow_Test MFC": {
                "description": "Test flow rate changes",
                "steps": [
                    {"time": 0.0, "flow mfc1": 0.5, "flow mfc2": 0.5, "flow mfc3": 0.5},
                    {"time": 10.0, "flow mfc1": 1.0, "flow mfc2": 0.5, "flow mfc3": 0.5},
                    {"time": 20.0, "flow mfc1": 1.5, "flow mfc2": 0.5, "flow mfc3": 0.5},
                    {"time": 30.0, "flow mfc1": 1.0, "flow mfc2": 0.5, "flow mfc3": 0.5},
                    {"time": 40.0, "flow mfc1": 0.5, "flow mfc2": 0.5, "flow mfc3": 0.5}
                ]
            }
        }
        
        self.mfcs = [BronkhorstMFC(port = 'COM1'),  BronkhorstMFC(port = 'COM2'), BronkhorstMFC(port = 'COM3')]
        
        self.stoprequest = False
        self.maxflow = 4
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

    def run_profile(self, update_callback = None):
        """Run the current profile with the given device controllers"""
        
        if not (self.mfcs[0].connected and self.mfcs[1].connected and self.mfcs[2].connected):
            messagebox.showerror("Connection Error", "MFCs not connected")
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
        self.stoprequest = False
        start_time = time.time()
        current_step_index = 0
        profile_complete = False
        # print("starttime profiles", start_time)
        # print("hoi")
        while not profile_complete and not self.stoprequest:
            elapsed_time = time.time() - start_time

            # Check if we need to move to next step
            if current_step_index < len(steps) - 1:
                next_step_time = steps[current_step_index + 1]["time"]
                # print("current step index", current_step_index, "total steps", steps, "next step time", next_step_time)
                if elapsed_time >= next_step_time:
                    current_step_index += 1
            
            # Get current step parameters
            current_step = steps[current_step_index]
            
            # Set devices to current step values
            self.mfcs[0].set_massflow(current_step["flow mfc1"])
            self.mfcs[1].set_massflow(current_step["flow mfc2"])
            self.mfcs[2].set_massflow(current_step["flow mfc3"])
            
            # print("massflow 1 set to", current_step["flow mfc1"])
            # print("massflow 2 set to", current_step["flow mfc2"])
            # print("massflow 3 set to", current_step["flow mfc3"])
            
            #if update_callback is called then we need to update the status with the corresponding data
            if update_callback:
                    update_callback({
                    "elapsed_time": elapsed_time,
                    "current_step": current_step_index + 1,
                    "total_steps": len(steps),
                    "flow mfc1": current_step["flow mfc1"],
                    "flow mfc2": current_step["flow mfc2"],
                    "flow mfc3": current_step["flow mfc3"],
                })
            # Check if profile is complete
            #such that the cpu doesn't overload
            time.sleep(0.1)
            if current_step_index == len(steps) - 1 and elapsed_time >= current_step["time"]:
                profile_complete = True
        return True
    
    def stop_profile(self):
        self.stoprequest = True
        
        #Vanuitgaand dat mfcs[2] de een is die dillute
        self.mfcs[0].set_massflow(0)
        self.mfcs[1].set_massflow(0)
        self.mfcs[2].set_massflow(self.maxflow)

class CoolingProfileManager:
    def __init__(self, profiles_dir="profiles_onetab"):
        #profiles_dir is the path where the profile will be saved
        self.profiles_dir = os.path.join(profiles_dir, "profiles_cooling")
        self.current_profile = None
        self.standard_profiles = {
            "Flow_Test COOLING": {
                "description": "Test flow rate changes",
                "steps": [
                    {"time": 0.0, "temperature": 25.0},
                    {"time": 10.0, "temperature": 15.0},
                    {"time": 20.0, "temperature": 20.0},
                    {"time": 30.0, "temperature": 10.0},
                    {"time": 40.0, "temperature": 15.0}
                ]
            }
        }
        self.cooling = Koelingsblok()
        
        self.stoprequest = False
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

    def run_profile(self, temp_ambient, update_callback = None):
        """Run the current profile with the given device controllers"""
        if not self.cooling.connected:
            messagebox.showerror("Connection Error", "Cooling is not connected")
            return False
        
        if not self.current_profile:
            messagebox.showerror("Error", "No profile loaded")
            return False
        steps = self.current_profile.get("steps", [])
        if not steps:
            messagebox.showerror("Error", "Profile has no steps")
            return False
        
        if temp_ambient is None:
            messagebox.showwarning("Warning", "Please set the ambient temperature first")
            
        # Sort steps by time
        steps = sorted(steps, key=lambda x: x["time"])
        
        self.stoprequest = False
        start_time = time.time()
        current_step_index = 0
        profile_complete = False

        while not profile_complete and not self.stoprequest:
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

            #if update_callback is called then we need to update the status with the corresponding data
            if update_callback:
                    update_callback({
                    "elapsed_time": elapsed_time,
                    "current_step": current_step_index + 1,
                    "total_steps": len(steps),
                    "temperature": current_step["temperature"],
                })

            time.sleep(0.1)
            # Check if profile is complete
            if current_step_index == len(steps) - 1 and elapsed_time >= current_step["time"]:
                profile_complete = True
        return True
    
    def stop_profile(self):
        self.stoprequest = True
        ###WAT MOETEN WE HIERNA DOEN?
        
class RVMProfileManager:
    def __init__(self, profiles_dir="profiles_onetab"):
        #profiles_dir is the path where the profile will be saved
        self.profiles_dir = os.path.join(profiles_dir, "profiles_valve")
        self.current_profile = None
        self.standard_profiles = {
            "Flow_Test VALVE": {
                "description": "Test flow rate changes",
                "steps": [
                    {"time": 0.0, "valve": 1},
                    {"time": 10.0, "valve": 1},
                    {"time": 20.0, "valve": 1},
                    {"time": 30.0, "valve": 1},
                    {"time": 40.0, "valve": 1}
                ]
            }
        }

        self.valve = RVM()
        self.stoprequest = False
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

    def run_profile(self, update_callback = None):
        """Run the current profile with the given device controllers"""

        if not self.valve.connected:
            messagebox.showerror("Connection Error", "Valve is not connected")
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
        self.stoprequest = False
        start_time = time.time()
        current_step_index = 0
        profile_complete = False
        # print("starttime profiles", start_time)
        # print("hoi")
        while not profile_complete and not self.stoprequest:
            elapsed_time = time.time() - start_time

            # Check if we need to move to next step
            if current_step_index < len(steps) - 1:
                next_step_time = steps[current_step_index + 1]["time"]
                # print("current step index", current_step_index, "total steps", steps, "next step time", next_step_time)
                if elapsed_time >= next_step_time:
                    current_step_index += 1
            
            # Get current step parameters
            current_step = steps[current_step_index]
            
            self.valve.set_valve(current_step["valve"])
        
            #if update_callback is called then we need to update the status with the corresponding data
            if update_callback:
                    update_callback({
                    "elapsed_time": elapsed_time,
                    "current_step": current_step_index + 1,
                    "total_steps": len(steps),
                    "valve": current_step["valve"],
                })
            # Check if profile is complete
            #such that the cpu doesn't overload
            time.sleep(0.1)
            if current_step_index == len(steps) - 1 and elapsed_time >= current_step["time"]:
                profile_complete = True
                

        return True
    
    def stop_profile(self):
        self.stoprequest = True
        ##home position
        # self.valve.set_valve(1)
        
class OnoffProfileManager:
    def __init__(self, UImfcs, UIcooling, UIvalve, profiles_dir="profiles_onetab"):
        #profiles_dir is the path where the profile will be saved
        self.profiles_dir = profiles_dir
        self.current_profile = None
        self.standard_profiles = {
            "Flow_Test": {
                "description": "Test flow rate changes",
                "steps": [
                    {"time": 0.0, "flow mfc1": 0.5, "flow mfc2": 0.5, "flow mfc3": 0.5,"temperature": 25.0, "valve": 1},
                    {"time": 10.0, "flow mfc1": 1.0, "flow mfc2": 0.5, "flow mfc3": 0.5,"temperature": 25.0, "valve": 1},
                    {"time": 20.0, "flow mfc1": 1.5, "flow mfc2": 0.5, "flow mfc3": 0.5,"temperature": 25.0, "valve": 1},
                    {"time": 30.0, "flow mfc1": 1.0, "flow mfc2": 0.5, "flow mfc3": 0.5, "temperature": 25.0, "valve": 1},
                    {"time": 40.0, "flow mfc1": 0.5, "flow mfc2": 0.5, "flow mfc3": 0.5, "temperature": 25.0, "valve": 1}
                ]
            }
        }

        self.mfcs = UImfcs
        self.cooling = UIcooling
        self.valve = UIvalve
        
        self.stoprequest = False
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

    def run_profile(self, temp_ambient, update_callback = None):
        """Run the current profile with the given device controllers"""
        # Ensuring that the MFC, cooling and valve are all connected
        print(self.mfcs[0].port, self.mfcs[1].port, self.mfcs[2].port)
        print(self.mfcs[0].connected , self.mfcs[1].connected , self.mfcs[2].connected , self.cooling.connected , self.valve.connected)
        
        # Check devices and ambient temp
        if not (self.mfcs[0].connected and self.mfcs[1].connected and self.mfcs[2].connected):
            messagebox.showerror("Connection Error", "One or more MFCs not connected.")
            return
        if not self.cooling.connected:
            messagebox.showerror("Connection Error", "Cooling not connected.")
            return
        if not self.valve.connected:
            messagebox.showerror("Connection Error", "Valve not connected.")
            return
        if not isinstance(temp_ambient, (int, float)):
            messagebox.showerror("Error", "Ambient temperature must be set.")
            return
        
        if not self.current_profile:
            messagebox.showerror("Error", "No profile loaded")
            return False
        steps = self.current_profile.get("steps", [])
        if not steps:
            messagebox.showerror("Error", "Profile has no steps")
            return False
        # Sort steps by time
        steps = sorted(steps, key=lambda x: x["time"])
        
        self.stoprequest = False
        
        start_time = time.time()
        current_step_index = 0
        profile_complete = False
        while not profile_complete and not self.stoprequest:
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
            self.cooling.set_temperature(current_step["temperature"], temp_ambient)
            self.valve.set_valve(current_step["valve"])
            
            # #if update_callback is called then we need to update the status with the corresponding data
            if update_callback:
                    update_callback({
                    "elapsed_time": elapsed_time,
                    "current_step": current_step_index + 1,
                    "total_steps": len(steps),
                    "flow mfc1": current_step["flow mfc1"],
                    "flow mfc2": current_step["flow mfc2"],
                    "flow mfc3": current_step["flow mfc3"],
                    "temperature": current_step["temperature"],
                    "valve": current_step["valve"]
                })
            # Check if profile is complete
            if current_step_index == len(steps) - 1 and elapsed_time >= current_step["time"]:
                profile_complete = True
        
        return True
    
    def stop_profile(self):
        self.stoprequest = True


class AutomatedSystemUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Automated System")
        self.root.geometry("1400x800")
        
        self.mfcprofilemanager = MFCProfileManager()
        self.coolingprofilemanager = CoolingProfileManager()
        self.valveprofilemanager = RVMProfileManager()

        
        ##Het volgende is niet zo logisch, alleen als je het niet zo doet, krijg je dus dat profilemanager en UI een andere bronkhorst te pakken gaan krijgen
        ##Daarnaast zijn de porten dan ook niet aligned aahh
        self.mfcs = self.mfcprofilemanager.mfcs
        self.cooling = self.coolingprofilemanager.cooling
        self.valve = self.valveprofilemanager.valve
        
        self.onoffprofilemanager = OnoffProfileManager(UImfcs= self.mfcs, UIcooling= self.cooling, UIvalve= self.valve)
        
        # Header frame for connection and status
        header_frame = ttk.Frame(self.root)
        header_frame.pack(side='top', fill='x', padx=5, pady=5)
        
        # Connection status frame
        connection_frame = ttk.Frame(header_frame)
        connection_frame.pack(side='right', padx=10)
        
        ttk.Label(connection_frame, text="Device Connections", font=("Arial", 10, "bold")).pack(fill = 'both', expand = True)
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
        ttk.Label(othervar_frame, text="Set Ambient Temperature", font=("Arial", 9, "bold")).pack(fill='both', expand=True)
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

        self.running_var_bar = tk.Label(header_frame, text="", anchor="w", relief="sunken")
        self.running_var_bar.pack(side='top', fill='x')
        
        overview_profile = ttk.Frame(self.root)
        overview_profile.pack(fill="x", padx=10, pady=5)
        
        ######PROFILE STATUS
        # Create a frame to contain the grid-like status table
        self.profile_status_frame = ttk.LabelFrame(overview_profile, text="Profile Overview")
        self.profile_status_frame.pack(side = "left", padx=10, pady=5)

        # Column headers
        ttk.Label(self.profile_status_frame, text="Profile", font=("Arial", 8, "bold")).grid(row=0, column=0, padx=5, sticky="w")
        ttk.Label(self.profile_status_frame, text="Elapsed Time", font=("Arial", 8, "bold")).grid(row=0, column=1, padx=5, sticky="w")
        ttk.Label(self.profile_status_frame, text="Step", font=("Arial", 8, "bold")).grid(row=0, column=2, padx=5, sticky="w")
        ttk.Label(self.profile_status_frame, text="Value", font=("Arial", 8, "bold")).grid(row=0, column=3, padx=5, sticky="w")

        # Row for MFC profile
        ttk.Label(self.profile_status_frame, text="MFC Running Profile").grid(row=1, column=0, padx=5, sticky="w")
        self.mfc_elapsed_label = ttk.Label(self.profile_status_frame, text="-")
        self.mfc_elapsed_label.grid(row=1, column=1, padx=5, sticky="w")
        self.mfc_step_label = ttk.Label(self.profile_status_frame, text="-")
        self.mfc_step_label.grid(row=1, column=2, padx=5, sticky="w")
        self.mfc_value_label = ttk.Label(self.profile_status_frame, text="-")
        self.mfc_value_label.grid(row=1, column=3, padx=5, sticky="w")

        # Cooling profile
        ttk.Label(self.profile_status_frame, text="Cooling Running Profile").grid(row=2, column=0, padx=5, sticky="w")
        self.cooling_elapsed_label = ttk.Label(self.profile_status_frame, text="-")
        self.cooling_elapsed_label.grid(row=2, column=1, padx=5, sticky="w")
        self.cooling_step_label = ttk.Label(self.profile_status_frame, text="-")
        self.cooling_step_label.grid(row=2, column=2, padx=5, sticky="w")
        self.cooling_value_label = ttk.Label(self.profile_status_frame, text="-")
        self.cooling_value_label.grid(row=2, column=3, padx=5, sticky="w")

        # Valve profile
        ttk.Label(self.profile_status_frame, text="Valve Running Profile").grid(row=3, column=0, padx=5, sticky="w")
        self.valve_elapsed_label = ttk.Label(self.profile_status_frame, text="-")
        self.valve_elapsed_label.grid(row=3, column=1, padx=5, sticky="w")
        self.valve_step_label = ttk.Label(self.profile_status_frame, text="-")
        self.valve_step_label.grid(row=3, column=2, padx=5, sticky="w")
        self.valve_value_label = ttk.Label(self.profile_status_frame, text="-")
        self.valve_value_label.grid(row=3, column=3, padx=5, sticky="w")

        # On/Off profile
        ttk.Label(self.profile_status_frame, text="On/Off Running Profile").grid(row=4, column=0, padx=5, sticky="w")
        self.onoff_elapsed_label = ttk.Label(self.profile_status_frame, text="-")
        self.onoff_elapsed_label.grid(row=4, column=1, padx=5, sticky="w")
        self.onoff_step_label = ttk.Label(self.profile_status_frame, text="-")
        self.onoff_step_label.grid(row=4, column=2, padx=5, sticky="w")
        self.onoff_value_label = ttk.Label(self.profile_status_frame, text="-")
        self.onoff_value_label.grid(row=4, column=3, padx=5, sticky="w")
        
        #####
        selectprofiles_frame = ttk.LabelFrame(overview_profile, text="Multiple Profile Runner")
        selectprofiles_frame.pack(side="right")

        # Label row

        ttk.Label(selectprofiles_frame, text="Valve Profiles").grid(row=0, column=1)
        ttk.Label(selectprofiles_frame, text="Cooling Profiles").grid(row=0, column=2)

        # MFC listbox with scrollbar
        ttk.Label(selectprofiles_frame, text="MFC Profiles").grid(row=0, column=0)
        mfc_listbox_frame = ttk.Frame(selectprofiles_frame)
        mfc_listbox_frame.grid(row=1, column=0, padx=5, pady=5)
        # # https://www.pythontutorial.net/tkinter/tkinter-listbox/#adding-a-scrollbar-to-the-listbox
        # # Making an empty profile listbox
        # Exportseleciton = False, such that when you select another listbox you still can have your selection
        self.selprof_mfc_listbox = tk.Listbox(mfc_listbox_frame, height=2, exportselection=False)
        self.selprof_mfc_listbox.pack(side='left', fill='y')
        mfc_v_scrollbar = ttk.Scrollbar(mfc_listbox_frame, orient=tk.VERTICAL, command=self.selprof_mfc_listbox.yview)
        mfc_v_scrollbar.pack(side='right', fill='y')
        self.selprof_mfc_listbox.config(yscrollcommand=mfc_v_scrollbar.set)
        
        # Valve Listbox with scrollbar
        valve_listbox_frame = ttk.Frame(selectprofiles_frame)
        valve_listbox_frame.grid(row=1, column=1, padx=5, pady=5)
        self.selprof_valve_listbox = tk.Listbox(valve_listbox_frame, height=2, exportselection=False)
        self.selprof_valve_listbox.pack(side='left', fill='y')
        valve_v_scrollbar = ttk.Scrollbar(valve_listbox_frame, orient=tk.VERTICAL, command=self.selprof_valve_listbox.yview)
        valve_v_scrollbar.pack(side='right', fill='y')
        self.selprof_valve_listbox.config(yscrollcommand=valve_v_scrollbar.set)

        # Cooling Listbox with scrollbar
        cooling_listbox_frame = ttk.Frame(selectprofiles_frame)
        cooling_listbox_frame.grid(row=1, column=2, padx=5, pady=5)
        self.selprof_cooling_listbox = tk.Listbox(cooling_listbox_frame, height=2, exportselection=False)
        self.selprof_cooling_listbox.pack(side='left', fill='y')
        cooling_v_scrollbar = ttk.Scrollbar(cooling_listbox_frame, orient=tk.VERTICAL, command=self.selprof_cooling_listbox.yview)
        cooling_v_scrollbar.pack(side='right', fill='y')
        self.selprof_cooling_listbox.config(yscrollcommand=cooling_v_scrollbar.set)


        # Populate listboxes
        for profile in self.mfcprofilemanager.get_profiles():
            self.selprof_mfc_listbox.insert(tk.END, profile)
        for profile in self.valveprofilemanager.get_profiles():
            self.selprof_valve_listbox.insert(tk.END, profile)
        for profile in self.coolingprofilemanager.get_profiles():
            self.selprof_cooling_listbox.insert(tk.END, profile)

        # Run Button
        ttk.Button(selectprofiles_frame, text="Run Selected Profiles", command=self.run_selected_profiles).grid(row=1, column=3, padx=10)

        
        # Notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True)

        self.create_menu()
        self.create_device_tab()
        self.create_onoffprofile_tab()
        self.create_mfcprofile_tab()
        self.create_coolingprofile_tab()
        self.create_valveprofile_tab()
        
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
 
        # ###update status bar
        # # Get mass flow rates from MFCs
        # mass_flow_1 = f"{self.mfcs[0].get_massflow():.2f} mL/min" if self.mfcs[0].connected else "N/A"
        # mass_flow_2 = f"{self.mfcs[1].get_massflow():.2f} mL/min" if self.mfcs[1].connected else "N/A"
        # mass_flow_3 = f"{self.mfcs[2].get_massflow():.2f} mL/min" if self.mfcs[2].connected else "N/A"

        # # Get temperature from cooling system
        # temperature = f"{self.cooling.get_temperature():.2f} °C" if self.cooling.connected else "N/A"

        # # Get valve position from valve
        # valve_position = self.valve.currentposition if self.valve.connected else "N/A"
        # self.running_var_bar.config(text=f"Reading Values   : MFC 1 Mass Flow Rate: {mass_flow_1} | MFC 2 Mass Flow Rate: {mass_flow_2} | MFC 3 Mass Flow Rate: {mass_flow_3} | Temperature: {temperature} | Valve Position: {valve_position}")
        # ####
        
        ##update device tab
        massflows = []
        
        for i in range(3):
            if self.mfcs[i].connected:
                flow = self.mfcs[i].get_massflow()
                flow_str = f"{flow:.2f} mL/min"
            else:
                flow = None
                flow_str = "-"
            massflows.append(flow_str)
            self.current_massflow_labels[i].config(text=f"Current mass flow rate: {flow_str}")

        if self.cooling.connected:
            temp = self.cooling.get_temperature()
            temp_str = f"{temp:.2f} °C"
        else:
            temp = None
            temp_str = "-"
        self.current_temperature_label.config(text=f"Current temperature: {temp_str}")

        if self.valve.connected:
            pos = self.valve.currentposition
        else:
            pos = "-"
        self.current_valve_label.config(text=f"Current position of the valve: {pos}")

        # Summary bar uses same values
        self.running_var_bar.config(
            text=(
                f"Reading Values   : "
                f"MFC 1 Mass Flow Rate: {massflows[0]} | "
                f"MFC 2 Mass Flow Rate: {massflows[1]} | "
                f"MFC 3 Mass Flow Rate: {massflows[2]} | "
                f"Temperature: {temp_str} | "
                f"Valve Position: {pos}"
            )
        )

        self.root.after(1000, self.update_run_var)






        # Schedule the next update, per 1s
        self.notebook.after(1000, self.update_run_var)

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

        coolingandvalve_frame = ttk.LabelFrame(device_tab)
        coolingandvalve_frame.pack(fill='x', padx=10, pady=5)
        
        ############	COOLING		###########################
        cooling_frame = ttk.LabelFrame(coolingandvalve_frame, text='Cooling')
        cooling_frame.grid(row=0, column=0, padx=10, pady=5, sticky='n')
        
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
        valve_frame = ttk.LabelFrame(coolingandvalve_frame, text='Valve')
        valve_frame.grid(row=0, column=1, padx=10, pady=5, sticky='n')
                
        # Valve position control
        ttk.Label(valve_frame, text="Valve Position:").grid(row=0, column=0, padx=10, pady=10)
        self.valve_pos_var = tk.IntVar(value=1)
        ttk.Combobox(valve_frame, textvariable=self.valve_pos_var, values=[1, 2], width=5).grid(row=0, column=1, padx=10, pady=10)
        
        # button to set the position of the valve
        set_valve_button = tk.Button(valve_frame, text="Set valve", command=self.set_valve)
        set_valve_button.grid(row=1, column=0, padx=10, pady=10)
        
        # Label to display the current position of the valve
        self.current_valve_label = tk.Label(valve_frame, text="Current position of the valve: Not available")
        self.current_valve_label.grid(row=2, column=0, padx=10, pady=10)
        
        # Connect button
        valve_connect_button = tk.Button(valve_frame, text="Connect", command=self.connect_valve)
        valve_connect_button.grid(row=3, column=0, padx=5, pady=5)
        
        # Disconnect button
        valve_disconnect_button = tk.Button(valve_frame, text="Disconnect", command=self.disconnect_valve)
        valve_disconnect_button.grid(row=3, column=1, padx=5, pady=5)
    
    def create_onoffprofile_tab(self):
        profile_tab = ttk.Frame(self.notebook)
        profile_tab.pack(fill = 'both', expand = True)
        self.notebook.add(profile_tab, text = 'On/Off Profile')
        
        ## Split into two frames
        list_frame = ttk.Frame(profile_tab)
        list_frame.pack(side= 'left', fill = 'both', expand=True, padx=5, pady=5)
        
        edit_frame = ttk.Frame(profile_tab)
        edit_frame.pack(side= 'right', fill= 'both', expand=True, padx=5, pady=5)
        
        ### Left frame / list frame
        ## Profile listbox with scrollbar
        # https://www.pythontutorial.net/tkinter/tkinter-listbox/#adding-a-scrollbar-to-the-listbox
        # Making an empty profile listbox
        self.onoffprofile_listbox = tk.Listbox(list_frame, selectmode = tk.SINGLE)
        self.onoffprofile_listbox.pack(fill= 'both', expand=True, padx=5, pady=5)
    
        # Putting all the profiles in the profile listbox
        self.update_onoffprofile_list()
        
        #Adding a scrollbar to the profile listbox
        v_scrollbar = ttk.Scrollbar(self.onoffprofile_listbox, orient = tk.VERTICAL, command = self.onoffprofile_listbox.yview)
        
        self.onoffprofile_listbox['yscrollcommand'] = v_scrollbar.set
        v_scrollbar.pack(side='right', fill='y')
        
        ##Adding the buttons to the left frame (list frame)
        # Profile list buttons
        button_frame = ttk.Frame(list_frame)
        button_frame.pack(fill='x', padx=5, pady=5)
        
        load_button = ttk.Button(button_frame, text="Load", command=self.load_onoffprofile)
        load_button.pack(side='left', padx=3, expand=True)
        
        delete_button = ttk.Button(button_frame, text="Delete", command=self.delete_onoffprofile)
        delete_button.pack(side='left', padx=3, expand=True)
        
        ##Right frame / edit frame
        # Profile info
        info_frame = ttk.Frame(edit_frame)
        info_frame.pack(fill='both', padx=5, pady=5)
        
        self.new_onoffprofile_label = ttk.Label(info_frame, text="")
        self.new_onoffprofile_label.pack(side = 'left', padx=5, expand=True, fill='x')
        
        profile_name_label = ttk.Label(info_frame, text="Name:").pack(side='left')
        self.onoffname_var = tk.StringVar()
        name_entry = ttk.Entry(info_frame, textvariable=self.onoffname_var)
        name_entry.pack(side='left', padx=5, expand=True, fill='x')
        
        profile_desc_label = ttk.Label(info_frame, text="Description:").pack(side='left')
        self.onoffdesc_var = tk.StringVar()
        desc_entry = ttk.Entry(info_frame, textvariable=self.onoffdesc_var)
        desc_entry.pack(side='left', padx=5, expand=True, fill='x')
        
        new_profile_btn = ttk.Button(info_frame, text = 'New Profile', command = self.create_new_onoffprofile)
        new_profile_btn.pack(side='right', padx=3, expand=True)
        
        # Steps in the right/frame
        steps_frame = ttk.Frame(edit_frame)
        steps_frame.pack(fill = 'both' , expand=True, padx=5, pady=5)
        
        #https://tk-tutorial.readthedocs.io/en/latest/tree/tree.html
        self.onoffsteps_tree = ttk.Treeview(
            steps_frame, 
            columns=("time", "flow mfc1", "flow mfc2", "flow mfc3", "temp", "valve"), 
            show="headings"
        )
        self.onoffsteps_tree.heading("time", text="Time (s)")
        self.onoffsteps_tree.heading("flow mfc1", text="Flow MFC 1 (mL/min)")
        self.onoffsteps_tree.heading("flow mfc2", text="Flow MFC 2 (mL/min)")
        self.onoffsteps_tree.heading("flow mfc3", text="Flow MFC 3 (mL/min)")
        self.onoffsteps_tree.heading("temp", text="Temperature (°C)")
        self.onoffsteps_tree.heading("valve", text="Valve Position (1 or 2)")
        
        self.onoffsteps_tree.column("time", width=80, anchor=tk.CENTER)
        self.onoffsteps_tree.column("flow mfc1", width=100, anchor=tk.CENTER)
        self.onoffsteps_tree.column("flow mfc2", width=100, anchor=tk.CENTER)
        self.onoffsteps_tree.column("flow mfc3", width=100, anchor=tk.CENTER)
        self.onoffsteps_tree.column("temp", width=100, anchor=tk.CENTER)
        self.onoffsteps_tree.column("valve", width=80, anchor=tk.CENTER)
        
        self.onoffsteps_tree.pack(fill = 'both' , expand=True)
        
        step_controls_frame = ttk.Frame(edit_frame)
        step_controls_frame.pack(fill='x', padx=5, pady=5)
        
        self.onoffprofile_time_label = ttk.Label(step_controls_frame, text="Time (s):").pack(side='left')
        self.onoffstep_time_var = tk.DoubleVar()
        step_time_entry = ttk.Entry(step_controls_frame, textvariable=self.onoffstep_time_var, width=8)
        step_time_entry.pack(side='left', padx=2)
        
        self.onoffprofile_mfc1_label = ttk.Label(step_controls_frame, text="Flow MFC 1 (mL/min):").pack(side='left')
        self.onoffstep_flow1_var = tk.DoubleVar()
        step_flow1_entry = ttk.Entry(step_controls_frame, textvariable=self.onoffstep_flow1_var, width=8)
        step_flow1_entry.pack(side='left', padx=2)

        self.onoffprofile_mfc2_label = ttk.Label(step_controls_frame, text="Flow MFC 2 (mL/min):").pack(side='left')
        self.onoffstep_flow2_var = tk.DoubleVar()
        step_flow2_entry = ttk.Entry(step_controls_frame, textvariable=self.onoffstep_flow2_var, width=8)
        step_flow2_entry.pack(side='left', padx=2)

        self.onoffprofile_mfc3_label = ttk.Label(step_controls_frame, text="Flow MFC 3 (mL/min):").pack(side='left')
        self.onoffstep_flow3_var = tk.DoubleVar()
        step_flow3_entry = ttk.Entry(step_controls_frame, textvariable=self.onoffstep_flow3_var, width=8)
        step_flow3_entry.pack(side='left', padx=2)
        
        self.onoffprofile_mfc4_label = ttk.Label(step_controls_frame, text="Temperature (°C):").pack(side='left')
        self.onoffstep_temp_var = tk.DoubleVar()
        step_temp_entry = ttk.Entry(step_controls_frame, textvariable=self.onoffstep_temp_var, width=8)
        step_temp_entry.pack(side='left', padx=2)
        
        self.onoffprofile_valve_label =  ttk.Label(step_controls_frame, text="Valve Position:").pack(side='left')
        self.onoffstep_valve_var = tk.IntVar() #integer variable, since the valve should be position on 1/2
        step_valve_combo = ttk.Combobox(
            step_controls_frame, 
            textvariable=self.onoffstep_valve_var, 
            values=[1, 2], 
            width=5
        )
        step_valve_combo.pack(side='left', padx=2)
        
        # Step buttons
        step_buttons_frame = ttk.Frame(edit_frame)
        step_buttons_frame.pack(fill='both')
        
        add_step_button = ttk.Button(step_buttons_frame, text="Add Step", command=self.onoffadd_step)
        add_step_button.pack(side='left', padx=2)
        
        remove_step_button = ttk.Button(step_buttons_frame, text="Remove Step", command=self.onoffremove_step)
        remove_step_button.pack(side='left', padx=2)
        
        clear_steps_button = ttk.Button(step_buttons_frame, text="Clear All Steps", command=self.onoffclear_steps)
        clear_steps_button.pack(side='left', padx=2)
        
        # Save and run buttons
        action_buttons_frame = ttk.Frame(edit_frame)
        action_buttons_frame.pack(fill='both')
        
        save_button = ttk.Button(action_buttons_frame, text="Save Profile", command=self.save_onoffprofile)
        save_button.pack(side='left', padx=2)
        
        run_button = ttk.Button(action_buttons_frame, text="Run Profile", command=self.run_onoffprofile)
        run_button.pack(side='left', padx=2)
        
        self.onoffstop_button = ttk.Button(action_buttons_frame, text="Stop", command=self.stop_onoffprofile)
        self.onoffstop_button.pack(side='left', padx=2)
        self.onoffstop_button.config(state=tk.DISABLED)
    
        # Initialize variables
        self.current_loaded_onoffprofile = None
        
    def create_mfcprofile_tab(self):
        profile_tab = ttk.Frame(self.notebook)
        profile_tab.pack(fill = 'both', expand = True)
        self.notebook.add(profile_tab, text = 'MFCs Profile')
        
        # ## Split into two frames
        list_frame = ttk.Frame(profile_tab, width = 400)
        list_frame.pack(side= 'left', fill = 'both', expand=True, padx=10, pady=10)
        list_frame.pack_propagate(False)

        
        edit_frame = ttk.Frame(profile_tab)
        edit_frame.pack(side= 'right', fill= 'both', expand=True, padx=10, pady=10)
        
        ### Left frame / list frame
        ## Profile listbox with scrollbar
        # https://www.pythontutorial.net/tkinter/tkinter-listbox/#adding-a-scrollbar-to-the-listbox
        # Making an empty profile listbox
        self.mfcprofile_listbox = tk.Listbox(list_frame, selectmode = tk.SINGLE)
        self.mfcprofile_listbox.pack(fill= 'both', expand=True, padx=5, pady=5)
    
        # Putting all the profiles in the profile listbox
        self.update_mfcprofile_list()
        
        #Adding a scrollbar to the profile listbox
        v_scrollbar = ttk.Scrollbar(self.mfcprofile_listbox, orient = tk.VERTICAL, command = self.mfcprofile_listbox.yview)
        
        self.mfcprofile_listbox['yscrollcommand'] = v_scrollbar.set
        v_scrollbar.pack(side='right', fill='y')
        
        ##Adding the buttons to the left frame (list frame)
        # Profile list buttons
        button_frame = ttk.Frame(list_frame)
        button_frame.pack(fill='x', padx=5, pady=5)
        
        load_button = ttk.Button(button_frame, text="Load", command=self.load_mfcprofile)
        load_button.pack(side='left', padx=3, expand=True)
        
        delete_button = ttk.Button(button_frame, text="Delete", command=self.delete_mfcprofile)
        delete_button.pack(side='left', padx=3, expand=True)
        
        ##Right frame / edit frame
        # Profile info
        info_frame = ttk.Frame(edit_frame)
        info_frame.pack(fill='both', padx=5, pady=5)
        
        self.new_mfcprofile_label = ttk.Label(info_frame, text="")
        self.new_mfcprofile_label.pack(side = 'left', padx=5, expand=True, fill='x')
        
        ttk.Label(info_frame, text="Name:").pack(side='left')
        self.mfcname_var = tk.StringVar()
        name_entry = ttk.Entry(info_frame, textvariable=self.mfcname_var)
        name_entry.pack(side='left', padx=5, expand=True, fill='x')
        
        ttk.Label(info_frame, text="Description:").pack(side='left')
        self.mfcdesc_var = tk.StringVar()
        desc_entry = ttk.Entry(info_frame, textvariable=self.mfcdesc_var)
        desc_entry.pack(side='left', padx=5, expand=True, fill='x')
        
        new_profile_btn = ttk.Button(info_frame, text = 'New Profile', command = self.create_new_mfcprofile)
        new_profile_btn.pack(side='right', padx=3, expand=True)
        
        # Steps in the right/frame
        steps_frame = ttk.Frame(edit_frame)
        steps_frame.pack(fill = 'both' , expand=True, padx=5, pady=5)
        
        #https://tk-tutorial.readthedocs.io/en/latest/tree/tree.html
        self.mfcsteps_tree = ttk.Treeview(
            steps_frame, 
            columns=("time", "flow mfc1", "flow mfc2", "flow mfc3", "temp", "valve"), 
            show="headings"
        )
        self.mfcsteps_tree.heading("time", text="Time (s)")
        self.mfcsteps_tree.heading("flow mfc1", text="Flow MFC 1 (mL/min)")
        self.mfcsteps_tree.heading("flow mfc2", text="Flow MFC 2 (mL/min)")
        self.mfcsteps_tree.heading("flow mfc3", text="Flow MFC 3 (mL/min)")
        
        self.mfcsteps_tree.column("time", width=250, anchor=tk.CENTER)
        self.mfcsteps_tree.column("flow mfc1", width=250, anchor=tk.CENTER)
        self.mfcsteps_tree.column("flow mfc2", width=250, anchor=tk.CENTER)
        self.mfcsteps_tree.column("flow mfc3", width=250, anchor=tk.CENTER)
        
        self.mfcsteps_tree.pack(fill = 'both' , expand=True)
        
        step_controls_frame = ttk.Frame(edit_frame)
        step_controls_frame.pack(fill='x', padx=5, pady=5)
        
        self.mfcprofile_time_label = ttk.Label(step_controls_frame, text="Time (s):").pack(side='left')
        self.mfcstep_time_var = tk.DoubleVar()
        step_time_entry = ttk.Entry(step_controls_frame, textvariable=self.mfcstep_time_var, width=8)
        step_time_entry.pack(side='left', padx=5)
        
        self.mfcprofile_mfc1_label = ttk.Label(step_controls_frame, text="Flow MFC 1 (mL/min):").pack(side='left')
        self.mfcstep_flow1_var = tk.DoubleVar()
        step_flow1_entry = ttk.Entry(step_controls_frame, textvariable=self.mfcstep_flow1_var, width=8)
        step_flow1_entry.pack(side='left', padx=5)

        self.mfcprofile_mfc2_label = ttk.Label(step_controls_frame, text="Flow MFC 2 (mL/min):").pack(side='left')
        self.mfcstep_flow2_var = tk.DoubleVar()
        step_flow2_entry = ttk.Entry(step_controls_frame, textvariable=self.mfcstep_flow2_var, width=8)
        step_flow2_entry.pack(side='left', padx=5)

        self.mfcprofile_mfc3_label = ttk.Label(step_controls_frame, text="Flow MFC 3 (mL/min):").pack(side='left')
        self.mfcstep_flow3_var = tk.DoubleVar()
        step_flow3_entry = ttk.Entry(step_controls_frame, textvariable=self.mfcstep_flow3_var, width=8)
        step_flow3_entry.pack(side='left', padx=5)
        
        # Step buttons
        step_buttons_frame = ttk.Frame(edit_frame)
        step_buttons_frame.pack(fill='both')
        
        add_step_button = ttk.Button(step_buttons_frame, text="Add Step", command=self.add_mfcstep)
        add_step_button.pack(side='left', padx=2)
        
        remove_step_button = ttk.Button(step_buttons_frame, text="Remove Step", command=self.remove_mfcstep)
        remove_step_button.pack(side='left', padx=2)
        
        clear_steps_button = ttk.Button(step_buttons_frame, text="Clear All Steps", command=self.clear_mfcsteps)
        clear_steps_button.pack(side='left', padx=2)
        
        # Save and run buttons
        action_buttons_frame = ttk.Frame(edit_frame)
        action_buttons_frame.pack(fill='both')
        
        save_button = ttk.Button(action_buttons_frame, text="Save Profile", command=self.save_mfcprofile)
        save_button.pack(side='left', padx=2)
        
        run_button = ttk.Button(action_buttons_frame, text="Run Profile", command=self.run_mfcprofile)
        run_button.pack(side='left', padx=2)
        
        self.mfcstop_button = ttk.Button(action_buttons_frame, text="Stop", command=self.stop_mfcprofile)
        self.mfcstop_button.pack(side='left', padx=2)
        self.mfcstop_button.config(state=tk.DISABLED)
        
    def create_coolingprofile_tab(self):
        profile_tab = ttk.Frame(self.notebook)
        profile_tab.pack(fill = 'both', expand = True)
        self.notebook.add(profile_tab, text = 'Cooling Profile')
        
        # ## Split into two frames
        list_frame = ttk.Frame(profile_tab, width = 400)
        list_frame.pack(side= 'left', fill = 'both', expand=True, padx=10, pady=10)
        list_frame.pack_propagate(False)

        
        edit_frame = ttk.Frame(profile_tab)
        edit_frame.pack(side= 'right', fill= 'both', expand=True, padx=10, pady=10)
        
        ### Left frame / list frame
        ## Profile listbox with scrollbar
        # https://www.pythontutorial.net/tkinter/tkinter-listbox/#adding-a-scrollbar-to-the-listbox
        # Making an empty profile listbox
        self.coolingprofile_listbox = tk.Listbox(list_frame, selectmode = tk.SINGLE)
        self.coolingprofile_listbox.pack(fill= 'both', expand=True, padx=5, pady=5)
    
        # Putting all the profiles in the profile listbox
        self.update_coolingprofile_list()
        
        #Adding a scrollbar to the profile listbox
        v_scrollbar = ttk.Scrollbar(self.coolingprofile_listbox, orient = tk.VERTICAL, command = self.coolingprofile_listbox.yview)
        
        self.coolingprofile_listbox['yscrollcommand'] = v_scrollbar.set
        v_scrollbar.pack(side='right', fill='y')
        
        ##Adding the buttons to the left frame (list frame)
        # Profile list buttons
        button_frame = ttk.Frame(list_frame)
        button_frame.pack(fill='x', padx=5, pady=5)
        
        load_button = ttk.Button(button_frame, text="Load", command=self.load_coolingprofile)
        load_button.pack(side='left', padx=3, expand=True)
        
        delete_button = ttk.Button(button_frame, text="Delete", command=self.delete_coolingprofile)
        delete_button.pack(side='left', padx=3, expand=True)
        
        ##Right frame / edit frame
        # Profile info
        info_frame = ttk.Frame(edit_frame)
        info_frame.pack(fill='both', padx=5, pady=5)
        
        self.new_coolingprofile_label = ttk.Label(info_frame, text="")
        self.new_coolingprofile_label.pack(side = 'left', padx=5, expand=True, fill='x')
        
        ttk.Label(info_frame, text="Name:").pack(side='left')
        self.coolingname_var = tk.StringVar()
        name_entry = ttk.Entry(info_frame, textvariable=self.coolingname_var)
        name_entry.pack(side='left', padx=5, expand=True, fill='x')
        
        ttk.Label(info_frame, text="Description:").pack(side='left')
        self.coolingdesc_var = tk.StringVar()
        desc_entry = ttk.Entry(info_frame, textvariable=self.coolingdesc_var)
        desc_entry.pack(side='left', padx=5, expand=True, fill='x')
        
        new_profile_btn = ttk.Button(info_frame, text = 'New Profile', command = self.create_new_coolingprofile)
        new_profile_btn.pack(side='right', padx=3, expand=True)
        
        # Steps in the right/frame
        steps_frame = ttk.Frame(edit_frame)
        steps_frame.pack(fill = 'both' , expand=True, padx=5, pady=5)
        
        #https://tk-tutorial.readthedocs.io/en/latest/tree/tree.html
        self.coolingsteps_tree = ttk.Treeview(
            steps_frame, 
            columns=("time", "temp"), 
            show="headings"
        )
        self.coolingsteps_tree.heading("time", text="Time (s)")
        self.coolingsteps_tree.heading("temp", text="Temperature (°C)")
        
        self.coolingsteps_tree.column("time", width=250, anchor=tk.CENTER)
        self.coolingsteps_tree.column("temp", width=250, anchor=tk.CENTER)
        self.coolingsteps_tree.pack(fill = 'both' , expand=True)
        
        step_controls_frame = ttk.Frame(edit_frame)
        step_controls_frame.pack(fill='x', padx=5, pady=5)
        
        self.coolingprofile_time_label = ttk.Label(step_controls_frame, text="Time (s):").pack(side='left')
        self.coolingstep_time_var = tk.DoubleVar()
        step_time_entry = ttk.Entry(step_controls_frame, textvariable=self.coolingstep_time_var, width=8)
        step_time_entry.pack(side='left', padx=5)
        
        self.coolingprofile_temp_label = ttk.Label(step_controls_frame, text="Temperature (°C):").pack(side='left')
        self.coolingstep_temp_var = tk.DoubleVar()
        step_temp_entry = ttk.Entry(step_controls_frame, textvariable=self.coolingstep_temp_var, width=8)
        step_temp_entry.pack(side='left', padx=2)
        
        # Step buttons
        step_buttons_frame = ttk.Frame(edit_frame)
        step_buttons_frame.pack(fill='both')
        
        add_step_button = ttk.Button(step_buttons_frame, text="Add Step", command=self.add_coolingstep)
        add_step_button.pack(side='left', padx=2)
        
        remove_step_button = ttk.Button(step_buttons_frame, text="Remove Step", command=self.remove_coolingstep)
        remove_step_button.pack(side='left', padx=2)
        
        clear_steps_button = ttk.Button(step_buttons_frame, text="Clear All Steps", command=self.clear_coolingsteps)
        clear_steps_button.pack(side='left', padx=2)
        
        # Save and run buttons
        action_buttons_frame = ttk.Frame(edit_frame)
        action_buttons_frame.pack(fill='both')
        
        save_button = ttk.Button(action_buttons_frame, text="Save Profile", command=self.save_coolingprofile)
        save_button.pack(side='left', padx=2)
        
        run_button = ttk.Button(action_buttons_frame, text="Run Profile", command=self.run_coolingprofile)
        run_button.pack(side='left', padx=2)
        
        self.coolingstop_button = ttk.Button(action_buttons_frame, text="Stop", command=self.stop_coolingprofile)
        self.coolingstop_button.pack(side='left', padx=2)
        self.coolingstop_button.config(state=tk.DISABLED)
        
        # # Status bar, to show what has been adjusted
        # self.status_var = tk.StringVar() 
        # self.status_bar = ttk.Label(edit_frame, textvariable=self.status_var)
        # self.status_bar.pack(fill='both', padx=5, pady=5)
        
        # Initialize variables
        # self.coolingcurrent_loaded_profile = None
    
    def create_valveprofile_tab(self):
        profile_tab = ttk.Frame(self.notebook)
        profile_tab.pack(fill = 'both', expand = True)
        self.notebook.add(profile_tab, text = 'Valve Profile')
        
        # ## Split into two frames
        list_frame = ttk.Frame(profile_tab, width = 400)
        list_frame.pack(side= 'left', fill = 'both', expand=True, padx=10, pady=10)
        list_frame.pack_propagate(False)

        edit_frame = ttk.Frame(profile_tab)
        edit_frame.pack(side= 'right', fill= 'both', expand=True, padx=10, pady=10)
        
        ### Left frame / list frame
        ## Profile listbox with scrollbar
        # https://www.pythontutorial.net/tkinter/tkinter-listbox/#adding-a-scrollbar-to-the-listbox
        # Making an empty profile listbox
        self.valveprofile_listbox = tk.Listbox(list_frame, selectmode = tk.SINGLE)
        self.valveprofile_listbox.pack(fill= 'both', expand=True, padx=5, pady=5)
    
        # Putting all the profiles in the profile listbox
        self.update_valveprofile_list()
        
        #Adding a scrollbar to the profile listbox
        v_scrollbar = ttk.Scrollbar(self.valveprofile_listbox, orient = tk.VERTICAL, command = self.valveprofile_listbox.yview)
        
        self.valveprofile_listbox['yscrollcommand'] = v_scrollbar.set
        v_scrollbar.pack(side='right', fill='y')
        
        ##Adding the buttons to the left frame (list frame)
        # Profile list buttons
        button_frame = ttk.Frame(list_frame)
        button_frame.pack(fill='x', padx=5, pady=5)
        
        load_button = ttk.Button(button_frame, text="Load", command=self.load_valveprofile)
        load_button.pack(side='left', padx=3, expand=True)
        
        delete_button = ttk.Button(button_frame, text="Delete", command=self.delete_valveprofile)
        delete_button.pack(side='left', padx=3, expand=True)
        
        ##Right frame / edit frame
        # Profile info
        info_frame = ttk.Frame(edit_frame)
        info_frame.pack(fill='both', padx=5, pady=5)
        
        self.new_valveprofile_label = ttk.Label(info_frame, text="")
        self.new_valveprofile_label.pack(side = 'left', padx=5, expand=True, fill='x')
        
        ttk.Label(info_frame, text="Name:").pack(side='left')
        self.valvename_var = tk.StringVar()
        name_entry = ttk.Entry(info_frame, textvariable=self.valvename_var)
        name_entry.pack(side='left', padx=5, expand=True, fill='x')
        
        ttk.Label(info_frame, text="Description:").pack(side='left')
        self.valvedesc_var = tk.StringVar()
        desc_entry = ttk.Entry(info_frame, textvariable=self.valvedesc_var)
        desc_entry.pack(side='left', padx=5, expand=True, fill='x')
        
        new_profile_btn = ttk.Button(info_frame, text = 'New Profile', command = self.create_new_valveprofile)
        new_profile_btn.pack(side='right', padx=3, expand=True)
        
        # Steps in the right/frame
        steps_frame = ttk.Frame(edit_frame)
        steps_frame.pack(fill = 'both' , expand=True, padx=5, pady=5)
        
        #https://tk-tutorial.readthedocs.io/en/latest/tree/tree.html
        self.valvesteps_tree = ttk.Treeview(
            steps_frame, 
            columns=("time", "valve"), 
            show="headings"
        )
        self.valvesteps_tree.heading("time", text="Time (s)")
        self.valvesteps_tree.heading("valve", text="Valve Position (1/2)")
        
        self.valvesteps_tree.column("time", width=250, anchor=tk.CENTER)
        self.valvesteps_tree.column("valve", width=250, anchor=tk.CENTER)
        
        self.valvesteps_tree.pack(fill = 'both' , expand=True)
        
        step_controls_frame = ttk.Frame(edit_frame)
        step_controls_frame.pack(fill='x', padx=5, pady=5)
        
        self.valveprofile_time_label = ttk.Label(step_controls_frame, text="Time (s):").pack(side='left')
        self.valvestep_time_var = tk.DoubleVar()
        step_time_entry = ttk.Entry(step_controls_frame, textvariable=self.valvestep_time_var, width=8)
        step_time_entry.pack(side='left', padx=5)
        
        self.valveprofile_valve_label =  ttk.Label(step_controls_frame, text="Valve Position:").pack(side='left')
        self.valvestep_valve_var = tk.IntVar() #integer variable, since the valve should be position on 1/2
        step_valve_combo = ttk.Combobox(
            step_controls_frame, 
            textvariable=self.valvestep_valve_var, 
            values=[1, 2], 
            width=5
        )
        step_valve_combo.pack(side='left', padx=2)
        
        # Step buttons
        step_buttons_frame = ttk.Frame(edit_frame)
        step_buttons_frame.pack(fill='both')
        
        add_step_button = ttk.Button(step_buttons_frame, text="Add Step", command=self.add_valvestep)
        add_step_button.pack(side='left', padx=2)
        
        remove_step_button = ttk.Button(step_buttons_frame, text="Remove Step", command=self.remove_valvestep)
        remove_step_button.pack(side='left', padx=2)
        
        clear_steps_button = ttk.Button(step_buttons_frame, text="Clear All Steps", command=self.clear_valvesteps)
        clear_steps_button.pack(side='left', padx=2)
        
        # Save and run buttons
        action_buttons_frame = ttk.Frame(edit_frame)
        action_buttons_frame.pack(fill='both')
        
        save_button = ttk.Button(action_buttons_frame, text="Save Profile", command=self.save_valveprofile)
        save_button.pack(side='left', padx=2)
        
        run_button = ttk.Button(action_buttons_frame, text="Run Profile", command=self.run_valveprofile)
        run_button.pack(side='left', padx=2)
        
        self.valvestop_button = ttk.Button(action_buttons_frame, text="Stop", command=self.stop_valveprofile)
        self.valvestop_button.pack(side='left', padx=2)
        self.valvestop_button.config(state=tk.DISABLED)
        
        # # Status bar, to show what has been adjusted
        # self.status_var = tk.StringVar() 
        # self.status_bar = ttk.Label(edit_frame, textvariable=self.status_var)
        # self.status_bar.pack(fill='both', padx=5, pady=5)
        
        # Initialize variables
        # self.valvecurrent_loaded_profile = None

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
        self.notebook.after(1000, lambda: self.update_massflow(index)) #updating the MFC flow rate reading each 1s
        
    def set_temperature(self):
        if self.cooling.connected is False:
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
        current_temp = self.cooling.get_temperature()
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
        current_position = self.valve.currentposition
        self.update_run_var()
        if current_position is not None:
            self.current_valve_label.config(text=f"Current position of the valve: {current_position}")
        else:
            self.status_var.set("Failed to read the position of the valve.")
    
    ####MFC PROFILE
    def update_mfcprofile_list(self):
        """Refresh the list of available profiles"""
        #https://youtu.be/Vm0ivVxNaA8
        
        #Delete all the items from the listbox
        self.mfcprofile_listbox.delete(0, tk.END)
        
        #Add all the profiles to the listbox
        for profile in self.mfcprofilemanager.get_profiles():
            self.mfcprofile_listbox.insert(tk.END, profile)  #listbox.insert(index, element)

    def load_mfcprofile(self):
        """Load the selected profile into the editor"""
        #https://pythonassets.com/posts/listbox-in-tk-tkinter/
        selection = self.mfcprofile_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a profile to load")
            return
        
        #To ensure that you only select the first selected
        profile_name = self.mfcprofile_listbox.get(selection[0])
        profile = self.mfcprofilemanager.load_profile(profile_name)
        
        self.new_mfcprofile_label.config(text = "")
        
        if profile:
            # self.mfccurrent_loaded_profile = profile_name
            #Update the name of the profile
            self.mfcname_var.set(profile_name)
            #Update the description in the field
            self.mfcdesc_var.set(profile.get("description", ""))
            
            # Clear the existing steps
            for item in self.mfcsteps_tree.get_children():
                self.mfcsteps_tree.delete(item)
            
            # Add new steps
            for step in profile.get("steps", []):
                self.mfcsteps_tree.insert("", tk.END, values=(
                    step["time"],
                    step["flow mfc1"],
                    step["flow mfc2"],
                    step["flow mfc3"]
                ))
            
            self.status_var.set(f"Loaded profile: {profile_name}")
        
    def delete_mfcprofile(self):
        """Delete the selected profile"""
        #https://pythonassets.com/posts/listbox-in-tk-tkinter/
        selection = self.mfcprofile_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a profile to delete")
            return
            
        profile_name = self.mfcprofile_listbox.get(selection[0]) #To ensure that you only select the first selected
        
        if messagebox.askyesno("Confirm", f"Delete profile '{profile_name}'?"):
            if self.mfcprofilemanager.delete_profile(profile_name):
                #Updating the new profile list
                self.update_mfcprofile_list() 
                #Changing the status
                self.status_var.set(f"Deleted profile: {profile_name}")
            else:
                messagebox.showerror("Error", f"Failed to delete the profile: '{profile_name}'")
                
    def create_new_mfcprofile(self):
        #Clearing all input fields and steps
        self.mfcname_var.set("")
        self.mfcdesc_var.set("")
        self.mfcstep_time_var.set("0")
        self.mfcstep_flow1_var.set("0")
        self.mfcstep_flow2_var.set("0")
        self.mfcstep_flow3_var.set("0")
        # self.mfcstep_temp_var.set("0")
        # self.mfcstep_valve_var.set("0")
        
        for item in self.mfcsteps_tree.get_children():
            self.mfcsteps_tree.delete(item)
        
        self.new_mfcprofile_label.config(text = "New profile", foreground = "green")
        
    def add_mfcstep(self):
        """Add a new step to the current profile"""
        try:
            time_val = float(self.mfcstep_time_var.get())
            flow1_val = float(self.mfcstep_flow1_var.get())
            flow2_val = float(self.mfcstep_flow2_var.get())
            flow3_val = float(self.mfcstep_flow3_var.get())
            # temp_val = float(self.mfcstep_temp_var.get())
            # valve_val = int(self.mfcstep_valve_var.get())
            
            if time_val < 0:
                raise ValueError("Time cannot be negative")
            # if valve_val not in [1, 2]:
            #     raise ValueError("Position of the valve must be 1 or 2")
            
            # Check if the time already exists
            for child in self.mfcsteps_tree.get_children():
                if float(self.mfcsteps_tree.item(child, "values")[0]) == time_val:
                    if not messagebox.askyesno("Confirm", f"Step at time {time_val}s already exists. Overwrite?"):
                        return #if True, thus no then return
                    self.mfcsteps_tree.delete(child)
                    break
            
            self.mfcsteps_tree.insert("", tk.END, values=(time_val, flow1_val, flow2_val, flow3_val)) #, temp_val, valve_val))
            
        except ValueError as error:
            messagebox.showerror("Error", f"Invalid input: {error}")
    
    def remove_mfcstep(self):
        """Remove the selected step"""
        selection = self.mfcsteps_tree.selection()
        if selection:
            self.mfcsteps_tree.delete(selection)
    
    def clear_mfcsteps(self):
        """Clear all steps"""
        if messagebox.askyesno("Confirm", "Clear all the steps?"):
            #Obtain all the steps and delete all the steps
            for item in self.mfcsteps_tree.get_children():
                self.mfcsteps_tree.delete(item)
    
    def save_mfcprofile(self):
        """Save the current profile"""
        #Getting the name
        name = self.mfcname_var.get().strip()
        
        #Ensuring that the name isn't empty
        if not name:
            messagebox.showwarning("Warning", "Profile name cannot be empty")
            return
        
        # Collect steps from the profile
        steps = []
        for child in self.mfcsteps_tree.get_children():
            #To obtain all the values of the steps
            values = self.mfcsteps_tree.item(child, "values")
            steps.append({
                "time": float(values[0]),
                "flow mfc1": float(values[1]),
                "flow mfc2": float(values[2]),
                "flow mfc3": float(values[3])
                # "temperature": float(values[4]),
                # "valve": int(values[5])
            })
        
        # Sort steps by time
        #https://docs.python.org/3/howto/sorting.html
        steps = sorted(steps, key=lambda steps: steps["time"])
        
        # Create the profile data
        profile_data = {
            "description": self.mfcdesc_var.get(),
            "steps": steps
        }
        
        if self.mfcprofilemanager.save_profile(name, profile_data):
            self.update_mfcprofile_list()
            self.status_var.set(f"Saved profile: {name}")
        else:
            messagebox.showerror("Error", f"Failed to save profile '{name}'")
    
    def run_mfcprofile(self):
        """Run the current profile"""    
            
        if not (self.mfcs[0].connected and self.mfcs[1].connected and self.mfcs[2].connected): #and self.cooling.connected and self.valve.connected):
            messagebox.showwarning("Error", "One or more devices are not connected")
            return False
          
        #Get the name of the profile without spaces, such that the .json file can be loaded later
        name = self.mfcname_var.get().strip()
        
        #Checking whether the name is empty
        if not name:
            messagebox.showwarning("Warning", "Please load or create a profile first")
            return

        # Load the profile that needs to be runned
        profile = self.mfcprofilemanager.load_profile(name)
        if not profile:
            messagebox.showerror("Error", f"Failed to load profile: '{name}'")
            return
        
        self.update_run_var()
        #Enabling the stop button, since you can now stop a running profile
        self.mfcstop_button.config(state=tk.NORMAL) 
        
        # Start profile in a separate thread, such that the UI doesn't freeze until it finishes
        # And you'll still be able to see what happens, e.g. popup of not connection
        self.mfcprofile_thread = threading.Thread(
            target=self.run_mfcprofile_thread,  
            daemon=True         # Stops threading by pressing an event, e.g. pressing on stop button
        )
        self.mfcprofile_thread.start()
    
    def run_mfcprofile_thread(self):
        """Thread function to run the profile"""
        try:
            # Displaying which profile is running
            self.status_var.set(f"Running profile: {self.mfcname_var.get()}")
            self.mfcprofilemanager.run_profile(update_callback=self.update_mfcprofile_var)
            # self.notebook.after(0, lambda: self.update_run_status)
            self.notebook.after(0, lambda: self.mfcprofile_complete)

        except Exception as e:
            self.notebook.after(0, lambda: self.mfcprofile_error(e))
    
    def mfcprofile_complete(self):
        """Called when profile completes successfully"""
        self.mfcstop_button.config(state=tk.DISABLED)
        self.status_var.set("Profile run completed")
    
    def mfcprofile_error(self, error):
        """Called when profile run encounters an error"""
        self.mfcstop_button.config(state=tk.DISABLED)
        messagebox.showerror("Error", f"Profile run failed: {error}")
        self.status_var.set("Profile run failed")
    
    def stop_mfcprofile(self):
        """Stop the currently running profile"""
        self.mfcprofilemanager.stop_profile()
        self.mfcstop_button.config(state=tk.DISABLED)
        self.status_var.set("Profile run stopped by user")

    def update_mfcprofile_var(self, status):
        self.mfc_elapsed_label.config(text=f"{status['elapsed_time']:.1f}s")
        self.mfc_step_label.config(text=f"{status['current_step']}/{status['total_steps']}")
        self.mfc_value_label.config(text=f"{status['flow mfc1']:.2f}, {status['flow mfc2']:.2f}, {status['flow mfc3']:.2f} mL/min")
            
        # Schedule the next update, per 1s
        self.notebook.after(1000, lambda: self.update_mfcprofile_var)
        
    
    ###COOLING PROFILE
        
    def update_coolingprofile_list(self):
        """Refresh the list of available profiles"""
        #https://youtu.be/Vm0ivVxNaA8
        
        #Delete all the items from the listbox
        self.coolingprofile_listbox.delete(0, tk.END)
        
        #Add all the profiles to the listbox
        for profile in self.coolingprofilemanager.get_profiles():
            self.coolingprofile_listbox.insert(tk.END, profile)  #listbox.insert(index, element)

    def load_coolingprofile(self):
        """Load the selected profile into the editor"""
        #https://pythonassets.com/posts/listbox-in-tk-tkinter/
        selection = self.coolingprofile_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a profile to load")
            return
        
        #To ensure that you only select the first selected
        profile_name = self.coolingprofile_listbox.get(selection[0])
        profile = self.coolingprofilemanager.load_profile(profile_name)
        
        self.new_coolingprofile_label.config(text = "")
        
        if profile:
            # self.coolingcurrent_loaded_profile = profile_name
            #Update the name of the profile
            self.coolingname_var.set(profile_name)
            #Update the description in the field
            self.coolingdesc_var.set(profile.get("description", ""))
            
            # Clear the existing steps
            for item in self.coolingsteps_tree.get_children():
                self.coolingsteps_tree.delete(item)
            
            # Add new steps
            for step in profile.get("steps", []):
                self.coolingsteps_tree.insert("", tk.END, values=(
                    step["time"],
                    step["temperature"]
                ))
            
            self.status_var.set(f"Loaded profile: {profile_name}")
        
    def delete_coolingprofile(self):
        """Delete the selected profile"""
        #https://pythonassets.com/posts/listbox-in-tk-tkinter/
        selection = self.coolingprofile_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a profile to delete")
            return
            
        profile_name = self.coolingprofile_listbox.get(selection[0]) #To ensure that you only select the first selected
        
        if messagebox.askyesno("Confirm", f"Delete profile '{profile_name}'?"):
            if self.coolingprofilemanager.delete_profile(profile_name):
                #Updating the new profile list
                self.update_coolingprofile_list() 
                #Changing the status
                self.status_var.set(f"Deleted profile: {profile_name}")
            else:
                messagebox.showerror("Error", f"Failed to delete the profile: '{profile_name}'")
                
    def create_new_coolingprofile(self):
        #Clearing all input fields and steps
        self.coolingname_var.set("")
        self.coolingdesc_var.set("")
        self.coolingstep_time_var.set("0")
        self.coolingstep_temp_var.set("0")
        
        for item in self.coolingsteps_tree.get_children():
            self.coolingsteps_tree.delete(item)
        
        self.new_coolingprofile_label.config(text = "New profile", foreground = "green")
        
    def add_coolingstep(self):
        """Add a new step to the current profile"""
        try:
            time_val = float(self.coolingstep_time_var.get())
            temp_val = float(self.coolingstep_temp_var.get())
            
            if time_val < 0:
                raise ValueError("Time cannot be negative")

            # Check if the time already exists
            for child in self.coolingsteps_tree.get_children():
                if float(self.coolingsteps_tree.item(child, "values")[0]) == time_val:
                    if not messagebox.askyesno("Confirm", f"Step at time {time_val}s already exists. Overwrite?"):
                        return #if True, thus no then return
                    self.coolingsteps_tree.delete(child)
                    break
            
            self.coolingsteps_tree.insert("", tk.END, values=(time_val, temp_val))
            
        except ValueError as error:
            messagebox.showerror("Error", f"Invalid input: {error}")
    
    def remove_coolingstep(self):
        """Remove the selected step"""
        selection = self.coolingsteps_tree.selection()
        if selection:
            self.coolingsteps_tree.delete(selection)
    
    def clear_coolingsteps(self):
        """Clear all steps"""
        if messagebox.askyesno("Confirm", "Clear all the steps?"):
            #Obtain all the steps and delete all the steps
            for item in self.coolingsteps_tree.get_children():
                self.coolingsteps_tree.delete(item)
    
    def save_coolingprofile(self):
        """Save the current profile"""
        #Getting the name
        name = self.coolingname_var.get().strip()
        
        #Ensuring that the name isn't empty
        if not name:
            messagebox.showwarning("Warning", "Profile name cannot be empty")
            return
        
        # Collect steps from the profile
        steps = []
        for child in self.coolingsteps_tree.get_children():
            #To obtain all the values of the steps
            values = self.coolingsteps_tree.item(child, "values")
            steps.append({
                "time": float(values[0]),
                "temperature": float(values[1])
            })
        
        # Sort steps by time
        #https://docs.python.org/3/howto/sorting.html
        steps = sorted(steps, key=lambda steps: steps["time"])
        
        # Create the profile data
        profile_data = {
            "description": self.coolingdesc_var.get(),
            "steps": steps
        }
        
        if self.coolingprofilemanager.save_profile(name, profile_data):
            self.update_coolingprofile_list()
            self.status_var.set(f"Saved profile: {name}")
        else:
            messagebox.showerror("Error", f"Failed to save profile '{name}'")
    
    def run_coolingprofile(self):
        """Run the current profile"""    
            
        if not self.cooling.connected:
            messagebox.showwarning("Error", "One or more devices are not connected")
            return False
        
        if not isinstance(self.ambient_temp, (int, float)):
            messagebox.showwarning("Invalid Input", "Ambient Temperature has not been set yet or is an non-numeric value.")
            return False
        #Get the name of the profile without spaces, such that the .json file can be loaded later
        name = self.coolingname_var.get().strip()
        
        #Checking whether the name is empty
        if not name:
            messagebox.showwarning("Warning", "Please load or create a profile first")
            return

        # Load the profile that needs to be runned
        profile = self.coolingprofilemanager.load_profile(name)
        if not profile:
            messagebox.showerror("Error", f"Failed to load profile: '{name}'")
            return
        
        self.update_run_var()
        #Enabling the stop button, since you can now stop a running profile
        self.coolingstop_button.config(state=tk.NORMAL) 
        

        
        # Start profile in a separate thread, such that the UI doesn't freeze until it finishes
        # And you'll still be able to see what happens, e.g. popup of not connection
        self.coolingprofile_thread = threading.Thread(
            target=self.run_coolingprofile_thread,  
            daemon=True         # Stops threading by pressing an event, e.g. pressing on stop button
        )
        self.coolingprofile_thread.start()
    
    def run_coolingprofile_thread(self):
        """Thread function to run the profile"""
        try:
            # Displaying which profile is running
            self.status_var.set(f"Running profile: {self.coolingname_var.get()}")
            self.coolingprofilemanager.run_profile(temp_ambient = self.ambient_temp, update_callback=self.update_coolingprofile_var)
            self.notebook.after(0, lambda: self.coolingprofile_complete)

        except Exception as e:
            self.notebook.after(0, lambda: self.coolingprofile_error(e))
    
    def coolingprofile_complete(self):
        """Called when profile completes successfully"""
        self.coolingstop_button.config(state=tk.DISABLED)
        self.status_var.set("Profile run completed")
    
    def coolingprofile_error(self, error):
        """Called when profile run encounters an error"""
        self.coolingstop_button.config(state=tk.DISABLED)
        messagebox.showerror("Error", f"Profile run failed: {error}")
        self.status_var.set("Profile run failed")
    
    def stop_coolingprofile(self):
        """Stop the currently running profile"""
        self.coolingprofilemanager.stop_profile()
        self.coolingstop_button.config(state=tk.DISABLED)
        self.status_var.set("Profile run stopped by user")

    def update_coolingprofile_var(self, status):
        self.cooling_elapsed_label.config(text=f"{status['elapsed_time']:.1f}s")
        self.cooling_step_label.config(text=f"{status['current_step']}/{status['total_steps']}")
        self.cooling_value_label.config(text=f"{status['temperature']:.2f} °C")
        # Schedule the next update, per 1s
        self.notebook.after(1000, lambda: self.update_coolingprofile_var)

    ####VALVE PROFILE
    def update_valveprofile_list(self):
        """Refresh the list of available profiles"""
        #https://youtu.be/Vm0ivVxNaA8
        
        #Delete all the items from the listbox
        self.valveprofile_listbox.delete(0, tk.END)
        
        #Add all the profiles to the listbox
        for profile in self.valveprofilemanager.get_profiles():
            self.valveprofile_listbox.insert(tk.END, profile)  #listbox.insert(index, element)

    def load_valveprofile(self):
        """Load the selected profile into the editor"""
        #https://pythonassets.com/posts/listbox-in-tk-tkinter/
        selection = self.valveprofile_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a profile to load")
            return
        
        #To ensure that you only select the first selected
        profile_name = self.valveprofile_listbox.get(selection[0])
        profile = self.valveprofilemanager.load_profile(profile_name)
        
        self.new_valveprofile_label.config(text = "")
        
        if profile:
            # self.valvecurrent_loaded_profile = profile_name
            #Update the name of the profile
            self.valvename_var.set(profile_name)
            #Update the description in the field
            self.valvedesc_var.set(profile.get("description", ""))
            
            # Clear the existing steps
            for item in self.valvesteps_tree.get_children():
                self.valvesteps_tree.delete(item)
            
            # Add new steps
            for step in profile.get("steps", []):
                self.valvesteps_tree.insert("", tk.END, values=(
                    step["time"],
                    step["valve"]
                ))
            
            self.status_var.set(f"Loaded profile: {profile_name}")
        
    def delete_valveprofile(self):
        """Delete the selected profile"""
        #https://pythonassets.com/posts/listbox-in-tk-tkinter/
        selection = self.valveprofile_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a profile to delete")
            return
            
        profile_name = self.valveprofile_listbox.get(selection[0]) #To ensure that you only select the first selected
        
        if messagebox.askyesno("Confirm", f"Delete profile '{profile_name}'?"):
            if self.valveprofilemanager.delete_profile(profile_name):
                #Updating the new profile list
                self.update_valveprofile_list() 
                #Changing the status
                self.status_var.set(f"Deleted profile: {profile_name}")
            else:
                messagebox.showerror("Error", f"Failed to delete the profile: '{profile_name}'")
                
    def create_new_valveprofile(self):
        #Clearing all input fields and steps
        self.valvename_var.set("")
        self.valvedesc_var.set("")
        self.valvestep_time_var.set("0")
        self.valvestep_valve_var.set("0")
        
        for item in self.valvesteps_tree.get_children():
            self.valvesteps_tree.delete(item)
        
        self.new_valveprofile_label.config(text = "New profile", foreground = "green")
        
    def add_valvestep(self):
        """Add a new step to the current profile"""
        try:
            time_val = float(self.valvestep_time_var.get())
            valve_val = int(self.valvestep_valve_var.get())
            
            if time_val < 0:
                raise ValueError("Time cannot be negative")
            
            
            ###ALS WE OOK POSITIE 3 ERIN GAAN DOEN MOET DIT GEWIJZIGD WORDEN
            if valve_val not in [1, 2]:
                raise ValueError("Position of the valve must be 1 or 2")
            
            # Check if the time already exists
            for child in self.valvesteps_tree.get_children():
                if float(self.valvesteps_tree.item(child, "values")[0]) == time_val:
                    if not messagebox.askyesno("Confirm", f"Step at time {time_val}s already exists. Overwrite?"):
                        return #if True, thus no then return
                    self.valvesteps_tree.delete(child)
                    break
            
            self.valvesteps_tree.insert("", tk.END, values=(time_val, valve_val))
            
        except ValueError as error:
            messagebox.showerror("Error", f"Invalid input: {error}")
    
    def remove_valvestep(self):
        """Remove the selected step"""
        selection = self.valvesteps_tree.selection()
        if selection:
            self.valvesteps_tree.delete(selection)
    
    def clear_valvesteps(self):
        """Clear all steps"""
        if messagebox.askyesno("Confirm", "Clear all the steps?"):
            #Obtain all the steps and delete all the steps
            for item in self.valvesteps_tree.get_children():
                self.valvesteps_tree.delete(item)
    
    def save_valveprofile(self):
        """Save the current profile"""
        #Getting the name
        name = self.valvename_var.get().strip()
        
        #Ensuring that the name isn't empty
        if not name:
            messagebox.showwarning("Warning", "Profile name cannot be empty")
            return
        
        # Collect steps from the profile
        steps = []
        for child in self.valvesteps_tree.get_children():
            #To obtain all the values of the steps
            values = self.valvesteps_tree.item(child, "values")
            steps.append({
                "time": float(values[0]),
                "valve": int(values[1])
            })
        
        # Sort steps by time
        #https://docs.python.org/3/howto/sorting.html
        steps = sorted(steps, key=lambda steps: steps["time"])
        
        # Create the profile data
        profile_data = {
            "description": self.valvedesc_var.get(),
            "steps": steps
        }
        
        if self.valveprofilemanager.save_profile(name, profile_data):
            self.update_valveprofile_list()
            self.status_var.set(f"Saved profile: {name}")
        else:
            messagebox.showerror("Error", f"Failed to save profile '{name}'")
    
    def run_valveprofile(self):
        """Run the current profile"""    
            
        if not self.valve.connected:
            messagebox.showwarning("Error", "One or more devices are not connected")
            return False
          
        #Get the name of the profile without spaces, such that the .json file can be loaded later
        name = self.valvename_var.get().strip()
        
        #Checking whether the name is empty
        if not name:
            messagebox.showwarning("Warning", "Please load or create a profile first")
            return

        # Load the profile that needs to be runned
        profile = self.valveprofilemanager.load_profile(name)
        if not profile:
            messagebox.showerror("Error", f"Failed to load profile: '{name}'")
            return
        
        self.update_run_var()
        #Enabling the stop button, since you can now stop a running profile
        self.valvestop_button.config(state=tk.NORMAL) 
        
        # Start profile in a separate thread, such that the UI doesn't freeze until it finishes
        # And you'll still be able to see what happens, e.g. popup of not connection
        self.valveprofile_thread = threading.Thread(
            target=self.run_valveprofile_thread,  
            daemon=True         # Stops threading by pressing an event, e.g. pressing on stop button
        )
        self.valveprofile_thread.start()
    
    def run_valveprofile_thread(self):
        """Thread function to run the profile"""
        try:
            # Displaying which profile is running
            self.status_var.set(f"Running profile: {self.valvename_var.get()}")
            self.valveprofilemanager.run_profile(update_callback=self.update_valveprofile_var)
            # self.notebook.after(0, lambda: self.update_run_status)
            self.notebook.after(0, lambda: self.valveprofile_complete)

        except Exception as e:
            self.notebook.after(0, lambda: self.valveprofile_error(e))
    
    def valveprofile_complete(self):
        """Called when profile completes successfully"""
        self.valvestop_button.config(state=tk.DISABLED)
        self.status_var.set("Profile run completed")
    
    def valveprofile_error(self, error):
        """Called when profile run encounters an error"""
        self.valvestop_button.config(state=tk.DISABLED)
        messagebox.showerror("Error", f"Profile run failed: {error}")
        self.status_var.set("Profile run failed")
    
    def stop_valveprofile(self):
        """Stop the currently running profile"""
        self.valveprofilemanager.stop_profile()
        self.valvestop_button.config(state=tk.DISABLED)
        self.status_var.set("Profile run stopped by user")

    def update_valveprofile_var(self, status):
        self.valve_elapsed_label.config(text=f"{status['elapsed_time']:.1f}s")
        self.valve_step_label.config(text=f"{status['current_step']}/{status['total_steps']}")
        self.valve_value_label.config(text=f"Position {status['valve']}")
        # Schedule the next update, per 1s
        self.notebook.after(1000, lambda: self.update_valveprofile_var)

    def run_selected_profiles(self):
        mfc_sel = self.selprof_mfc_listbox.curselection()
        valve_sel = self.selprof_valve_listbox.curselection()
        cooling_sel = self.selprof_cooling_listbox.curselection()

        if not mfc_sel or not valve_sel or not cooling_sel:
            messagebox.showwarning("Selection Error", "Please select a profile from each list.")
            return

        mfc_name = self.selprof_mfc_listbox.get(mfc_sel[0])
        cooling_name = self.selprof_cooling_listbox.get(cooling_sel[0])
        valve_name = self.selprof_valve_listbox.get(valve_sel[0])

        # Load profiles
        if not self.mfcprofilemanager.load_profile(mfc_name):
            messagebox.showerror("Error", f"Failed to load MFC profile '{mfc_name}'")
            return
        if not self.coolingprofilemanager.load_profile(cooling_name):
            messagebox.showerror("Error", f"Failed to load Cooling profile '{cooling_name}'")
            return
        if not self.valveprofilemanager.load_profile(valve_name):
            messagebox.showerror("Error", f"Failed to load Valve profile '{valve_name}'")
            return

        # Check devices and ambient temp
        if not (self.mfcs[0].connected and self.mfcs[1].connected and self.mfcs[2].connected):
            messagebox.showerror("Connection Error", "One or more MFCs not connected.")
            return
        if not self.cooling.connected:
            messagebox.showerror("Connection Error", "Cooling not connected.")
            return
        if not self.valve.connected:
            messagebox.showerror("Connection Error", "Valve not connected.")
            return
        if not isinstance(self.ambient_temp, (int, float)):
            messagebox.showerror("Error", "Ambient temperature must be set.")
            return
        
        self.update_run_var()
        
        # Start all three profiles in threads
        threading.Thread(target=self.run_mfcprofile_thread, daemon=True).start()
        threading.Thread(target=self.run_coolingprofile_thread, daemon=True).start()
        threading.Thread(target=self.run_valveprofile_thread, daemon=True).start()

        self.status_var.set(f"Running MFC: {mfc_name}, Valve: {valve_name}, Cooling: {cooling_name}")
 
 ###on/offprofile
    def update_onoffprofile_list(self):
        """Refresh the list of available profiles"""
        #https://youtu.be/Vm0ivVxNaA8
        
        #Delete all the items from the listbox
        self.onoffprofile_listbox.delete(0, tk.END)
        
        #Add all the profiles to the listbox
        for profile in self.onoffprofilemanager.get_profiles():
            self.onoffprofile_listbox.insert(tk.END, profile)  #listbox.insert(index, element)

    def load_onoffprofile(self):
        """Load the selected profile into the editor"""
        #https://pythonassets.com/posts/listbox-in-tk-tkinter/
        selection = self.onoffprofile_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a profile to load")
            return
        
        #To ensure that you only select the first selected
        profile_name = self.onoffprofile_listbox.get(selection[0])
        profile = self.onoffprofilemanager.load_profile(profile_name)
        
        self.new_onoffprofile_label.config(text = "")
        
        if profile:
            self.current_loaded_profile = profile_name
            #Update the name of the profile
            self.onoffname_var.set(profile_name)
            #Update the description in the field
            self.onoffdesc_var.set(profile.get("description", ""))
            
            # Clear the existing steps
            for item in self.onoffsteps_tree.get_children():
                self.onoffsteps_tree.delete(item)
            
            # Add new steps
            for step in profile.get("steps", []):
                self.onoffsteps_tree.insert("", tk.END, values=(
                    step["time"],
                    step["flow mfc1"],
                    step["flow mfc2"],
                    step["flow mfc3"],
                    step["temperature"],
                    step["valve"]
                ))
            
            self.status_var.set(f"Loaded profile: {profile_name}")
        
    def delete_onoffprofile(self):
        """Delete the selected profile"""
        #https://pythonassets.com/posts/listbox-in-tk-tkinter/
        selection = self.onoffprofile_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a profile to delete")
            return
            
        profile_name = self.onoffprofile_listbox.get(selection[0]) #To ensure that you only select the first selected
        
        if messagebox.askyesno("Confirm", f"Delete profile '{profile_name}'?"):
            if self.onoffprofilemanager.delete_profile(profile_name):
                #Updating the new profile list
                self.update_onoffprofile_list() 
                #Changing the status
                self.status_var.set(f"Deleted profile: {profile_name}")
            else:
                messagebox.showerror("Error", f"Failed to delete the profile: '{profile_name}'")
                
    def create_new_onoffprofile(self):
		#Clearing all input fields and steps
        self.onoffname_var.set("")
        self.onoffdesc_var.set("")
        self.onoffstep_time_var.set("0")
        self.onoffstep_flow1_var.set("0")
        self.onoffstep_flow2_var.set("0")
        self.onoffstep_flow3_var.set("0")
        self.onoffstep_temp_var.set("0")
        self.onoffstep_valve_var.set("0")
        
        for item in self.onoffsteps_tree.get_children():
            self.onoffsteps_tree.delete(item)
        
        self.new_onoffprofile_label.config(text = "New profile", foreground = "green")
        
    def onoffadd_step(self):
        """Add a new step to the current profile"""
        try:
            time_val = float(self.onoffstep_time_var.get())
            flow1_val = float(self.onoffstep_flow1_var.get())
            flow2_val = float(self.onoffstep_flow2_var.get())
            flow3_val = float(self.onoffstep_flow3_var.get())
            temp_val = float(self.onoffstep_temp_var.get())
            valve_val = int(self.onoffstep_valve_var.get())
            
            if time_val < 0:
                raise ValueError("Time cannot be negative")
            if valve_val not in [1, 2]:
                raise ValueError("Position of the valve must be 1 or 2")
            
            # Check if the time already exists
            for child in self.onoffsteps_tree.get_children():
                if float(self.onoffsteps_tree.item(child, "values")[0]) == time_val:
                    if not messagebox.askyesno("Confirm", f"Step at time {time_val}s already exists. Overwrite?"):
                        return #if True, thus no then return
                    self.onoffsteps_tree.delete(child)
                    break
            
            self.onoffsteps_tree.insert("", tk.END, values=(time_val, flow1_val, flow2_val, flow3_val, temp_val, valve_val))
            
        except ValueError as error:
            messagebox.showerror("Error", f"Invalid input: {error}")
    
    def onoffremove_step(self):
        """Remove the selected step"""
        selection = self.onoffsteps_tree.selection()
        if selection:
            self.onoffsteps_tree.delete(selection)
    
    def onoffclear_steps(self):
        """Clear all steps"""
        if messagebox.askyesno("Confirm", "Clear all the steps?"):
            #Obtain all the steps and delete all the steps
            for item in self.onoffsteps_tree.get_children():
                self.onoffsteps_tree.delete(item)
    
    def save_onoffprofile(self):
        """Save the current profile"""
        #Getting the name
        name = self.onoffname_var.get().strip()
        
        #Ensuring that the name isn't empty
        if not name:
            messagebox.showwarning("Warning", "Profile name cannot be empty")
            return
        
        # Collect steps from the profile
        steps = []
        for child in self.onoffsteps_tree.get_children():
            #To obtain all the values of the steps
            values = self.onoffsteps_tree.item(child, "values")
            steps.append({
                "time": float(values[0]),
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
            "description": self.onoffdesc_var.get(),
            "steps": steps
        }
        
        if self.onoffprofilemanager.save_profile(name, profile_data):
            self.update_onoffprofile_list()
            self.status_var.set(f"Saved profile: {name}")
        else:
            messagebox.showerror("Error", f"Failed to save profile '{name}'")
    
    def run_onoffprofile(self):
        """Run the current profile"""    
            
        if not (self.mfcs[0].connected and self.mfcs[1].connected and self.mfcs[2].connected and self.cooling.connected and self.valve.connected):
            messagebox.showwarning("Error", "One or more devices are not connected")
            return False
          
        #Get the name of the profile without spaces, such that the .json file can be loaded later
        name = self.onoffname_var.get().strip()
        
        #Checking whether the name is empty
        if not name:
            messagebox.showwarning("Warning", "Please load or create a profile first")
            return

        # Load the profile that needs to be runned
        profile = self.onoffprofilemanager.load_profile(name)
        if not profile:
            messagebox.showerror("Error", f"Failed to load profile: '{name}'")
            return
        
        self.update_run_var()
        #Enabling the stop button, since you can now stop a running profile
        self.onoffstop_button.config(state=tk.NORMAL) 
        
        # Start profile in a separate thread, such that the UI doesn't freeze until it finishes
        # And you'll still be able to see what happens, e.g. popup of not connection
        self.onoffprofile_thread = threading.Thread(
            target=self.run_onoffprofile_thread,
            args=(profile,),    
            daemon=True         # Stops threading by pressing an event, e.g. pressing on stop button
        )
        self.onoffprofile_thread.start()
    
    def run_onoffprofile_thread(self, profile):
        """Thread function to run the profile"""
        try:
            # Displaying which profile is running
            self.status_var.set(f"Running profile: {self.onoffname_var.get()}")
            self.onoffprofilemanager.run_profile(temp_ambient= self.ambient_temp,update_callback=self.update_onoffprofile_var)
            # self.notebook.after(0, lambda: self.update_run_status)
            self.notebook.after(0, self.onoffprofile_complete)

        except Exception as e:
            self.notebook.after(0, lambda: self.onoffprofile_error(str(e)))
    
    def onoffprofile_complete(self):
        """Called when profile completes successfully"""
        self.onoffstop_button.config(state=tk.DISABLED)
        self.status_var.set("Profile run completed")
    
    def onoffprofile_error(self, error):
        """Called when profile run encounters an error"""
        self.onoffstop_button.config(state=tk.DISABLED)
        messagebox.showerror("Error", f"Profile run failed: {error}")
        self.status_var.set("Profile run failed")
    
    def stop_onoffprofile(self):
        """Stop the currently running profile"""
        self.onoffstop_button.config(state=tk.DISABLED)
        self.status_var.set("Profile run stopped by user")
    
    def update_onoffprofile_var(self, status):
        self.onoff_elapsed_label.config(text=f"{status['elapsed_time']:.1f}s")
        self.onoff_step_label.config(text=f"{status['current_step']}/{status['total_steps']}")
        self.onoff_value_label.config(text=f"{status['flow mfc1']:.2f}, {status['flow mfc2']:.2f}, {status['flow mfc3']:.2f}, {status['temperature']:.1f}°C, V{status['valve']}")
        self.notebook.after(1000, lambda: self.update_onoffprofile_var(status))  # loop or trigger update
    
def main():
    root = tk.Tk()
    app = AutomatedSystemUI(root)
    root.mainloop()
    
if __name__ == "__main__":
    main()
