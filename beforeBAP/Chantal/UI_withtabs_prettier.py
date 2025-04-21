import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation
from matplotlib.figure import Figure
import time
import threading
import json
import os
import pandas as pd
from datetime import datetime

# This is a mockup UI design for the microfluidic gas supply system
# In a real implementation, these would be replaced with actual device control code
class BronkhorstController:
    def __init__(self, port='COM1'):
        self.port = port
        self.connected = False
        self.instrument = None
        self.flow_rate = 0
        self.target_flow_rate = 0
        
    def connect(self):
        try:
            import propar
            self.instrument = propar.instrument(self.port)
            self.connected = True
            return self.connected
        except Exception as e:
            print(f"Error connecting to Bronkhorst controller: {e}")
            # Fallback to simulation mode
            self.connected = True
            return self.connected
        
    def set_flow_rate(self, value):
        self.target_flow_rate = value
        if self.connected and self.instrument:
            try:
                # Set setpoint (parameter 206 is setpoint in output units)
                self.instrument.writeParameter(206, value)
                return True
            except Exception as e:
                print(f"Error setting flow rate: {e}")
                return False
        return False
        
    def get_flow_rate(self):
        if self.connected and self.instrument:
            try:
                # Read measure (parameter 205 is measure in output units)
                self.flow_rate = self.instrument.readParameter(205)
                return self.flow_rate
            except Exception as e:
                print(f"Error reading flow rate: {e}")
                # Fallback to simulation
                if self.flow_rate < self.target_flow_rate:
                    self.flow_rate += min(0.1, self.target_flow_rate - self.flow_rate)
                elif self.flow_rate > self.target_flow_rate:
                    self.flow_rate -= min(0.1, self.flow_rate - self.target_flow_rate)
                return self.flow_rate
        else:
            # Simulation mode
            if self.flow_rate < self.target_flow_rate:
                self.flow_rate += min(0.1, self.target_flow_rate - self.flow_rate)
            elif self.flow_rate > self.target_flow_rate:
                self.flow_rate -= min(0.1, self.flow_rate - self.target_flow_rate)
            return self.flow_rate
        
    def disconnect(self):
        self.connected = False
        self.instrument = None


class TorreyPinesController:
    def __init__(self, port='COM2'):
        self.port = port
        self.connected = False
        self.ser = None
        self.temperature = 25.0
        self.target_temperature = 25.0
        
    def connect(self):
        try:
            import serial
            self.ser = serial.Serial(self.port, 9600, timeout=1)
            self.connected = True
            return self.connected
        except Exception as e:
            print(f"Error connecting to Torrey Pines controller: {e}")
            # Fallback to simulation mode
            self.connected = True
            return self.connected
        
    def set_temperature(self, value):
        self.target_temperature = value
        if self.connected and self.ser:
            try:
                # Send command to set temperature
                self.ser.write(f"SET TEMP {value}\r\n".encode())
                response = self.ser.readline().decode().strip()
                return "OK" in response
            except Exception as e:
                print(f"Error setting temperature: {e}")
                return False
        return False
        
    def get_temperature(self):
        if self.connected and self.ser:
            try:
                # Send command to read temperature
                self.ser.write("READ TEMP\r\n".encode())
                response = self.ser.readline().decode().strip()
                self.temperature = float(response)
                return self.temperature
            except Exception as e:
                print(f"Error reading temperature: {e}")
                # Fallback to simulation
                if self.temperature < self.target_temperature:
                    self.temperature += min(0.05, self.target_temperature - self.temperature)
                elif self.temperature > self.target_temperature:
                    self.temperature -= min(0.05, self.temperature - self.target_temperature)
                return self.temperature
        else:
            # Simulation mode
            if self.temperature < self.target_temperature:
                self.temperature += min(0.05, self.target_temperature - self.temperature)
            elif self.temperature > self.target_temperature:
                self.temperature -= min(0.05, self.temperature - self.target_temperature)
            return self.temperature
        
    def disconnect(self):
        if self.ser:
            try:
                self.ser.close()
            except Exception as e:
                print(f"Error disconnecting from Torrey Pines controller: {e}")
        self.connected = False
        self.ser = None


class AMFValveController:
    def __init__(self, port='COM3'):
        self.port = port
        self.connected = False
        self.valve = None
        self.position = 1
        self.max_positions = 6
        
    def connect(self):
        try:
            import rvm_valve
            self.valve = rvm_valve.rvm_valve(self.port)
            self.connected = True
            return self.connected
        except Exception as e:
            print(f"Error connecting to AMF valve controller: {e}")
            # Fallback to simulation mode
            self.connected = True
            return self.connected
        
    def set_position(self, position):
        if 1 <= position <= self.max_positions:
            self.position = position
            if self.connected and self.valve:
                try:
                    # Move valve to position
                    self.valve.move(position)
                    return True
                except Exception as e:
                    print(f"Error setting valve position: {e}")
                    return False
        return False
        
    def get_position(self):
        if self.connected and self.valve:
            try:
                # Get current position
                # Note: According to documentation, this method might need implementation
                # Fallback to stored position if method not available
                try:
                    pos = self.valve.get_valve_position()
                    self.position = pos
                except:
                    # If get_valve_position is not implemented, use stored position
                    pass
                return self.position
            except Exception as e:
                print(f"Error getting valve position: {e}")
                return self.position
        return self.position
        
    def home(self):
        if self.connected and self.valve:
            try:
                # Home the valve
                self.valve.home()
                self.position = 1
                return True
            except Exception as e:
                print(f"Error homing valve: {e}")
                self.position = 1
                return False
        else:
            # Simulation mode
            self.position = 1
            return True
        
    def disconnect(self):
        # Close the connection
        self.connected = False
        self.valve = None


class ProfileManager:
    def __init__(self, profiles_dir="profiles"):
        self.profiles_dir = profiles_dir
        self.current_profile = None
        self.standard_profiles = {
            "Constant Flow": {
                "description": "Maintain constant flow rate",
                "steps": [
                    {"time": 0, "flow": 5.0, "temperature": 25.0, "valve": 1}
                ]
            },
            "Temperature Ramp": {
                "description": "Gradually increase temperature",
                "steps": [
                    {"time": 0, "flow": 5.0, "temperature": 25.0, "valve": 1},
                    {"time": 300, "flow": 5.0, "temperature": 35.0, "valve": 1},
                    {"time": 600, "flow": 5.0, "temperature": 45.0, "valve": 1}
                ]
            },
            "Valve Sequence": {
                "description": "Cycle through valve positions",
                "steps": [
                    {"time": 0, "flow": 5.0, "temperature": 25.0, "valve": 1},
                    {"time": 60, "flow": 5.0, "temperature": 25.0, "valve": 2},
                    {"time": 120, "flow": 5.0, "temperature": 25.0, "valve": 3},
                    {"time": 180, "flow": 5.0, "temperature": 25.0, "valve": 4}
                ]
            }
        }
        
        # Create profiles directory if it doesn't exist
        if not os.path.exists(profiles_dir):
            os.makedirs(profiles_dir)
            
        # Save standard profiles if they don't exist
        for name, profile in self.standard_profiles.items():
            file_path = os.path.join(self.profiles_dir, f"{name}.json")
            if not os.path.exists(file_path):
                with open(file_path, 'w') as f:
                    json.dump(profile, f, indent=4)
    
    def get_profiles(self):
        profiles = []
        for filename in os.listdir(self.profiles_dir):
            if filename.endswith('.json'):
                profiles.append(filename[:-5])  # Remove .json extension
        return profiles
    
    def load_profile(self, name):
        file_path = os.path.join(self.profiles_dir, f"{name}.json")
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                self.current_profile = json.load(f)
                return self.current_profile
        return None
    
    def save_profile(self, name, profile):
        file_path = os.path.join(self.profiles_dir, f"{name}.json")
        with open(file_path, 'w') as f:
            json.dump(profile, f, indent=4)
        return True


class DataLogger:
    def __init__(self, log_dir="logs"):
        self.log_dir = log_dir
        self.logging = False
        self.log_file = None
        self.log_interval = 1.0  # seconds
        self.data = []
        
        # Create logs directory if it doesn't exist
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
    
    def start_logging(self):
        if not self.logging:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.log_file = os.path.join(self.log_dir, f"log_{timestamp}.csv")
            self.logging = True
            self.data = []
            return True
        return False
    
    def log_data(self, time_elapsed, flow_rate, temperature, valve_position):
        if self.logging:
            self.data.append({
                'time': time_elapsed,
                'flow_rate': flow_rate,
                'temperature': temperature,
                'valve_position': valve_position
            })
            return True
        return False
    
    def stop_logging(self):
        if self.logging:
            df = pd.DataFrame(self.data)
            df.to_csv(self.log_file, index=False)
            self.logging = False
            return self.log_file
        return None


class MicrofluidicSystemUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Microfluidic Gas Supply System")
        self.root.geometry("1200x800")
        
        # Set theme for better appearance
        style = ttk.Style()
        if 'clam' in style.theme_names():
            style.theme_use('clam')
            
        # Configure colors for better visibility
        style.configure('TButton', font=('Arial', 10, 'bold'))
        style.configure('TLabel', font=('Arial', 10))
        style.configure('TFrame', background='#f0f0f0')
        style.configure('TLabelframe', background='#f0f0f0')
        style.configure('TLabelframe.Label', font=('Arial', 10, 'bold'))
        
        # Initialize device controllers
        self.flow_controller = BronkhorstController()
        self.temp_controller = TorreyPinesController()
        self.valve_controller = AMFValveController()
        
        # Initialize profile manager and data logger
        self.profile_manager = ProfileManager()
        self.data_logger = DataLogger()
        
        # Data for plotting
        self.time_data = []
        self.flow_data = []
        self.temp_data = []
        self.valve_data = []
        
        # Runtime variables
        self.running = False
        self.start_time = 0
        self.elapsed_time = 0
        
        # Create UI components
        self.create_menu()
        self.create_main_frame()
        
        # Start update loop
        self.update_data()
    
    def create_menu(self):
        menubar = tk.Menu(self.root)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Connect Devices", command=self.connect_devices)
        file_menu.add_command(label="Disconnect Devices", command=self.disconnect_devices)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)
        
        # Settings menu
        settings_menu = tk.Menu(menubar, tearoff=0)
        settings_menu.add_command(label="Communication Settings", command=self.show_comm_settings)
        settings_menu.add_command(label="Logging Settings", command=self.show_log_settings)
        menubar.add_cascade(label="Settings", menu=settings_menu)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="Help", command=self.show_help)
        help_menu.add_command(label="About", command=self.show_about)
        menubar.add_cascade(label="Help", menu=help_menu)
        
        self.root.config(menu=menubar)
    
    def create_main_frame(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Add a title label with larger font
        title_label = ttk.Label(main_frame, text="Microfluidic Gas Supply System", 
                               font=('Arial', 16, 'bold'))
        title_label.pack(pady=(0, 10))
        
        # Top control frame
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Start/Stop button with more prominent styling
        self.start_button = ttk.Button(control_frame, text="Start", command=self.toggle_run, 
                                     style='Action.TButton')
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        # Create a special style for the action button
        style = ttk.Style()
        style.configure('Action.TButton', font=('Arial', 12, 'bold'), padding=5)
        
        # Home button
        self.home_button = ttk.Button(control_frame, text="Home Valve", command=self.home_valve)
        self.home_button.pack(side=tk.LEFT, padx=5)
        
        # Profile selection
        ttk.Label(control_frame, text="Profile:").pack(side=tk.LEFT, padx=(20, 5))
        self.profile_var = tk.StringVar()
        self.profile_combo = ttk.Combobox(control_frame, textvariable=self.profile_var, width=20)
        self.profile_combo.pack(side=tk.LEFT, padx=5)
        self.update_profile_list()
        
        # Load profile button
        self.load_button = ttk.Button(control_frame, text="Load", command=self.load_profile)
        self.load_button.pack(side=tk.LEFT, padx=5)
        
        # Elapsed time display
        self.time_var = tk.StringVar(value="Time: 00:00:00")
        ttk.Label(control_frame, textvariable=self.time_var).pack(side=tk.RIGHT, padx=5)
        
        # Create notebook (tabbed interface)
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create tabs
        self.create_dashboard_tab()
        self.create_flow_tab()
        self.create_temperature_tab()
        self.create_valve_tab()
        self.create_profile_tab()
        self.create_logging_tab()
        
        # Status bar
        status_frame = ttk.Frame(main_frame)
        status_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Device status indicators
        self.flow_status_var = tk.StringVar(value="Flow Controller: Disconnected")
        self.temp_status_var = tk.StringVar(value="Temperature Controller: Disconnected")
        self.valve_status_var = tk.StringVar(value="Valve Controller: Disconnected")
        
        ttk.Label(status_frame, textvariable=self.flow_status_var).pack(side=tk.LEFT, padx=5)
        ttk.Label(status_frame, textvariable=self.temp_status_var).pack(side=tk.LEFT, padx=5)
        ttk.Label(status_frame, textvariable=self.valve_status_var).pack(side=tk.LEFT, padx=5)
    
    def create_dashboard_tab(self):
        dashboard_frame = ttk.Frame(self.notebook)
        self.notebook.add(dashboard_frame, text="Dashboard")
        
        # Add a welcome message and instructions
        welcome_frame = ttk.LabelFrame(dashboard_frame, text="System Overview")
        welcome_frame.pack(fill=tk.X, padx=10, pady=10)
        
        welcome_text = """
Welcome to the Microfluidic Gas Supply System control interface!

This dashboard provides real-time monitoring of all system parameters.
Use the tabs above to control individual components or manage profiles.
Press the START button to begin system operation.

System Status:
        """
        welcome_label = ttk.Label(welcome_frame, text=welcome_text, font=('Arial', 10))
        welcome_label.pack(padx=10, pady=10, anchor=tk.W)
        
        # Add status indicators
        status_frame = ttk.Frame(welcome_frame)
        status_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Flow status
        self.flow_indicator_var = tk.StringVar(value="Waiting")
        ttk.Label(status_frame, text="Flow Controller:", font=('Arial', 10, 'bold')).grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Label(status_frame, textvariable=self.flow_indicator_var).grid(row=0, column=1, sticky=tk.W, padx=5, pady=2)
        
        # Temperature status
        self.temp_indicator_var = tk.StringVar(value="Waiting")
        ttk.Label(status_frame, text="Temperature Controller:", font=('Arial', 10, 'bold')).grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Label(status_frame, textvariable=self.temp_indicator_var).grid(row=1, column=1, sticky=tk.W, padx=5, pady=2)
        
        # Valve status
        self.valve_indicator_var = tk.StringVar(value="Waiting")
        ttk.Label(status_frame, text="Valve Controller:", font=('Arial', 10, 'bold')).grid(row=2, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Label(status_frame, textvariable=self.valve_indicator_var).grid(row=2, column=1, sticky=tk.W, padx=5, pady=2)
        
        # Create a frame for the graphs
        graph_frame = ttk.Frame(dashboard_frame)
        graph_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create figure for plots
        self.dashboard_fig = Figure(figsize=(10, 6), dpi=100)
        
        # Create subplots
        self.flow_ax = self.dashboard_fig.add_subplot(311)
        self.temp_ax = self.dashboard_fig.add_subplot(312)
        self.valve_ax = self.dashboard_fig.add_subplot(313)
        
        # Set titles
        self.flow_ax.set_title("Flow Rate")
        self.temp_ax.set_title("Temperature")
        self.valve_ax.set_title("Valve Position")
        
        # Set y-labels
        self.flow_ax.set_ylabel("Flow Rate (mL/min)")
        self.temp_ax.set_ylabel("Temperature (°C)")
        self.valve_ax.set_ylabel("Position")
        
        # Set x-label only on the bottom plot
        self.valve_ax.set_xlabel("Time (s)")
        
        # Adjust layout
        self.dashboard_fig.tight_layout()
        
        # Create canvas
        self.dashboard_canvas = FigureCanvasTkAgg(self.dashboard_fig, graph_frame)
        self.dashboard_canvas.draw()
        self.dashboard_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def create_flow_tab(self):
        flow_frame = ttk.Frame(self.notebook)
        self.notebook.add(flow_frame, text="Flow Control")
        
        # Flow control frame
        control_frame = ttk.LabelFrame(flow_frame, text="Flow Rate Control")
        control_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Flow rate slider
        ttk.Label(control_frame, text="Flow Rate (mL/min):").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.flow_scale = ttk.Scale(control_frame, from_=0, to=100, orient=tk.HORIZONTAL, length=300)
        self.flow_scale.grid(row=0, column=1, padx=5, pady=5)
        self.flow_scale.set(0)
        
        # Flow rate entry
        self.flow_var = tk.DoubleVar(value=0.0)
        flow_entry = ttk.Entry(control_frame, textvariable=self.flow_var, width=10)
        flow_entry.grid(row=0, column=2, padx=5, pady=5)
        
        # Set button
        set_flow_button = ttk.Button(control_frame, text="Set", command=self.set_flow_rate)
        set_flow_button.grid(row=0, column=3, padx=5, pady=5)
        
        # Current flow rate display
        ttk.Label(control_frame, text="Current Flow Rate:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.current_flow_var = tk.StringVar(value="0.0 mL/min")
        ttk.Label(control_frame, textvariable=self.current_flow_var).grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        
        # Preset buttons
        preset_frame = ttk.LabelFrame(flow_frame, text="Presets")
        preset_frame.pack(fill=tk.X, padx=10, pady=10)
        
        presets = [("Low", 5.0), ("Medium", 25.0), ("High", 50.0), ("Max", 100.0)]
        for i, (name, value) in enumerate(presets):
            button = ttk.Button(preset_frame, text=name, command=lambda v=value: self.set_flow_preset(v))
            button.grid(row=0, column=i, padx=10, pady=5)
        
        # Graph frame
        graph_frame = ttk.LabelFrame(flow_frame, text="Flow Rate Graph")
        graph_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create figure for flow plot
        self.flow_fig = Figure(figsize=(6, 4), dpi=100)
        self.flow_plot_ax = self.flow_fig.add_subplot(111)
        self.flow_plot_ax.set_xlabel("Time (s)")
        self.flow_plot_ax.set_ylabel("Flow Rate (mL/min)")
        self.flow_plot_ax.set_title("Flow Rate vs Time")
        
        # Create canvas
        self.flow_canvas = FigureCanvasTkAgg(self.flow_fig, graph_frame)
        self.flow_canvas.draw()
        self.flow_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def create_temperature_tab(self):
        temp_frame = ttk.Frame(self.notebook)
        self.notebook.add(temp_frame, text="Temperature Control")
        
        # Temperature control frame
        control_frame = ttk.LabelFrame(temp_frame, text="Temperature Control")
        control_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Temperature slider
        ttk.Label(control_frame, text="Temperature (°C):").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.temp_scale = ttk.Scale(control_frame, from_=0, to=100, orient=tk.HORIZONTAL, length=300)
        self.temp_scale.grid(row=0, column=1, padx=5, pady=5)
        self.temp_scale.set(25)
        
        # Temperature entry
        self.temp_var = tk.DoubleVar(value=25.0)
        temp_entry = ttk.Entry(control_frame, textvariable=self.temp_var, width=10)
        temp_entry.grid(row=0, column=2, padx=5, pady=5)
        
        # Set button
        set_temp_button = ttk.Button(control_frame, text="Set", command=self.set_temperature)
        set_temp_button.grid(row=0, column=3, padx=5, pady=5)
        
        # Current temperature display
        ttk.Label(control_frame, text="Current Temperature:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.current_temp_var = tk.StringVar(value="25.0 °C")
        ttk.Label(control_frame, textvariable=self.current_temp_var).grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        
        # Preset buttons
        preset_frame = ttk.LabelFrame(temp_frame, text="Presets")
        preset_frame.pack(fill=tk.X, padx=10, pady=10)
        
        presets = [("Cold", 10.0), ("Room", 25.0), ("Warm", 40.0), ("Hot", 60.0)]
        for i, (name, value) in enumerate(presets):
            button = ttk.Button(preset_frame, text=name, command=lambda v=value: self.set_temp_preset(v))
            button.grid(row=0, column=i, padx=10, pady=5)
        
        # Graph frame
        graph_frame = ttk.LabelFrame(temp_frame, text="Temperature Graph")
        graph_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create figure for temperature plot
        self.temp_fig = Figure(figsize=(6, 4), dpi=100)
        self.temp_plot_ax = self.temp_fig.add_subplot(111)
        self.temp_plot_ax.set_xlabel("Time (s)")
        self.temp_plot_ax.set_ylabel("Temperature (°C)")
        self.temp_plot_ax.set_title("Temperature vs Time")
        
        # Create canvas
        self.temp_canvas = FigureCanvasTkAgg(self.temp_fig, graph_frame)
        self.temp_canvas.draw()
        self.temp_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def create_valve_tab(self):
        valve_frame = ttk.Frame(self.notebook)
        self.notebook.add(valve_frame, text="Valve Control")
        
        # Valve control frame
        control_frame = ttk.LabelFrame(valve_frame, text="Valve Position Control")
        control_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Position buttons
        positions_frame = ttk.Frame(control_frame)
        positions_frame.pack(pady=10)
        
        for i in range(1, 7):
            button = ttk.Button(positions_frame, text=str(i), width=3, 
                               command=lambda pos=i: self.set_valve_position(pos))
            button.grid(row=0, column=i-1, padx=5)
        
        # Home button
        home_button = ttk.Button(control_frame, text="Home", command=self.home_valve)
        home_button.pack(pady=5)
        
        # Current position display
        position_frame = ttk.Frame(control_frame)
        position_frame.pack(pady=10)
        
        ttk.Label(position_frame, text="Current Position:").grid(row=0, column=0, padx=5)
        self.current_position_var = tk.StringVar(value="1")
        ttk.Label(position_frame, textvariable=self.current_position_var).grid(row=0, column=1, padx=5)
        
        # Sequence programming frame
        sequence_frame = ttk.LabelFrame(valve_frame, text="Valve Sequence Programming")
        sequence_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Sequence table
        self.sequence_tree = ttk.Treeview(sequence_frame, columns=("Step", "Position", "Duration"), show="headings")
        self.sequence_tree.heading("Step", text="Step")
        self.sequence_tree.heading("Position", text="Position")
        self.sequence_tree.heading("Duration", text="Duration (s)")
        self.sequence_tree.column("Step", width=50)
        self.sequence_tree.column("Position", width=100)
        self.sequence_tree.column("Duration", width=100)
        self.sequence_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Add sequence controls
        controls_frame = ttk.Frame(sequence_frame)
        controls_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(controls_frame, text="Position:").grid(row=0, column=0, padx=5, pady=5)
        self.seq_position_var = tk.IntVar(value=1)
        position_combo = ttk.Combobox(controls_frame, textvariable=self.seq_position_var, values=list(range(1, 7)), width=5)
        position_combo.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(controls_frame, text="Duration (s):").grid(row=0, column=2, padx=5, pady=5)
        self.seq_duration_var = tk.IntVar(value=10)
        duration_entry = ttk.Entry(controls_frame, textvariable=self.seq_duration_var, width=10)
        duration_entry.grid(row=0, column=3, padx=5, pady=5)
        
        add_button = ttk.Button(controls_frame, text="Add Step", command=self.add_sequence_step)
        add_button.grid(row=0, column=4, padx=5, pady=5)
        
        remove_button = ttk.Button(controls_frame, text="Remove Step", command=self.remove_sequence_step)
        remove_button.grid(row=0, column=5, padx=5, pady=5)
        
        clear_button = ttk.Button(controls_frame, text="Clear All", command=self.clear_sequence)
        clear_button.grid(row=0, column=6, padx=5, pady=5)
    
    def create_profile_tab(self):
        profile_frame = ttk.Frame(self.notebook)
        self.notebook.add(profile_frame, text="Profile Management")
        
        # Split into two frames
        left_frame = ttk.Frame(profile_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        right_frame = ttk.Frame(profile_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Profile list frame
        list_frame = ttk.LabelFrame(left_frame, text="Available Profiles")
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # Profile listbox
        self.profile_listbox = tk.Listbox(list_frame)
        self.profile_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.update_profile_list()
        
        # Profile buttons
        button_frame = ttk.Frame(list_frame)
        button_frame.pack(fill=tk.X, pady=5)
        
        load_button = ttk.Button(button_frame, text="Load", command=self.load_selected_profile)
        load_button.pack(side=tk.LEFT, padx=5)
        
        delete_button = ttk.Button(button_frame, text="Delete", command=self.delete_profile)
        delete_button.pack(side=tk.LEFT, padx=5)
        
        # Profile editor frame
        editor_frame = ttk.LabelFrame(right_frame, text="Profile Editor")
        editor_frame.pack(fill=tk.BOTH, expand=True)
        
        # Profile name
        name_frame = ttk.Frame(editor_frame)
        name_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(name_frame, text="Profile Name:").pack(side=tk.LEFT, padx=5)
        self.profile_name_var = tk.StringVar()
        name_entry = ttk.Entry(name_frame, textvariable=self.profile_name_var, width=30)
        name_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # Profile description
        desc_frame = ttk.Frame(editor_frame)
        desc_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(desc_frame, text="Description:").pack(side=tk.LEFT, padx=5)
        self.profile_desc_var = tk.StringVar()
        desc_entry = ttk.Entry(desc_frame, textvariable=self.profile_desc_var, width=30)
        desc_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # Profile steps
        steps_frame = ttk.LabelFrame(editor_frame, text="Profile Steps")
        steps_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Steps table
        self.steps_tree = ttk.Treeview(steps_frame, 
                                      columns=("Time", "Flow", "Temperature", "Valve"), 
                                      show="headings")
        self.steps_tree.heading("Time", text="Time (s)")
        self.steps_tree.heading("Flow", text="Flow (mL/min)")
        self.steps_tree.heading("Temperature", text="Temp (°C)")
        self.steps_tree.heading("Valve", text="Valve Pos")
        
        self.steps_tree.column("Time", width=80)
        self.steps_tree.column("Flow", width=80)
        self.steps_tree.column("Temperature", width=80)
        self.steps_tree.column("Valve", width=80)
        
        self.steps_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Step editor
        step_editor = ttk.Frame(editor_frame)
        step_editor.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(step_editor, text="Time (s):").grid(row=0, column=0, padx=5, pady=5)
        self.step_time_var = tk.IntVar(value=0)
        time_entry = ttk.Entry(step_editor, textvariable=self.step_time_var, width=8)
        time_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(step_editor, text="Flow:").grid(row=0, column=2, padx=5, pady=5)
        self.step_flow_var = tk.DoubleVar(value=5.0)
        flow_entry = ttk.Entry(step_editor, textvariable=self.step_flow_var, width=8)
        flow_entry.grid(row=0, column=3, padx=5, pady=5)
        
        ttk.Label(step_editor, text="Temp:").grid(row=0, column=4, padx=5, pady=5)
        self.step_temp_var = tk.DoubleVar(value=25.0)
        temp_entry = ttk.Entry(step_editor, textvariable=self.step_temp_var, width=8)
        temp_entry.grid(row=0, column=5, padx=5, pady=5)
        
        ttk.Label(step_editor, text="Valve:").grid(row=0, column=6, padx=5, pady=5)
        self.step_valve_var = tk.IntVar(value=1)
        valve_combo = ttk.Combobox(step_editor, textvariable=self.step_valve_var, values=list(range(1, 7)), width=5)
        valve_combo.grid(row=0, column=7, padx=5, pady=5)
        
        # Step buttons
        step_buttons = ttk.Frame(editor_frame)
        step_buttons.pack(fill=tk.X, padx=5, pady=5)
        
        add_step_button = ttk.Button(step_buttons, text="Add Step", command=self.add_profile_step)
        add_step_button.pack(side=tk.LEFT, padx=5)
        
        remove_step_button = ttk.Button(step_buttons, text="Remove Step", command=self.remove_profile_step)
        remove_step_button.pack(side=tk.LEFT, padx=5)
        
        clear_steps_button = ttk.Button(step_buttons, text="Clear Steps", command=self.clear_profile_steps)
        clear_steps_button.pack(side=tk.LEFT, padx=5)
        
        # Save profile button
        save_frame = ttk.Frame(editor_frame)
        save_frame.pack(fill=tk.X, padx=5, pady=10)
        
        save_button = ttk.Button(save_frame, text="Save Profile", command=self.save_profile)
        save_button.pack(side=tk.RIGHT, padx=5)
    
    def create_logging_tab(self):
        logging_frame = ttk.Frame(self.notebook)
        self.notebook.add(logging_frame, text="Data Logging")
        
        # Logging control frame
        control_frame = ttk.LabelFrame(logging_frame, text="Logging Controls")
        control_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Logging interval
        interval_frame = ttk.Frame(control_frame)
        interval_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(interval_frame, text="Logging Interval (s):").pack(side=tk.LEFT, padx=5)
        self.log_interval_var = tk.DoubleVar(value=1.0)
        interval_entry = ttk.Entry(interval_frame, textvariable=self.log_interval_var, width=10)
        interval_entry.pack(side=tk.LEFT, padx=5)
        
        set_interval_button = ttk.Button(interval_frame, text="Set", 
                                        command=lambda: setattr(self.data_logger, 'log_interval', self.log_interval_var.get()))
        set_interval_button.pack(side=tk.LEFT, padx=5)
        
        # Log directory
        dir_frame = ttk.Frame(control_frame)
        dir_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(dir_frame, text="Log Directory:").pack(side=tk.LEFT, padx=5)
        self.log_dir_var = tk.StringVar(value=self.data_logger.log_dir)
        dir_entry = ttk.Entry(dir_frame, textvariable=self.log_dir_var, width=30)
        dir_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # Logging status
        status_frame = ttk.Frame(control_frame)
        status_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.logging_status_var = tk.StringVar(value="Logging: Inactive")
        ttk.Label(status_frame, textvariable=self.logging_status_var).pack(side=tk.LEFT, padx=5)
        
        self.log_button = ttk.Button(status_frame, text="Start Logging", command=self.toggle_logging)
        self.log_button.pack(side=tk.RIGHT, padx=5)
        
        # Data display frame
        data_frame = ttk.LabelFrame(logging_frame, text="Logged Data")
        data_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Data table
        self.data_tree = ttk.Treeview(data_frame, 
                                     columns=("Time", "Flow", "Temperature", "Valve"), 
                                     show="headings")
        self.data_tree.heading("Time", text="Time (s)")
        self.data_tree.heading("Flow", text="Flow (mL/min)")
        self.data_tree.heading("Temperature", text="Temp (°C)")
        self.data_tree.heading("Valve", text="Valve Pos")
        
        self.data_tree.column("Time", width=80)
        self.data_tree.column("Flow", width=80)
        self.data_tree.column("Temperature", width=80)
        self.data_tree.column("Valve", width=80)
        
        self.data_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Export button
        export_button = ttk.Button(data_frame, text="Export Data", command=self.export_data)
        export_button.pack(side=tk.RIGHT, padx=5, pady=5)
    
    def connect_devices(self):
        # Connect to all devices
        flow_connected = self.flow_controller.connect()
        temp_connected = self.temp_controller.connect()
        valve_connected = self.valve_controller.connect()
        
        # Update status indicators
        self.flow_status_var.set(f"Flow Controller: {'Connected' if flow_connected else 'Disconnected'}")
        self.temp_status_var.set(f"Temperature Controller: {'Connected' if temp_connected else 'Disconnected'}")
        self.valve_status_var.set(f"Valve Controller: {'Connected' if valve_connected else 'Disconnected'}")
    
    def disconnect_devices(self):
        # Disconnect all devices
        self.flow_controller.disconnect()
        self.temp_controller.disconnect()
        self.valve_controller.disconnect()
        
        # Update status indicators
        self.flow_status_var.set("Flow Controller: Disconnected")
        self.temp_status_var.set("Temperature Controller: Disconnected")
        self.valve_status_var.set("Valve Controller: Disconnected")
    
    def show_comm_settings(self):
        # Create a settings dialog
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Communication Settings")
        settings_window.geometry("400x300")
        settings_window.transient(self.root)
        settings_window.grab_set()
        
        # Flow controller settings
        flow_frame = ttk.LabelFrame(settings_window, text="Flow Controller")
        flow_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(flow_frame, text="Port:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        flow_port_var = tk.StringVar(value=self.flow_controller.port)
        flow_port_entry = ttk.Entry(flow_frame, textvariable=flow_port_var)
        flow_port_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Temperature controller settings
        temp_frame = ttk.LabelFrame(settings_window, text="Temperature Controller")
        temp_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(temp_frame, text="Port:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        temp_port_var = tk.StringVar(value=self.temp_controller.port)
        temp_port_entry = ttk.Entry(temp_frame, textvariable=temp_port_var)
        temp_port_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Valve controller settings
        valve_frame = ttk.LabelFrame(settings_window, text="Valve Controller")
        valve_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(valve_frame, text="Port:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        valve_port_var = tk.StringVar(value=self.valve_controller.port)
        valve_port_entry = ttk.Entry(valve_frame, textvariable=valve_port_var)
        valve_port_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Save button
        def save_settings():
            self.flow_controller.port = flow_port_var.get()
            self.temp_controller.port = temp_port_var.get()
            self.valve_controller.port = valve_port_var.get()
            settings_window.destroy()
        
        save_button = ttk.Button(settings_window, text="Save", command=save_settings)
        save_button.pack(pady=10)
    
    def show_log_settings(self):
        # Create a settings dialog
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Logging Settings")
        settings_window.geometry("400x200")
        settings_window.transient(self.root)
        settings_window.grab_set()
        
        # Logging settings
        log_frame = ttk.Frame(settings_window)
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        ttk.Label(log_frame, text="Log Directory:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        log_dir_var = tk.StringVar(value=self.data_logger.log_dir)
        log_dir_entry = ttk.Entry(log_frame, textvariable=log_dir_var, width=30)
        log_dir_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(log_frame, text="Log Interval (s):").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        log_interval_var = tk.DoubleVar(value=self.data_logger.log_interval)
        log_interval_entry = ttk.Entry(log_frame, textvariable=log_interval_var, width=10)
        log_interval_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        
        # Save button
        def save_settings():
            self.data_logger.log_dir = log_dir_var.get()
            self.data_logger.log_interval = log_interval_var.get()
            self.log_dir_var.set(log_dir_var.get())
            self.log_interval_var.set(log_interval_var.get())
            settings_window.destroy()
        
        save_button = ttk.Button(settings_window, text="Save", command=save_settings)
        save_button.pack(pady=10)
    
    def show_help(self):
        # Create a help dialog
        help_window = tk.Toplevel(self.root)
        help_window.title("Help")
        help_window.geometry("600x400")
        help_window.transient(self.root)
        
        # Help text
        help_text = """
        Microfluidic Gas Supply System Help
        
        This application controls a microfluidic gas supply system with the following components:
        - Bronkhorst Propar Mass-Flow Controller
        - Torrey Pines Scientific Digital Chilling/Heating Dry Baths
        - AMF RVM Industrial Microfluidic Rotary Valve
        
        Basic Usage:
        1. Connect to devices using File > Connect Devices
        2. Set flow rate, temperature, and valve position using respective tabs
        3. Create and load profiles for automated operation
        4. Start/stop the system using the Start/Stop button
        5. Monitor real-time data on the Dashboard tab
        6. Log data for later analysis using the Data Logging tab
        
        For more information, please refer to the user manual.
        """
        
        text_widget = tk.Text(help_window, wrap=tk.WORD)
        text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        text_widget.insert(tk.END, help_text)
        text_widget.config(state=tk.DISABLED)
    
    def show_about(self):
        # Create an about dialog
        about_window = tk.Toplevel(self.root)
        about_window.title("About")
        about_window.geometry("400x200")
        about_window.transient(self.root)
        
        # About text
        about_text = """
        Microfluidic Gas Supply System
        Version 1.0
        
        A control interface for microfluidic gas supply systems.
        
        Supports:
        - Bronkhorst Propar Mass-Flow Controller
        - Torrey Pines Scientific Digital Chilling/Heating Dry Baths
        - AMF RVM Industrial Microfluidic Rotary Valve
        
        © 2025 All rights reserved.
        """
        
        text_widget = tk.Text(about_window, wrap=tk.WORD)
        text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        text_widget.insert(tk.END, about_text)
        text_widget.config(state=tk.DISABLED)
    
    def toggle_run(self):
        if not self.running:
            # Start the system
            self.running = True
            self.start_time = time.time()
            self.start_button.config(text="STOP")
            
            # Show a confirmation message
            tk.messagebox.showinfo("System Started", "The microfluidic gas supply system has been started successfully!")
            
            # Start data logging if not already started
            if not self.data_logger.logging:
                self.data_logger.start_logging()
                self.logging_status_var.set("Logging: Active")
                self.log_button.config(text="Stop Logging")
        else:
            # Stop the system
            self.running = False
            self.start_button.config(text="START")
            
            # Show a confirmation message
            tk.messagebox.showinfo("System Stopped", "The microfluidic gas supply system has been stopped.")
            
            # Stop data logging if it was started automatically
            if self.data_logger.logging:
                log_file = self.data_logger.stop_logging()
                self.logging_status_var.set(f"Logging: Inactive (Saved to {log_file})")
                self.log_button.config(text="Start Logging")
    
    def toggle_logging(self):
        if not self.data_logger.logging:
            # Start logging
            self.data_logger.start_logging()
            self.logging_status_var.set("Logging: Active")
            self.log_button.config(text="Stop Logging")
            
            # Show confirmation message
            tk.messagebox.showinfo("Logging Started", "Data logging has been started. Data will be saved automatically.")
        else:
            # Stop logging
            log_file = self.data_logger.stop_logging()
            self.logging_status_var.set(f"Logging: Inactive (Saved to {log_file})")
            self.log_button.config(text="Start Logging")
            
            # Show confirmation with file path
            tk.messagebox.showinfo("Logging Stopped", f"Data logging has been stopped.\nData saved to: {log_file}")
    
    def export_data(self):
        if self.data_logger.data:
            # Create a timestamp for the filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"export_{timestamp}.csv"
            filepath = os.path.join(self.data_logger.log_dir, filename)
            
            # Create DataFrame and save to CSV
            df = pd.DataFrame(self.data_logger.data)
            df.to_csv(filepath, index=False)
            
            # Show confirmation
            tk.messagebox.showinfo("Export Complete", f"Data exported to {filepath}")
        else:
            tk.messagebox.showinfo("No Data", "No data available to export")
    
    def set_flow_rate(self):
        # Get flow rate from entry
        flow_rate = self.flow_var.get()
        
        # Set flow rate in controller
        self.flow_controller.set_flow_rate(flow_rate)
        
        # Update slider to match
        self.flow_scale.set(flow_rate)
    
    def set_flow_preset(self, value):
        # Set flow rate to preset value
        self.flow_var.set(value)
        self.flow_scale.set(value)
        self.set_flow_rate()
    
    def set_temperature(self):
        # Get temperature from entry
        temperature = self.temp_var.get()
        
        # Set temperature in controller
        self.temp_controller.set_temperature(temperature)
        
        # Update slider to match
        self.temp_scale.set(temperature)
    
    def set_temp_preset(self, value):
        # Set temperature to preset value
        self.temp_var.set(value)
        self.temp_scale.set(value)
        self.set_temperature()
    
    def set_valve_position(self, position):
        # Set valve position in controller
        self.valve_controller.set_position(position)
    
    def home_valve(self):
        # Home the valve
        self.valve_controller.home()
    
    def add_sequence_step(self):
        # Get values from entry fields
        position = self.seq_position_var.get()
        duration = self.seq_duration_var.get()
        
        # Add to treeview
        step = len(self.sequence_tree.get_children()) + 1
        self.sequence_tree.insert("", "end", values=(step, position, duration))
    
    def remove_sequence_step(self):
        # Get selected item
        selected = self.sequence_tree.selection()
        if selected:
            self.sequence_tree.delete(selected)
            
            # Renumber steps
            for i, item in enumerate(self.sequence_tree.get_children(), 1):
                values = self.sequence_tree.item(item, "values")
                self.sequence_tree.item(item, values=(i, values[1], values[2]))
    
    def clear_sequence(self):
        # Clear all items
        for item in self.sequence_tree.get_children():
            self.sequence_tree.delete(item)
    
    def update_profile_list(self):
        # Update profile combobox
        profiles = self.profile_manager.get_profiles()
        self.profile_combo['values'] = profiles
        
        # Update profile listbox if it exists (only after profile tab is created)
        if hasattr(self, 'profile_listbox'):
            self.profile_listbox.delete(0, tk.END)
            for profile in profiles:
                self.profile_listbox.insert(tk.END, profile)
    
    def load_profile(self):
        # Get selected profile
        profile_name = self.profile_var.get()
        if profile_name:
            profile = self.profile_manager.load_profile(profile_name)
            if profile:
                # Display profile info
                tk.messagebox.showinfo("Profile Loaded", f"Loaded profile: {profile_name}")
    
    def load_selected_profile(self):
        # Get selected profile from listbox
        selection = self.profile_listbox.curselection()
        if selection:
            profile_name = self.profile_listbox.get(selection[0])
            profile = self.profile_manager.load_profile(profile_name)
            
            if profile:
                # Set profile name and description
                self.profile_name_var.set(profile_name)
                self.profile_desc_var.set(profile.get('description', ''))
                
                # Clear and populate steps
                self.clear_profile_steps()
                for step in profile.get('steps', []):
                    self.steps_tree.insert("", "end", values=(
                        step.get('time', 0),
                        step.get('flow', 0),
                        step.get('temperature', 25),
                        step.get('valve', 1)
                    ))
    
    def delete_profile(self):
        # Get selected profile from listbox
        selection = self.profile_listbox.curselection()
        if selection:
            profile_name = self.profile_listbox.get(selection[0])
            
            # Confirm deletion
            if tk.messagebox.askyesno("Confirm Delete", f"Delete profile '{profile_name}'?"):
                # Delete profile file
                file_path = os.path.join(self.profile_manager.profiles_dir, f"{profile_name}.json")
                if os.path.exists(file_path):
                    os.remove(file_path)
                    self.update_profile_list()
    
    def add_profile_step(self):
        # Get values from entry fields
        time_val = self.step_time_var.get()
        flow_val = self.step_flow_var.get()
        temp_val = self.step_temp_var.get()
        valve_val = self.step_valve_var.get()
        
        # Add to treeview
        self.steps_tree.insert("", "end", values=(time_val, flow_val, temp_val, valve_val))
    
    def remove_profile_step(self):
        # Get selected item
        selected = self.steps_tree.selection()
        if selected:
            self.steps_tree.delete(selected)
    
    def clear_profile_steps(self):
        # Clear all items
        for item in self.steps_tree.get_children():
            self.steps_tree.delete(item)
    
    def save_profile(self):
        # Get profile name and description
        name = self.profile_name_var.get()
        description = self.profile_desc_var.get()
        
        if not name:
            tk.messagebox.showerror("Error", "Profile name is required")
            return
        
        # Get steps from treeview
        steps = []
        for item in self.steps_tree.get_children():
            values = self.steps_tree.item(item, "values")
            steps.append({
                'time': int(values[0]),
                'flow': float(values[1]),
                'temperature': float(values[2]),
                'valve': int(values[3])
            })
        
        # Create profile
        profile = {
            'description': description,
            'steps': steps
        }
        
        # Save profile
        self.profile_manager.save_profile(name, profile)
        
        # Update profile list
        self.update_profile_list()
        
        # Show confirmation
        tk.messagebox.showinfo("Profile Saved", f"Profile '{name}' saved successfully")
    
    def update_data(self):
        # Update elapsed time if running
        if self.running:
            self.elapsed_time = time.time() - self.start_time
            hours, remainder = divmod(int(self.elapsed_time), 3600)
            minutes, seconds = divmod(remainder, 60)
            self.time_var.set(f"Time: {hours:02d}:{minutes:02d}:{seconds:02d}")
        
        # Get current values from controllers
        flow_rate = self.flow_controller.get_flow_rate()
        temperature = self.temp_controller.get_temperature()
        valve_position = self.valve_controller.get_position()
        
        # Update displays
        self.current_flow_var.set(f"{flow_rate:.1f} mL/min")
        self.current_temp_var.set(f"{temperature:.1f} °C")
        self.current_position_var.set(f"{valve_position}")
        
        # Update status indicators
        if hasattr(self, 'flow_indicator_var'):
            if self.running:
                self.flow_indicator_var.set(f"Active - {flow_rate:.1f} mL/min")
            else:
                self.flow_indicator_var.set(f"Standby - {flow_rate:.1f} mL/min")
                
        if hasattr(self, 'temp_indicator_var'):
            if self.running:
                if temperature < self.temp_controller.target_temperature - 0.5:
                    self.temp_indicator_var.set(f"Heating - {temperature:.1f} °C")
                elif temperature > self.temp_controller.target_temperature + 0.5:
                    self.temp_indicator_var.set(f"Cooling - {temperature:.1f} °C")
                else:
                    self.temp_indicator_var.set(f"Stable - {temperature:.1f} °C")
            else:
                self.temp_indicator_var.set(f"Standby - {temperature:.1f} °C")
                
        if hasattr(self, 'valve_indicator_var'):
            self.valve_indicator_var.set(f"Position {valve_position}")
        
        # Add data to arrays for plotting
        self.time_data.append(self.elapsed_time)
        self.flow_data.append(flow_rate)
        self.temp_data.append(temperature)
        self.valve_data.append(valve_position)
        
        # Keep all data points for complete history
        # No limit on data points to show full history
        
        # Update plots
        self.update_plots()
        
        # Log data if logging is active
        if self.data_logger.logging and self.running:
            self.data_logger.log_data(self.elapsed_time, flow_rate, temperature, valve_position)
            
            # Update data tree
            if len(self.data_logger.data) % 10 == 0:  # Update every 10 data points to avoid UI lag
                self.update_data_tree()
        
        # Schedule next update
        self.root.after(100, self.update_data)
    
    def update_plots(self):
        # Clear plots
        self.flow_ax.clear()
        self.temp_ax.clear()
        self.valve_ax.clear()
        self.flow_plot_ax.clear()
        self.temp_plot_ax.clear()
        
        # Set titles
        self.flow_ax.set_title("Flow Rate")
        self.temp_ax.set_title("Temperature")
        self.valve_ax.set_title("Valve Position")
        self.flow_plot_ax.set_title("Flow Rate vs Time")
        self.temp_plot_ax.set_title("Temperature vs Time")
        
        # Set y-labels
        self.flow_ax.set_ylabel("Flow Rate (mL/min)")
        self.temp_ax.set_ylabel("Temperature (°C)")
        self.valve_ax.set_ylabel("Position")
        self.flow_plot_ax.set_ylabel("Flow Rate (mL/min)")
        self.temp_plot_ax.set_ylabel("Temperature (°C)")
        
        # Set x-label only on the bottom plot
        self.valve_ax.set_xlabel("Time (s)")
        self.flow_plot_ax.set_xlabel("Time (s)")
        self.temp_plot_ax.set_xlabel("Time (s)")
        
        # Plot data
        if self.time_data:
            self.flow_ax.plot(self.time_data, self.flow_data, 'b-')
            self.temp_ax.plot(self.time_data, self.temp_data, 'r-')
            self.valve_ax.step(self.time_data, self.valve_data, 'g-', where='post')
            self.flow_plot_ax.plot(self.time_data, self.flow_data, 'b-')
            self.temp_plot_ax.plot(self.time_data, self.temp_data, 'r-')
            
            # Set y-limits
            self.flow_ax.set_ylim(0, max(max(self.flow_data) * 1.1, 0.1))
            self.temp_ax.set_ylim(min(min(self.temp_data) * 0.9, 20), max(max(self.temp_data) * 1.1, 30))
            self.valve_ax.set_ylim(0, max(max(self.valve_data) + 1, 7))
            self.flow_plot_ax.set_ylim(0, max(max(self.flow_data) * 1.1, 0.1))
            self.temp_plot_ax.set_ylim(min(min(self.temp_data) * 0.9, 20), max(max(self.temp_data) * 1.1, 30))
            
            # Set x-limits to show full history
            if len(self.time_data) > 1:
                self.flow_ax.set_xlim(0, max(self.time_data))
                self.temp_ax.set_xlim(0, max(self.time_data))
                self.valve_ax.set_xlim(0, max(self.time_data))
                self.flow_plot_ax.set_xlim(0, max(self.time_data))
                self.temp_plot_ax.set_xlim(0, max(self.time_data))
        
        # Adjust layout
        self.dashboard_fig.tight_layout()
        self.flow_fig.tight_layout()
        self.temp_fig.tight_layout()
        
        # Draw canvases
        self.dashboard_canvas.draw()
        self.flow_canvas.draw()
        self.temp_canvas.draw()
    
    def update_data_tree(self):
        # Clear tree
        for item in self.data_tree.get_children():
            self.data_tree.delete(item)
        
        # Add last 20 data points
        for data in self.data_logger.data[-20:]:
            self.data_tree.insert("", "end", values=(
                f"{data['time']:.1f}",
                f"{data['flow_rate']:.1f}",
                f"{data['temperature']:.1f}",
                f"{data['valve_position']}"
            ))


def main():
    root = tk.Tk()
    app = MicrofluidicSystemUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
