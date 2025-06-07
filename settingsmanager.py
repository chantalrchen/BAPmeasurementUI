import json
import os
from tkinter import messagebox

class SettingsManager:
    """
    Class to manage configuration settings related to COM ports, VOC data, and profile paths.
    Reads from and writes to a JSON configuration file.
    """
    def __init__(self, base_dir = "SettingsManager", filename="settings.json"):
        ## Initialize settings manager with default paths and data ##
        self.setting = {}
        self.profilepath = base_dir
        
        # Python dictionary used to store the data values 
        # https://www.w3schools.com/python/python_dictionaries.asp
        # Default COM ports for various devices
        self.default_ports = {
            "mfc1": "COM6",
            "mfc2": "COM5",
            "mfc3": "COM3",
            "cooling": "COM7",
            "valve1": "COM4",
            "valve2": "COM5"
        }

        # Default VOC data: [Antoine A, B, C, Tmin, Tmax] 
        # Since the concentration will only be calculated for T = 0, acetic acid, water and DMSO is commented out, since these Antoine coefficients do not hold for T = 0, their Tmin > 0 degrees Celcius
        self.default_vocdata = {
            '2-Nonanol': [7.87942, 1966.54, 194.918, -35, 349.85],              #Obtained from Iranian Chemical Engineers Website
            'Nonanal': [7.42543, 1825.65, 206.718, -18, 366.85],                #Obtained from Iranian Chemical Engineers Website
            'Tetradecane': [7.2715, 1926.44, 187.657, -12.85, 418.85],          #Obtained from Iranian Chemical Engineers Website
            '1-dodecanethiol': [7.62037, 2309.1, 212.597, -8, 450.85],          #Obtained from Iranian Chemical Engineers Website
            'Ethanol': [8.13484, 1662.48, 238.131, -114.1, 243.1],              #Obtained from Iranian Chemical Engineers Website
            '1 propanol': [8.37895, 1788.02, 227.438, -26, 83],                 #Obtained from Yaws, C. L. Chemical Properties Handbook
            '2 propanol': [8.87829, 2010.33, 252.636, -15, 98],                 #Obtained from Yaws, C. L. Chemical Properties Handbook
            'methanol': [8.09126, 1582.91, 239.096, -97.68, 239.43],            #methylalcohol, obtained from Iranian Chemical Engineers Website
            'Acetone': [7.31414, 1315.67, 240.479, -94.7, 235.05],              #Obtained from Iranian Chemical Engineers Website
            # 'acetic acid': [7.8152, 1800.03, 246.894, 16.66, 319.56],           #Obtained from Iranian Chemical Engineers Website
            'α-Pinene': [7.06153, 1621.22, 231.645, -64, 358.85],               #alpha-pinene, obtained from Iranian Chemical Engineers Website
            # 'water': [8.07131, 1730.63, 233.426, 1, 100],                       #Yaws, C. L. Chemical Properties Handbook
            'α-Terpinene': [7.13456, 1673.54, 216.227, -53.15, 378.85],         #alpha-terpinene, obtained from Iranian Chemical Engineers Website
            '1-Butanol': [7.62121, 1543.89, 208.029, -89.3, 289.78],            #Obtained from Iranian Chemical Engineers Website
            'Toluene': [7.1362, 1457.29, 231.827, -94.97, 318.64],              #Obtained from Iranian Chemical Engineers Website
            '2-Butanone (MEK]': [7.29427, 1400.37, 237.655, -86.67, 262.35],    #methyl ethyl ketone, obtained from Iranian Chemical Engineers Website
            # 'DMSO': [7.25197, 1733.52, 207.58, 18.52, 452.85]                   #dimethyl sulfoxide, obtained from Iranian Chemical Engineers Website
        }
        self.settings_path = os.path.join(self.profilepath, filename)

        # Ensure that folder exists
        settings_folder = os.path.dirname(self.settings_path)
        if settings_folder and not os.path.exists(settings_folder):
            os.makedirs(settings_folder)
            
        # Load the file
        self.load_settingsfile()

    def load_settingsfile(self):
        """Load the JSON settings file or create default settings this is not not found

        Returns:
            dict: loaded or created settings dictionary
        """
        if os.path.exists(self.settings_path):
            # Read the settings file 
            with open(self.settings_path, 'r') as openfile:
                self.setting = json.load(openfile)
            
            # Ensure that com_ports, profile_paths and voc_data is present, if not present initialize with defaults
            if "com_ports" not in self.setting:
                self.setting["com_ports"] = self.default_ports.copy()
                self.save_settingsfile()                
            if "profiles_path" not in self.setting:
                self.setting["profiles_path"] = "profiles_onetab"
                self.save_settingsfile()
            if "voc_data" not in self.setting:
                self.setting["voc_data"] = self.default_vocdata.copy()
                self.save_settingsfile()
                
        else:
            # If the settings file does not exist, initialize with defaults
            self.setting = {
                "com_ports": self.default_ports.copy(),
                "profiles_path": "profiles_onetab",
                "voc_data": self.default_vocdata.copy()
            }
            self.save_settingsfile()  
        return self.setting
    
    def save_settingsfile(self):
        """Save the current settings dictionary to the settings file

        Returns:
            bool: True when saving went correctly
        """
        # Open settingsfile
        with open(self.settings_path, 'w') as outfile:
            # Dump the json file to a readable format
            json.dump(self.setting, outfile, indent=4)
            return True

    def get_com_ports(self):
        """Get the COM ports for each device from the settings file

        Returns:
            dict: returning the dictionary with the com ports for each device, returns empty dictionary if it does not exist
        """
        #If com_ports doesn't exist, then it returns {}
        return self.setting.get("com_ports", {})

    def set_com_ports(self, ports):
        """Overwrite the COM ports in the settings file
        
        Args:
            ports (dict): Dictionary with the COM port mapping
        """
        # Store the com values under "com_ports"
        self.setting["com_ports"] = ports
        # Save the updated settingsfile
        self.save_settingsfile()
    
    def update_com_port(self, device_name, port):
        """Updating the COM ports for specific device

        Args:
            device_name (str): the label of the device, such as mfc1
            port (str): COM port assigned to the device
        """
        
        # Ensure that COM_port exists in settings file
        if "com_ports" not in self.setting:
            self.setting["com_ports"] = {}
            
        # Update the COM port for the given device
        self.setting["com_ports"][device_name] = port
        
        # Save the updated settings to file
        self.save_settingsfile()

    def get_profiles_path(self):
        """Get the path where the profiles are stored.

        Returns:
            str: path where the profiles are stored
        """
        return self.setting.get("profiles_path", self.profilepath)

    def set_profiles_path(self, new_path):
        self.setting["profiles_path"] = new_path
        self.profilepath = new_path
        self.save_settingsfile()

    def get_voc_data(self):
        """ Retrieve the VOC data from the settings

        Returns:
            dict: VOC data dictionary with the VOC name and the A, B, C, Tmin, Tmax values.
        """
        # https://www.geeksforgeeks.org/python-sort-python-dictionaries-by-key-or-value/
        
        # Get the data from the dictionary, if it does not exist, then an empty directionary will be 'returned'
        data = self.setting.get("voc_data", {})
        
        # Ensure that the VOCs are sorted alphabetically by name, and also case-insensitive.
        return dict(sorted(data.items(), key=lambda item: item[0].lower()))

    def add_voc(self, name, antoine_abc_tmintmax):
        """Add a new VOC entry to the settings with its Antoine coefficients (A,B,C) and the temperature range for which these Antoine coefficients holds

        Args:
            name (str): Name of the VOC
            antoine_abc_tmintmax (tuple): [A, B, C, Tmin, Tmax]

        Raises:
            ValueError: If the input is not a tuple of 5 values or is not a float.
            ValueError: _description_
        """
        try:
            # Check whether the input tuple contains 5 values
            if not isinstance(antoine_abc_tmintmax, (list, tuple)) or len(antoine_abc_tmintmax) != 5:
                raise ValueError("VOC data must have 5 values: A, B, C, Tmin, Tmax")

            # Ensure that all elements are floats
            if not all(isinstance(value, float) for value in antoine_abc_tmintmax):
                raise ValueError("A, B, C, Tmin, Tmax must be of type float")
            
            # Add or update the VOC
            vocs = self.get_voc_data()
            vocs[name] = list(antoine_abc_tmintmax)
            self.setting["voc_data"] = vocs
            self.save_settingsfile()
            
        except Exception as e:
            # Messsagebox if saving fails
            messagebox.showerror("Error", f"Could not add VOC: {e}")
            
    def delete_voc(self, name):
        """Delete VOC entry from the settings

        Args:
            name (str): Name of the VOC that needs to be deleted

        Raises:
            ValueError: If errors occurs while trying to delete the VOC or VOC name can't be found in the settings
        """
        try:
            # Get the existing VOCs
            vocs = self.get_voc_data()
            
            # Delete the VOC if the name exists
            if name in vocs:
                del vocs[name]  
                self.setting["voc_data"] = vocs
                self.save_settingsfile()
            else:
                # Messagebox if name of VOC can't be found
                raise ValueError(f"VOC '{name}' not found.")
            
        except Exception as e:
            # Messagebox if deletion fails
            messagebox.showerror("Error", f"Could not delete VOC: {e}")