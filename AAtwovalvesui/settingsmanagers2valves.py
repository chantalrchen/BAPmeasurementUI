import json
import os
from tkinter import messagebox

class SettingsManager:
    def __init__(self, base_dir = "profilestab_2VALVES", filename="settings.json"):
        self.setting = {}
        self.profilepath = base_dir
        
        # Python dictionary used to store the data values 
        # https://www.w3schools.com/python/python_dictionaries.asp
        
        self.default_ports = {
            "mfc1": "COM6",
            "mfc2": "COM5",
            "mfc3": "COM3",
            "cooling": "COM7",
            "valve1": "COM4",
            "valve2": "COM5"
        }
        
        self.default_vocdata = {
            '2-Nonanol': [7.87942, 1966.54, 194.918, -35, 349.85],
            'Nonanal': [7.42543, 1825.65, 206.718, -18, 366.85],
            'Tetradecane': [7.2715, 1926.44, 187.657, -12.85, 418.85],
            '1-dodecanethiol': [7.62037, 2309.1, 212.597, -8, 450.85],
            'Ethanol': [8.13484, 1662.48, 238.131, -114.1, 243.1],
            '1 propanol': [8.37895, 1788.02, 227.438, -26, 83], ####Yaws, C. L. Chemical Properties Handbook
            '2 propanol': [8.87829, 2010.33, 252.636, -15, 98], ####Yaws, C. L. Chemical Properties Handbook
            'methanol': [8.09126, 1582.91, 239.096, -97.68, 239.43], #methylalcohol
            'Acetone': [7.31414, 1315.67, 240.479, -94.7, 235.05], 
            'acetic acid': [7.8152, 1800.03, 246.894, 16.66, 319.56], 
            'α-Pinene': [7.06153, 1621.22, 231.645, -64, 358.85], #alpha-pinene
            'water': [8.07131, 1730.63, 233.426, 1, 100], #Yaws, C. L. Chemical Properties Handbook
            'α-Terpinene': [7.13456, 1673.54, 216.227, -53.15, 378.85], #alpha-terpinene
            '1-Butanol': [7.62121, 1543.89, 208.029, -89.3, 289.78],
            'Toluene': [7.1362, 1457.29, 231.827, -94.97, 318.64],
            '2-Butanone (MEK]': [7.29427, 1400.37, 237.655, -86.67, 262.35], #methyl ethyl ketone
            'DMSO': [7.25197, 1733.52, 207.58, 18.52, 452.85] #dimethyl sulfoxide
        }
        self.settings_path = os.path.join(self.profilepath, filename)

        # Ensure that folder exists
        settings_folder = os.path.dirname(self.settings_path)
        if settings_folder and not os.path.exists(settings_folder):
            os.makedirs(settings_folder)
            
        # Load the file
        self.load_settingsfile()

    def load_settingsfile(self):
        if os.path.exists(self.settings_path):
            with open(self.settings_path, 'r') as openfile:
                self.setting = json.load(openfile)
                
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
            self.setting = {
                "com_ports": self.default_ports.copy(),
                "profiles_path": "profiles_onetab",
                "voc_data": self.default_vocdata.copy()
            }
            self.save_settingsfile()  
        return self.setting
    
    def save_settingsfile(self):
        with open(self.settings_path, 'w') as outfile:
            json.dump(self.setting, outfile, indent=6)
            return True

    def get_com_ports(self):
        #If com_ports doesn't exist, then it returns {}
        return self.setting.get("com_ports", {})

    def set_com_ports(self, ports):
        # Store the com values under "com_ports"
        self.setting["com_ports"] = ports
        self.save_settingsfile()
    
    def update_com_port(self, device_name, port):
        if "com_ports" not in self.setting:
            self.setting["com_ports"] = {}
        self.setting["com_ports"][device_name] = port
        self.save_settingsfile()

    def get_profiles_path(self):
        return self.setting.get("profiles_path", self.profilepath)

    def set_profiles_path(self, new_path):
        self.setting["profiles_path"] = new_path
        self.profilepath = new_path
        self.save_settingsfile()

    def get_voc_data(self):
        # https://www.geeksforgeeks.org/python-sort-python-dictionaries-by-key-or-value/
        data = self.setting.get("voc_data", {})
        return dict(sorted(data.items(), key=lambda item: item[0].lower()))

    def add_voc(self, name, antoine_abc_tmintmax):
        try:
            if not isinstance(antoine_abc_tmintmax, (list, tuple)) or len(antoine_abc_tmintmax) != 5:
                raise ValueError("VOC data must have 5 values: A, B, C, Tmin, Tmax")

            if not all(isinstance(value, float) for value in antoine_abc_tmintmax):
                raise ValueError("A, B, C, Tmin, Tmax must be of type float")
            
            vocs = self.get_voc_data()
            vocs[name] = list(antoine_abc_tmintmax)
            self.setting["voc_data"] = vocs
            self.save_settingsfile()
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not add VOC: {e}")
            

    def delete_voc(self, name):
        try:
            vocs = self.get_voc_data()
            if name in vocs:
                del vocs[name]  
                self.setting["voc_data"] = vocs
                self.save_settingsfile()
            else:
                raise ValueError(f"VOC '{name}' not found.")
        except Exception as e:
            messagebox.showerror("Error", f"Could not delete VOC: {e}")