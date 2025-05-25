import json
import os

class SettingsManager:
    def __init__(self, base_dir, filename="settings.json"):
        self.setting = {}
        self.profilepath = base_dir
        self.default_ports = {
            "mfc1": "COM6",
            "mfc2": "COM5",
            "mfc3": "COM3",
            "cooling": "COM7",
            "valve": "COM4"
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
        else:
            self.setting = {
                "com_ports": self.default_ports.copy(),
                "profiles_path": "profiles_onetab"
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