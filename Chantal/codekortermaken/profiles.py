import tkinter as tk
from tkinter import messagebox, ttk
import time 
import json
import os
from devices import BronkhorstMFC, Koelingsblok, RVM

class BaseProfileManager:
    def __init__(self, base_dir, profiles_dir, standard_profiles):
        self.profiles_dir = os.path.join(base_dir, profiles_dir)
        self.standard_profiles = standard_profiles
        self.current_profile = None
        self.stoprequest = False

        # Create profiles directory if it doesn't exist
        if not os.path.exists(self.profiles_dir):
            os.makedirs(self.profiles_dir)

        # Save standard profiles if they don't exist
        #https://www.geeksforgeeks.org/python-dictionary-values/
        for name, profile in self.standard_profiles.items():
            #Obtaining the name of the profile and the value of the profile
            file_path = os.path.join(self.profiles_dir, f"{name}.json")
            #We want to overwrite an already existing profile
            if not os.path.exists(file_path):
                self.save_profile(name, profile)

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
        """Save a profile"""
        file_path = os.path.join(self.profiles_dir, f"{name}.json")
        ## https://www.geeksforgeeks.org/reading-and-writing-json-to-a-file-in-python/
        with open(file_path, 'w') as outfile:
            json.dump(profile_data, outfile, indent=4)
        return True
    
    def delete_profile(self, name):
        """Delete a profile"""
        file_path = os.path.join(self.profiles_dir, f"{name}.json")
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False

class MFCProfileManager(BaseProfileManager):
# MFCProfileManager is a Child Class of BaseProfileManager
# https://www.w3schools.com/python/python_inheritance.asp
    def __init__(self, profiles_dir="profiles_onetab"):
        standard_profiles = {
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
        
        # https://www.w3schools.com/python/python_inheritance.asp
        #inherit all the methods and properties from its parent, baseprofilemanager
        super().__init__(profiles_dir, "profiles_mfc", standard_profiles)

        self.mfcs = [BronkhorstMFC("COM1"), BronkhorstMFC("COM2"), BronkhorstMFC("COM3")]
        self.maxflow = 4

    def run_profile(self, update_callback=None):
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

        while not profile_complete and not self.stoprequest:
            elapsed_time = time.time() - start_time
            
            # Check if we need to move to next step
            if current_step_index < len(steps) - 1:
                next_time = steps[current_step_index + 1]["time"]
                if elapsed_time >= next_time:
                    current_step_index += 1

            # Get current step parameters
            current_step = steps[current_step_index]
            
            # Set devices to current step values
            self.mfcs[0].set_massflow(current_step["flow mfc1"])
            self.mfcs[1].set_massflow(current_step["flow mfc2"])
            self.mfcs[2].set_massflow(current_step["flow mfc3"])
            
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

            if current_step_index == len(steps) - 1 and elapsed_time >= current_step["time"]:
                profile_complete = True
                break

            time.sleep(0.5)

        return True

    def stop_profile(self):
        self.stoprequest = True
        
        #Vanuitgaand dat mfcs[2] de een is die dillute
        self.mfcs[0].set_massflow(0)
        self.mfcs[1].set_massflow(0)
        self.mfcs[2].set_massflow(self.maxflow)

class CoolingProfileManager(BaseProfileManager):
    def __init__(self, profiles_dir="profiles_onetab"):
        standard_profiles = {
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
        
        # https://www.w3schools.com/python/python_inheritance.asp
        #inherit all the methods and properties from its parent, baseprofilemanager
        super().__init__(profiles_dir, "profiles_cooling", standard_profiles)
        
        self.cooling = Koelingsblok()

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

            # Check if profile is complete
            if current_step_index == len(steps) - 1 and elapsed_time >= current_step["time"]:
                profile_complete = True
                break
                
            time.sleep(0.5)
        return True
    
    def stop_profile(self):
        self.stoprequest = True
        ###WAT MOETEN WE HIERNA DOEN?

class RVMProfileManager(BaseProfileManager):
    def __init__(self, profiles_dir="profiles_onetab"):
        standard_profiles = {
            "Flow_Test VALVE": {
                "description": "Test valve switching",
                "steps": [
                    {"time": 0.0, "valve": 1},
                    {"time": 10.0, "valve": 1},
                    {"time": 20.0, "valve": 1},
                    {"time": 30.0, "valve": 1},
                    {"time": 40.0, "valve": 1}
                ]
            }
        }
        
        # https://www.w3schools.com/python/python_inheritance.asp
        #inherit all the methods and properties from its parent, baseprofilemanager
        super().__init__(profiles_dir, "profiles_valve", standard_profiles)
        self.valve = RVM()
    
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

            if current_step_index == len(steps) - 1 and elapsed_time >= current_step["time"]:
                profile_complete = True
                break
            time.sleep(0.5)
        return True
    
    def stop_profile(self):
        self.stoprequest = True
        ##home position
        # self.valve.set_valve(1)

class OnoffProfileManager(BaseProfileManager):
    def __init__(self, UImfcs, UIcooling, UIvalve, profiles_dir="profiles_onetab"):
        standard_profiles = {
            "Flow_Test": {
                "description": "Test all devices together",
                "steps": [
                    {"time": 0.0, "flow mfc1": 0.5, "flow mfc2": 0.5, "flow mfc3": 0.5, "temperature": 25.0, "valve": 1},
                    {"time": 10.0, "flow mfc1": 1.0, "flow mfc2": 0.5, "flow mfc3": 0.5, "temperature": 25.0, "valve": 1},
                    {"time": 20.0, "flow mfc1": 1.5, "flow mfc2": 0.5, "flow mfc3": 0.5, "temperature": 25.0, "valve": 1},
                    {"time": 30.0, "flow mfc1": 1.0, "flow mfc2": 0.5, "flow mfc3": 0.5, "temperature": 25.0, "valve": 1},
                    {"time": 40.0, "flow mfc1": 0.5, "flow mfc2": 0.5, "flow mfc3": 0.5, "temperature": 25.0, "valve": 1}
                ]
            }
        }
        super().__init__(profiles_dir, "", standard_profiles)
        self.mfcs = UImfcs
        self.cooling = UIcooling
        self.valve = UIvalve
    
    
    def run_profile(self, temp_ambient, update_callback = None):
        """Run the current profile with the given device controllers"""
        # Ensuring that the MFC, cooling and valve are all connected
        # print(self.mfcs[0].port, self.mfcs[1].port, self.mfcs[2].port)
        # print(self.mfcs[0].connected , self.mfcs[1].connected , self.mfcs[2].connected , self.cooling.connected , self.valve.connected)
        
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
                break
            
            time.sleep(0.5)
        
        return True
    
    def stop_profile(self):
        self.stoprequest = True
