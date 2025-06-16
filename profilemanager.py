import tkinter as tk
from tkinter import messagebox
import time 
import json
import os

# This code has been written by C.R. Chen and F.Lin for the BAP project E-nose.

# When the "real"-devices are used
# from devices import BronkhorstMFC, RVM

# To simulate the devices
from simulate_devices import BronkhorstMFC, RVM

class BaseProfileManager:
    """Profile Manager which can load, save and delete the profiles
    """
    def __init__(self, base_dir, profiles_dir, standard_profiles):
        """Initialize the base profile manager with the directory path and default profiles

        Args:
            base_dir (str): Base directory where the profiles should be stored
            profiles_dir (str): Sub directory where the profile type should be stored
            standard_profiles (dict): Dictionary with predefined profiles
        """
        # Directory path of where the profiles are saved
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
        """Return a list of the available profile names

        Returns:
            list: list of profile names in alphabetical order
        """
        profiles = []
        #List all the files in directory
        for filename in os.listdir(self.profiles_dir):
            # Remove .json extension
            if filename.endswith('.json'):
                profiles.append(filename[:-5])  
        return sorted(profiles) #List of profile names in alphabetical order

    def load_profile(self, name):
        """Load a profile by name and set it as current profile

        Args:
            name (str): name of the profile

        Returns:
            dict: the content of the profile as dictionary, if file does not exist, return None
        """
        file_path = os.path.join(self.profiles_dir, f"{name}.json")
        if os.path.exists(file_path):
            ## https://www.geeksforgeeks.org/reading-and-writing-json-to-a-file-in-python/
            # Load the file
            with open(file_path, 'r') as openfile:
                self.current_profile = json.load(openfile)
                return self.current_profile
        return None

    def save_profile(self, name, profile_data):
        """Saves the profile

        Args:
            name (str): name of the profile
            profile_data (dict): dictionary of the profile

        Returns:
            boolean: If saving profile succeed, return true
        """
        file_path = os.path.join(self.profiles_dir, f"{name}.json")
        ## https://www.geeksforgeeks.org/reading-and-writing-json-to-a-file-in-python/
        # Writing the profile to a json file
        with open(file_path, 'w') as outfile:
            json.dump(profile_data, outfile, indent=6)
        return True
    
    def delete_profile(self, name):
        """Deleting the profile 

        Args:
            name (str): name of the profile

        Returns:
            boolean: If file is successfully deleted return True, else False
        """
        
        #Path to the json file
        file_path = os.path.join(self.profiles_dir, f"{name}.json")
        
        # If the file exists in the path delete the file
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False

class MFCProfileManager(BaseProfileManager):
    """Class to control the profiles of the three MFCs
    
    The class is a child class of the baseprofilemanager.
    # https://www.w3schools.com/python/python_inheritance.asp
    
    This class can also:
    - include standard profiles
    - initialize the MFCs via Ports
    - Execute profiles based on times and the set flwo rates
    """

    def __init__(self, mfc1port, mfc2port, mfc3port, profiles_dir):
        """Initialize the MFCprofilemanager with COM ports and standard profiles

        Args:
            mfc1port (str): Serial port for MFC1
            mfc2port (str): Serial port for MFC2
            mfc3port (str): Serial port for MFC3
            profiles_dir (str): Directory to store and load the MFC profiles
        """
        # For standard profiles
        standard_profiles = {
            "Flow_Test MFC": {
                "description": "Test flow rate changes",
                "steps": [
                    {"time": 0.0, "flow mfc1": 0.5, "flow mfc2": 1.0, "flow mfc3": 0.5},
                    {"time": 10.0, "flow mfc1": 1.0, "flow mfc2": 0.5, "flow mfc3": 0.5},
                    {"time": 20.0, "flow mfc1": 1.5, "flow mfc2": 0.0, "flow mfc3": 0.5},
                    {"time": 30.0, "flow mfc1": 1.0, "flow mfc2": 0.5, "flow mfc3": 0.5},
                    {"time": 40.0, "flow mfc1": 0.5, "flow mfc2": 0.5, "flow mfc3": 1.0}
                ]
            }
        }
        
        # https://www.w3schools.com/python/python_inheritance.asp
        # inherit all the methods and properties from its parent, baseprofilemanager
        super().__init__(profiles_dir, "profiles_MFC", standard_profiles)
        
        # Initialize the 3 MFCs with the according COM ports
        self.mfcs = [BronkhorstMFC(port = mfc1port), BronkhorstMFC(port = mfc2port), BronkhorstMFC(port = mfc3port)] #,  BronkhorstMFC(port = 'COM3', channel = 2), BronkhorstMFC(port = 'COM3', channel = 3)]

    def run_profile(self, update_callback=None):
        """Running the profile of the mass flow controller. Each step in the profile has a desired flow rate for each MFC. The execution of the profile is based on the time.
        Updates to the UI can be given through the callback function.

        Args:
            update_callback (function, optional): Function that receives a dictionary with the current execution status (elapsed time, current step, set flow values). Defaults to None.

        Returns:
            boolean: If MFCs are not connected, no profile is loaded or invalid profile returns False, else if profiles is completed or stopped return True
        """
        
        # Check whether all three MFCs are connected
        if not (self.mfcs[0].connected and self.mfcs[1].connected and self.mfcs[2].connected):
            messagebox.showerror("Connection Error", "MFCs not connected")
            return False

        # Checks whether there is a profile loaded
        if not self.current_profile:
            messagebox.showerror("Error", "No profile loaded")
            return False

        # Obtain the steps
        steps = self.current_profile.get("steps", [])
        # Check whether the profile has steps
        if not steps:
            messagebox.showerror("Error", "Profile has no steps")
            return False
        # Sort steps by time
        steps = sorted(steps, key=lambda x: x["time"])

        # Initialize the stop request
        self.stoprequest = False
        # Get the current time
        start_time = time.time()
        # Initialize the step index        
        current_step_index = 0
        # Initialize the flag whether the profile is completed
        profile_complete = False
        
        # Executing the profile based on time
        # Check whether the profile has completed with running or the user want to stop running the profile
        while not profile_complete and not self.stoprequest:
            # Get the current time
            now = time.time()
            # Calculate how long the profile already has been "running"
            elapsed_time = now - start_time

            # Check if we need to move to next step
            if current_step_index < len(steps) - 1:
                next_time = steps[current_step_index + 1]["time"]
                # Update the current step index when time obtained
                if elapsed_time >= next_time:
                    current_step_index += 1

            # Get the current step data
            current_step = steps[current_step_index]

            # Set the massflow rates to the corresponding mfcs
            self.mfcs[0].set_massflow(current_step["flow mfc1"])
            self.mfcs[1].set_massflow(current_step["flow mfc2"])
            self.mfcs[2].set_massflow(current_step["flow mfc3"])

            # Update callback for UI (if callback is provided)
            if update_callback:
                update_callback({
                    "elapsed_time": elapsed_time,
                    "current_step": current_step_index + 1,
                    "total_steps": len(steps),
                    "flow mfc1": current_step["flow mfc1"],
                    "flow mfc2": current_step["flow mfc2"],
                    "flow mfc3": current_step["flow mfc3"],
                })

            # Check whether we have reached last step, if last step we need to consider wait_time
            if current_step_index < len(steps) - 1:
                next_time = steps[current_step_index + 1]["time"]
                # Calculate how much time we need to wait before the next step should start
                wait_time = max(0, next_time - (time.time() - start_time))
                # Sleep in small steps until finally wait_time has reached, thus until the next time has reached, kinda stukje bij stukje wachten
                # Minimum 0.1 s to ensure that UI still is reponsive
                time.sleep(min(wait_time, 0.1))  
            else:
                # Last step, and wait in steps until the final duration has reached
                final_duration = current_step["time"]
                if elapsed_time >= final_duration:
                    profile_complete = True
                else:
                    # Sleep in small steps until final time has reached
                    time.sleep(0.1)

    def stop_profile(self):
        """Sets a request to stop the profile during executing of the profiles
        """
        self.stoprequest = True

class RVMProfileManager(BaseProfileManager):
    """Class to control the profiles of the RVM
    
    The class is a child class of the baseprofilemanager.
    # https://www.w3schools.com/python/python_inheritance.asp
    
    This class can also:
    - include standard profiles
    - initialize the RVMs via Ports
    - Execute profiles based on times and the set the valve position
    """
    
    def __init__(self, valveport1, valveport2, profiles_dir):
        """Initialize the RVMprofilemanager with COM ports for the two RVM valves

        Args:
            valveport1 (str): Serial port for valve 1
            valveport2 (str): Serial port for valve 2
            profiles_dir (str): Directory path to store and load the valve profiles
        """
        # For standard profiles
        standard_profiles = {
            "Flow_Test VALVE": {
                "description": "Test valve switching",
                "steps": [
                    {"time": 0.0, "valve1": 1, "valve2": 2},
                    {"time": 10.0, "valve1": 2, "valve2": 1},
                    {"time": 20.0, "valve1": 1, "valve2": 2},
                    {"time": 30.0, "valve1": 2, "valve2": 1},
                    {"time": 40.0, "valve1": 1, "valve2": 2}
                ]
            }
        }
        
        # https://www.w3schools.com/python/python_inheritance.asp
        #inherit all the methods and properties from its parent, baseprofilemanager
        super().__init__(profiles_dir, "profiles_RVM", standard_profiles)
        
        # Initialize the 2 RVM valves with the corresponding COM ports
        self.valve =[RVM(valveport1), RVM(valveport2)]
        
    
    def run_profile(self, update_callback = None):
        """Running the profile of the RVM. Each step in the profile has a desired position for each RVM. The execution of the profile is based on the time.
        Updates to the UI can be given through the callback function.

        Args:
            update_callback (function, optional): Function that receives a dictionary with the current execution status (elapsed time, current step, set position). Defaults to None.

        Returns:
            boolean: If RVMs are not connected, no profile is loaded or invalid profile returns False, else if profiles is completed or stopped return True
        """
        
        # Check whether both valves are connected
        if not (self.valve[0].connected and self.valve[1].connected):
            messagebox.showerror("Connection Error", "Valve is not connected")
            return False
        
        # Check whether there is a profile loaded
        if not self.current_profile:
            messagebox.showerror("Error", "No profile loaded")
            return False
        
        # Obtain the steps
        steps = self.current_profile.get("steps", [])
        # Check whether the profile has steps
        if not steps:
            messagebox.showerror("Error", "Profile has no steps")
            return False
        # Sort steps by time
        steps = sorted(steps, key=lambda x: x["time"])

        # Initialize the stop request
        self.stoprequest = False
        # Get the current time
        start_time = time.time()
        # Initialize the step index
        current_step_index = 0
        # Initialize the flag whether the profile is completed
        profile_complete = False

        # Executing the profile based on time
        # Check whether the profile has completed with running or the user want to stop running the profile
        while not profile_complete and not self.stoprequest:
            # Get the current time
            now = time.time()
            # Calculate how long the profile already has been "running"
            elapsed_time = now - start_time

            # Check if we need to move to next step
            if current_step_index < len(steps) - 1:
                next_time = steps[current_step_index + 1]["time"]
                # Update the current step index when time obtained
                if elapsed_time >= next_time:
                    current_step_index += 1

            # Get the current step data
            current_step = steps[current_step_index]
            
            # Set the valve position according to the current step
            self.valve[0].switch_position(current_step["valve1"])
            self.valve[1].switch_position(current_step["valve2"])
        
            #if update_callback is called then we need to update the status with the corresponding data
            if update_callback:
                    update_callback({
                    "elapsed_time": elapsed_time,
                    "current_step": current_step_index + 1,
                    "total_steps": len(steps),
                    "valve1": current_step["valve1"],
                    "valve2": current_step["valve2"],
                })

            # Check whether we have reached last step, if last step we need to consider wait_time
            if current_step_index < len(steps) - 1:
                next_time = steps[current_step_index + 1]["time"]
                # Calculate how much time we need to wait before the next step should start
                wait_time = max(0, next_time - (time.time() - start_time))
                # sleep in small steps until finally wait_time has reached, thus until the next time has reached, kinda stukje bij stukje wachten
                # Minimum 0.1 s to ensure that UI still is reponsive
                time.sleep(min(wait_time, 0.1))  
            else:
                # Last step, and wait in steps until the final duration has reached
                final_duration = current_step["time"]
                if elapsed_time >= final_duration:
                    profile_complete = True
                else:
                    # Sleep in small steps until final time has reached
                    time.sleep(0.1)
        return True
    
    def stop_profile(self):
        """Sets a request to stop the profile during executing of the profiles
        """
        self.stoprequest = True

class MFCandRVMProfileManager(BaseProfileManager):
    """Class to control the MFCs and the Valves based on the time
    
    The class is a child class of the baseprofilemanager.
    # https://www.w3schools.com/python/python_inheritance.asp
    
    This class can also:
    - include standard profiles for both the flow rate and valve switching
    - initialize the MFCs and Valve
    - Execute profiles based on times set the flow rate and valves position
    """
    def __init__(self, UImfcs, UIvalve, profiles_dir):
        """Initialize the profile manager for both the MFCs and the RVMs

        Args:
            UImfcs (list): List of MFCs devices
            UIvalve (list): List of RVM devices
            profiles_dir (str): Directory path to store and load the profiles
        """
        # For standard profiles
        standard_profiles = {
            "Flow_Test": {
                "description": "Test all devices together",
                "steps": [
                    {"time": 0.0, "flow mfc1": 0.5, "flow mfc2": 1.0, "flow mfc3": 0.5, "valve1": 1, "valve2": 1},
                    {"time": 10.0, "flow mfc1": 1.0, "flow mfc2": 0.5, "flow mfc3": 0.5, "valve1": 2, "valve2": 1},
                    {"time": 20.0, "flow mfc1": 1.5, "flow mfc2": 0.5, "flow mfc3": 0.0, "valve1": 2, "valve2": 2},
                    {"time": 30.0, "flow mfc1": 1.0, "flow mfc2": 0.5, "flow mfc3": 0.5, "valve1": 2, "valve2": 1},
                    {"time": 40.0, "flow mfc1": 0.5, "flow mfc2": 1.0, "flow mfc3": 0.5, "valve1": 1, "valve2": 2},
                ]
            }
        }

        # https://www.w3schools.com/python/python_inheritance.asp
        # inherit all the methods and properties from its parent, baseprofilemanager
        super().__init__(profiles_dir, "profiles_MFCandRVM", standard_profiles)
        self.mfcs = UImfcs
        self.valve = UIvalve
    
    def run_profile(self, update_callback = None): 
        """Running the combined profile for the MFCs and RVMs. Each step in the profile has a desired flow rate for each MFC and desired position for each RVMs. The execution of the profile is based on the time.
        Updates to the UI can be given through the callback function.

        Args:
            update_callback (function, optional): Function that receives a dictionary with the current execution status (elapsed time, current step, set flow values, set position). Defaults to None.

        Returns:
            boolean: If MFCs or RVMs are not connected, no profile is loaded or invalid profile returns False, else if profiles is completed or stopped return True
        """
        # Ensuring that the MFCs connected
        if not (self.mfcs[0].connected and self.mfcs[1].connected and self.mfcs[2].connected):
            messagebox.showerror("Connection Error", "One or more MFCs not connected.")
            return

        # Ensuring that the RVMs are connected
        if not (self.valve[0].connected and self.valve[1].connected):
            messagebox.showerror("Connection Error", "Valve not connected.")
            return
        
        # Check if a profile is loaded
        if not self.current_profile:
            messagebox.showerror("Error", "No profile loaded")
            return False
        
        # Obtain the steps
        steps = self.current_profile.get("steps", [])
        # Check whether the profile has steps
        if not steps:
            messagebox.showerror("Error", "Profile has no steps")
            return False
        # Sort steps by time
        steps = sorted(steps, key=lambda x: x["time"])
        
        # Initialize the stop request
        self.stoprequest = False
        # Get the current time
        start_time = time.time()
        # Initialzie the step index
        current_step_index = 0
        # Initialize the flag whether the profile is completed
        profile_complete = False

        # Executing the profile based on time
        # Check whether the profile has completed with running or the user want to stop running the profile
        while not profile_complete and not self.stoprequest:
            # Get the current time
            now = time.time()
            # Calculate how long the profile already has been "running"
            elapsed_time = now - start_time

            # Check if we need to move to next step
            if current_step_index < len(steps) - 1:
                next_time = steps[current_step_index + 1]["time"]
                # Update the current step index when time obtained
                if elapsed_time >= next_time:
                    current_step_index += 1

            # Get the current step data
            current_step = steps[current_step_index]

            # Set the massflow rates to the corresponding mfcs
            self.mfcs[0].set_massflow(current_step["flow mfc1"])
            self.mfcs[1].set_massflow(current_step["flow mfc2"])
            self.mfcs[2].set_massflow(current_step["flow mfc3"])

            # Set the position to the corresponding RVMs
            self.valve[0].switch_position(current_step["valve1"])
            self.valve[1].switch_position(current_step["valve2"])
            
            # #if update_callback is called then we need to update the status with the corresponding data
            if update_callback:
                    update_callback({
                    "elapsed_time": elapsed_time,
                    "current_step": current_step_index + 1,
                    "total_steps": len(steps),
                    "flow mfc1": current_step["flow mfc1"],
                    "flow mfc2": current_step["flow mfc2"],
                    "flow mfc3": current_step["flow mfc3"],
                    "valve1": current_step["valve1"],
                    "valve2": current_step["valve2"]
                })

            # Check whether we have reached last step, if last step we need to consider wait_time
            if current_step_index < len(steps) - 1:
                next_time = steps[current_step_index + 1]["time"]
                # Calculate how much time we need to wait before the next step should start
                wait_time = max(0, next_time - (time.time() - start_time))
                # sleep in small steps until finally wait_time has reached, thus until the next time has reached, kinda stukje bij stukje wachten
                # Minimum 0.1 s to ensure that UI still is reponsive
                time.sleep(min(wait_time, 0.1))  
            else:
                # Last step, and wait in steps until the final duration has reached
                final_duration = current_step["time"]
                if elapsed_time >= final_duration:
                    profile_complete = True
                else:
                    # Sleep in small steps until final time has reached
                    time.sleep(0.1)
        return True
    
    def stop_profile(self):
        """Sets a request to stop the profile during executing of the profiles
        """
        self.stoprequest = True

class OnOffConcProfileManager(BaseProfileManager):
    """Class to control the On/Off profile that can calculate the corresponding flow rates based on the concentration
    
    The class is a child class of the baseprofilemanager.
    # https://www.w3schools.com/python/python_inheritance.asp
    
    This class can also:
    - include standard profiles
    - initialize the MFCs via Ports
    - Execute profiles based on times and the set flow rates based on the concentration, and set the valves based on ON/OFF situation
    """
    def __init__(self, UImfcs, UIvalve, profiles_dir):
        """Initialize the OnOffConcProfileManager

        Args:
            UImfcs (list): List of MFCs devices
            UIvalve (list): List of RVM devices
            profiles_dir (str): Directory path to store and load the profiles
        """
        # For standard profiles
        standard_profiles = {}
        # https://www.w3schools.com/python/python_inheritance.asp
        # inherit all the methods and properties from its parent, baseprofilemanager
        super().__init__(profiles_dir,  "profiles_puregas_onoff_conc", standard_profiles)

class DiffConcProfileManager(BaseProfileManager):
    """Class to control the profile that can calculate the corresponding flow rates based on the concentration
    
    The class is a child class of the baseprofilemanager.
    # https://www.w3schools.com/python/python_inheritance.asp
    
    This class can also:
    - include standard profiles
    - initialize the MFCs via Ports
    - Execute profiles based on times and the set flow rates based on the concentration, and set the valves based on ON/OFF situation
    
    The class do not enable the user to mix VOC1 with VOC2
    """
    def __init__(self, UImfcs, UIvalve, profiles_dir):
        """Initialize the DiffConcProfileManager with the MFCs and RVms

        Args:
            UImfcs (list): List of MFCs devices
            UIvalve (list): List of RVM devices
            profiles_dir (str): Directory path to store and load the profiles
        """
        # For standard profiles
        standard_profiles = {}

        # https://www.w3schools.com/python/python_inheritance.asp
        # inherit all the methods and properties from its parent, baseprofilemanager
        super().__init__(profiles_dir, "profiles_puregas_diffconc", standard_profiles)
        
        #Initialize the MFCs and the RVMs
        self.mfcs = UImfcs
        self.valve = UIvalve
    
    def run_profile(self, update_callback = None):
        """Run the profile with the connected devices. Each step in the profiles has a desired concentration and required gas in the gas inlet. The execution of the profile is based on the time.
        Updates to the UI can be given through the callback function.

        Args:
            update_callback (function, optional): Function that receives a dictionary with the current execution status (elapsed time, current step, set flow values). Defaults to None.

        Returns:
            boolean: If MFCs or RVMs are not connected, no profile is loaded or invalid profile returns False, else if profiles is completed or stopped return True
        """

        # Check whether all three MFCs are connected
        if not (self.mfcs[0].connected and self.mfcs[1].connected and self.mfcs[2].connected):
            messagebox.showerror("Connection Error", "One or more MFCs not connected.")
            return
        
        # Check whether the two RVMs are connected
        if not (self.valve[0].connected and self.valve[1].connected):
            messagebox.showerror("Connection Error", "Valve not connected.")
            return

        # Checks whether there is a profile loaded
        if not self.current_profile:
            messagebox.showerror("Error", "No profile loaded")
            return False
        
        # Obtain the steps
        steps = self.current_profile.get("steps", [])
        # Check whether the profile has steps
        if not steps:
            messagebox.showerror("Error", "Profile has no steps")
            return False
        # Sort steps by time
        steps = sorted(steps, key=lambda x: x["time"])
        
        # Initialize the stop request
        self.stoprequest = False
        # Get the current time       
        start_time = time.time()
        # Initialize the step index        
        current_step_index = 0
        # Initialize the flag whether the profile is completed
        profile_complete = False

        # Executing the profile based on time
        # Check whether the profile has completed with running or the user want to stop running the profile
        while not profile_complete and not self.stoprequest:
            # Get the current time
            now = time.time()
            # Calculate how long the profile already has been "running"
            elapsed_time = now - start_time

            # Check if we need to move to next step
            if current_step_index < len(steps) - 1:
                next_time = steps[current_step_index + 1]["time"]
                # Update the current step index when time obtained
                if elapsed_time >= next_time:
                    current_step_index += 1

            # Get the current step data
            current_step = steps[current_step_index]
            
            # Determine which is the MFC of the VOC (index 1 or 2)
            self.vocmfcindex = self.current_profile.get("mfcchoice", "")
            if self.vocmfcindex == "VOC1 (MFC2)":
                self.vocmfcindex = 1
            elif self.vocmfcindex == "VOC2 (MFC3)":
                self.vocmfcindex = 2
            else:
                messagebox.showerror("Error", f"Invalid MFC choice: {self.vocmfcindex}")
                return False
            
            # Assign the selected MFC for the VOC flow
            self.vocmfc = self.mfcs[self.vocmfcindex] 
        
            # Determine the gas inlet for valve switching, this is either the VOC or N2 that goes in the chamber gas inlet.
            gas_inlet = current_step["gas_inlet"]
            
            # Set the flow for N2 (always on MFC1)
            self.mfcs[0].set_massflow(current_step["flow mfc1"]) 
            # Set the flow rate for VOC (MFC2 or MFC3 based on the selected MFC)
            self.vocmfc.set_massflow(current_step["flow mfc2"]) 
            
            # Set the valve position based on the gas inlet 
            if gas_inlet == "VOC" :  
                # vocmfc = 1 means VOC1 in MFC2, so in order to get the VOC in the chamber, we should switch valve to position 2, 2
                if self.vocmfcindex == 1:
                    self.valve[0].switch_position(2)
                    self.valve[1].switch_position(2)
                # vocmfc 2 means VOC2 in MFC3, so in order to get the VOC in the chamber, we should switch valve to position 1, 1
                elif self.vocmfcindex == 2:
                    self.valve[0].switch_position(1)
                    self.valve[1].switch_position(1)
                # When the user want nitrogen in the gas inlet, the valve should switch to position 1, 2 
            elif gas_inlet == "N2":  
                self.valve[0].switch_position(1)
                self.valve[1].switch_position(2)

            # #if update_callback is called then we need to update the status with the corresponding data
            if update_callback:
                    update_callback({
                    "elapsed_time": elapsed_time,
                    "current_step": current_step_index + 1,
                    "total_steps": len(steps),
                    "concentration": current_step["concentration"],
                    "gas_inlet": current_step["gas_inlet"],
                    "flow mfc1": current_step["flow mfc1"],
                    "flow mfc2": current_step["flow mfc2"]
                })

            # Check whether we have reached last step, if last step we need to consider wait_time
            if current_step_index < len(steps) - 1:
                next_time = steps[current_step_index + 1]["time"]
                # Calculate how much time we need to wait before the next step should start
                wait_time = max(0, next_time - (time.time() - start_time))
                # sleep in small steps until finally wait_time has reached, thus until the next time has reached, kinda stukje bij stukje wachten
                # Minimum 0.1 s to ensure that UI still is reponsive
                time.sleep(min(wait_time, 0.1))  
            else:
                # Last step, and wait in steps until the final duration has reached
                final_duration = current_step["time"]
                if elapsed_time >= final_duration:
                    profile_complete = True
                else:
                    # Sleep in small steps until final time has reached
                    time.sleep(0.1)
        
        return True
    
    def stop_profile(self):
        """Sets a request to stop the profile during executing of the profiles
        """
        self.stoprequest = True
