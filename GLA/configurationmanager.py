import json
import os

class ConfigManager:
    def __init__(self, base_dir="profiles_onetab", filename="config.json"):
        self.config_path = os.path.join(base_dir, filename)
        self.config = {}
        
        self.default_ports = {
            "mfc1": "COM6",
            "mfc2": "COM5",
            "mfc3": "COM3",
            "cooling": "COM7",
            "valve": "COM4"
        }

        # Ensure that folder exists
        config_folder = os.path.dirname(self.config_path)
        if config_folder and not os.path.exists(config_folder):
            os.makedirs(config_folder)
            
        # Load the configuration
        self.load_config()

    def load_config(self):
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as openfile:
                self.config = json.load(openfile)
        else:
            self.config = {
                "com_ports": self.default_ports.copy()
            }
            self.save_config()  
        return self.config
    
    def save_config(self):
        with open(self.config_path, 'w') as outfile:
            json.dump(self.config, outfile, indent=6)
            return True

    def get_com_ports(self):
        #If com_ports doesn't exist, then it returns {}
        return self.config.get("com_ports", {})

    def set_com_ports(self, ports):
        # Store the com values under "com_ports"
        self.config["com_ports"] = ports
        self.save_config()
    
    def update_com_port(self, device_name, port):
        if "com_ports" not in self.config:
            self.config["com_ports"] = {}
        self.config["com_ports"][device_name] = port
        self.save_config()