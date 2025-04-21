import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import propar
import serial
import time
import threading
import json
import csv
import os
from datetime import datetime
import numpy as np

class MicrofluidicGasSupplySystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Microfluidic Gas Supply System")
        self.root.geometry("1200x800")
        self.root.configure(bg="#f0f0f0")
        
        # Data storage
        self.flow_data = []
        self.temp_data = []
        self.valve_data = []
        self.time_data = []
        self.start_time = None
        self.is_running = False
        self.current_profile = None
        
        # Device connections
        self.flow_controller = None
        self.thermal_bath = None
        self.rotary_valve = None
        
        # Status bar - create it first
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        self.status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Create main frames
        self.create_frames()
        
        # Create UI elements
        self.create_connection_panel()
        self.create_control_panel()
        self.create_visualization_panel()
        self.create_profile_panel()
        
        # Load predefined profiles
        self.load_predefined_profiles()
        
        # Set up periodic data update
        self.update_interval = 500  # ms
        self.update_id = None
        
    def create_frames(self):
        # Top frame for connection settings
        self.connection_frame = ttk.LabelFrame(self.root, text="Device Connections")
        self.connection_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Left frame for controls
        self.control_frame = ttk.LabelFrame(self.root, text="Control Panel")
        self.control_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Right frame for visualization
        self.visualization_frame = ttk.LabelFrame(self.root, text="Data Visualization")
        self.visualization_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Bottom frame for profiles
        self.profile_frame = ttk.LabelFrame(self.root, text="Profiles")
        self.profile_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=5, before=self.status_bar)
        
    def create_connection_panel(self):
        # Flow Controller Connection
        flow_frame = ttk.Frame(self.connection_frame)
        flow_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)
        
        ttk.Label(flow_frame, text="Flow Controller Port:").grid(row=0, column=0, sticky=tk.W)
        self.flow_port = ttk.Entry(flow_frame, width=15)
        self.flow_port.grid(row=0, column=1, padx=5, pady=2)
        self.flow_port.insert(0, "COM1")
        
        ttk.Label(flow_frame, text="Node Address:").grid(row=1, column=0, sticky=tk.W)
        self.flow_node = ttk.Entry(flow_frame, width=15)
        self.flow_node.grid(row=1, column=1, padx=5, pady=2)
        self.flow_node.insert(0, "0")
        
        self.flow_connect_btn = ttk.Button(flow_frame, text="Connect", command=self.connect_flow_controller)
        self.flow_connect_btn.grid(row=0, column=2, rowspan=2, padx=5, pady=2)
        
        # Thermal Bath Connection
        thermal_frame = ttk.Frame(self.connection_frame)
        thermal_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)
        
        ttk.Label(thermal_frame, text="Thermal Bath Port:").grid(row=0, column=0, sticky=tk.W)
        self.thermal_port = ttk.Entry(thermal_frame, width=15)
        self.thermal_port.grid(row=0, column=1, padx=5, pady=2)
        self.thermal_port.insert(0, "COM2")
        
        ttk.Label(thermal_frame, text="Baud Rate:").grid(row=1, column=0, sticky=tk.W)
        self.thermal_baud = ttk.Entry(thermal_frame, width=15)
        self.thermal_baud.grid(row=1, column=1, padx=5, pady=2)
        self.thermal_baud.insert(0, "9600")
        
        self.thermal_connect_btn = ttk.Button(thermal_frame, text="Connect", command=self.connect_thermal_bath)
        self.thermal_connect_btn.grid(row=0, column=2, rowspan=2, padx=5, pady=2)
        
        # Rotary Valve Connection
        valve_frame = ttk.Frame(self.connection_frame)
        valve_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)
        
        ttk.Label(valve_frame, text="Rotary Valve Port:").grid(row=0, column=0, sticky=tk.W)
        self.valve_port = ttk.Entry(valve_frame, width=15)
        self.valve_port.grid(row=0, column=1, padx=5, pady=2)
        self.valve_port.insert(0, "COM3")
        
        ttk.Label(valve_frame, text="Baud Rate:").grid(row=1, column=0, sticky=tk.W)
        self.valve_baud = ttk.Entry(valve_frame, width=15)
        self.valve_baud.grid(row=1, column=1, padx=5, pady=2)
        self.valve_baud.insert(0, "9600")
        
        self.valve_connect_btn = ttk.Button(valve_frame, text="Connect", command=self.connect_rotary_valve)
        self.valve_connect_btn.grid(row=0, column=2, rowspan=2, padx=5, pady=2)
        
    def create_control_panel(self):
        # Flow Control
        flow_control_frame = ttk.LabelFrame(self.control_frame, text="Flow Control")
        flow_control_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(flow_control_frame, text="Flow Rate (mL/min):").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.flow_rate_var = tk.DoubleVar(value=0.0)
        self.flow_rate_entry = ttk.Entry(flow_control_frame, textvariable=self.flow_rate_var, width=10)
        self.flow_rate_entry.grid(row=0, column=1, padx=5, pady=2)
        
        self.flow_rate_scale = ttk.Scale(flow_control_frame, from_=0, to=100, orient=tk.HORIZONTAL, 
                                         variable=self.flow_rate_var, length=200)
        self.flow_rate_scale.grid(row=0, column=2, padx=5, pady=2)
        
        ttk.Button(flow_control_frame, text="Set Flow", command=self.set_flow_rate).grid(row=0, column=3, padx=5, pady=2)
        
        # Temperature Control
        temp_control_frame = ttk.LabelFrame(self.control_frame, text="Temperature Control")
        temp_control_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(temp_control_frame, text="Temperature (°C):").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.temp_var = tk.DoubleVar(value=25.0)
        self.temp_entry = ttk.Entry(temp_control_frame, textvariable=self.temp_var, width=10)
        self.temp_entry.grid(row=0, column=1, padx=5, pady=2)
        
        self.temp_scale = ttk.Scale(temp_control_frame, from_=0, to=100, orient=tk.HORIZONTAL, 
                                    variable=self.temp_var, length=200)
        self.temp_scale.grid(row=0, column=2, padx=5, pady=2)
        
        ttk.Button(temp_control_frame, text="Set Temperature", command=self.set_temperature).grid(row=0, column=3, padx=5, pady=2)
        
        # Valve Control
        valve_control_frame = ttk.LabelFrame(self.control_frame, text="Valve Control")
        valve_control_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(valve_control_frame, text="Valve Position:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.valve_pos_var = tk.IntVar(value=1)
        self.valve_pos_combo = ttk.Combobox(valve_control_frame, textvariable=self.valve_pos_var, 
                                           values=list(range(1, 9)), width=5)
        self.valve_pos_combo.grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Button(valve_control_frame, text="Set Position", command=self.set_valve_position).grid(row=0, column=2, padx=5, pady=2)
        
        # Run Control
        run_control_frame = ttk.LabelFrame(self.control_frame, text="Run Control")
        run_control_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.run_btn = ttk.Button(run_control_frame, text="Start", command=self.toggle_run, width=20)
        self.run_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        ttk.Button(run_control_frame, text="Save Data", command=self.save_data, width=20).pack(side=tk.RIGHT, padx=5, pady=5)
        
        # Status Display
        status_frame = ttk.LabelFrame(self.control_frame, text="Status")
        status_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        ttk.Label(status_frame, text="Current Flow:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.current_flow_var = tk.StringVar(value="0.0 mL/min")
        ttk.Label(status_frame, textvariable=self.current_flow_var).grid(row=0, column=1, sticky=tk.W, padx=5, pady=2)
        
        ttk.Label(status_frame, text="Current Temperature:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        self.current_temp_var = tk.StringVar(value="25.0 °C")
        ttk.Label(status_frame, textvariable=self.current_temp_var).grid(row=1, column=1, sticky=tk.W, padx=5, pady=2)
        
        ttk.Label(status_frame, text="Current Valve Position:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=2)
        self.current_valve_var = tk.StringVar(value="1")
        ttk.Label(status_frame, textvariable=self.current_valve_var).grid(row=2, column=1, sticky=tk.W, padx=5, pady=2)
        
        ttk.Label(status_frame, text="Elapsed Time:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=2)
        self.elapsed_time_var = tk.StringVar(value="00:00:00")
        ttk.Label(status_frame, textvariable=self.elapsed_time_var).grid(row=3, column=1, sticky=tk.W, padx=5, pady=2)
        
    def create_visualization_panel(self):
        # Create matplotlib figure
        self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(6, 6), dpi=100)
        
        # Flow rate plot
        self.ax1.set_title('Flow Rate vs Time')
        self.ax1.set_xlabel('Time (s)')
        self.ax1.set_ylabel('Flow Rate (mL/min)')
        self.flow_line, = self.ax1.plot([], [], 'b-')
        
        # Temperature plot
        self.ax2.set_title('Temperature vs Time')
        self.ax2.set_xlabel('Time (s)')
        self.ax2.set_ylabel('Temperature (°C)')
        self.temp_line, = self.ax2.plot([], [], 'r-')
        
        self.fig.tight_layout()
        
        # Embed the figure in the tkinter window
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.visualization_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
    def create_profile_panel(self):
        # Profile selection
        profile_select_frame = ttk.Frame(self.profile_frame)
        profile_select_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(profile_select_frame, text="Profile:").pack(side=tk.LEFT, padx=5)
        
        self.profile_var = tk.StringVar()
        self.profile_combo = ttk.Combobox(profile_select_frame, textvariable=self.profile_var, width=30)
        self.profile_combo.pack(side=tk.LEFT, padx=5)
        self.profile_combo.bind("<<ComboboxSelected>>", self.load_profile)
        
        ttk.Button(profile_select_frame, text="Load", command=self.load_profile).pack(side=tk.LEFT, padx=5)
        ttk.Button(profile_select_frame, text="Save Current", command=self.save_profile).pack(side=tk.LEFT, padx=5)
        ttk.Button(profile_select_frame, text="New", command=self.new_profile).pack(side=tk.LEFT, padx=5)
        ttk.Button(profile_select_frame, text="Delete", command=self.delete_profile).pack(side=tk.LEFT, padx=5)
        
    def connect_flow_controller(self):
        try:
            port = self.flow_port.get()
            node = int(self.flow_node.get())
            
            # Connect to Bronkhorst Propar Mass-Flow Controller
            self.flow_controller = propar.master(port, baudrate=38400)
            
            # Test connection by reading a parameter
            self.flow_controller.read(node, 33)  # Read measure value
            
            self.status_var.set(f"Connected to Flow Controller on {port}")
            self.flow_connect_btn.configure(text="Disconnect", command=self.disconnect_flow_controller)
            messagebox.showinfo("Connection", "Successfully connected to Flow Controller")
        except Exception as e:
            self.status_var.set(f"Error connecting to Flow Controller: {str(e)}")
            messagebox.showerror("Connection Error", f"Failed to connect to Flow Controller: {str(e)}")
    
    def disconnect_flow_controller(self):
        if self.flow_controller:
            self.flow_controller = None
            self.status_var.set("Disconnected from Flow Controller")
            self.flow_connect_btn.configure(text="Connect", command=self.connect_flow_controller)
    
    def connect_thermal_bath(self):
        try:
            port = self.thermal_port.get()
            baud = int(self.thermal_baud.get())
            
            # Connect to Torrey Pines Scientific Digital Chilling/Heating Dry Bath
            self.thermal_bath = serial.Serial(port, baud, timeout=1)
            
            # Test connection by sending a command
            self.thermal_bath.write(b"*IDN?\r\n")
            response = self.thermal_bath.readline().decode().strip()
            
            if response:
                self.status_var.set(f"Connected to Thermal Bath on {port}")
                self.thermal_connect_btn.configure(text="Disconnect", command=self.disconnect_thermal_bath)
                messagebox.showinfo("Connection", "Successfully connected to Thermal Bath")
            else:
                raise Exception("No response from device")
        except Exception as e:
            self.status_var.set(f"Error connecting to Thermal Bath: {str(e)}")
            messagebox.showerror("Connection Error", f"Failed to connect to Thermal Bath: {str(e)}")
    
    def disconnect_thermal_bath(self):
        if self.thermal_bath:
            self.thermal_bath.close()
            self.thermal_bath = None
            self.status_var.set("Disconnected from Thermal Bath")
            self.thermal_connect_btn.configure(text="Connect", command=self.connect_thermal_bath)
    
    def connect_rotary_valve(self):
        try:
            port = self.valve_port.get()
            baud = int(self.valve_baud.get())
            
            # Connect to AMF RVM Microfluidic Rotary Valve
            self.rotary_valve = serial.Serial(port, baud, timeout=1)
            
            # Test connection by sending a command
            self.rotary_valve.write(b"*IDN?\r\n")
            response = self.rotary_valve.readline().decode().strip()
            
            if response:
                self.status_var.set(f"Connected to Rotary Valve on {port}")
                self.valve_connect_btn.configure(text="Disconnect", command=self.disconnect_rotary_valve)
                messagebox.showinfo("Connection", "Successfully connected to Rotary Valve")
            else:
                raise Exception("No response from device")
        except Exception as e:
            self.status_var.set(f"Error connecting to Rotary Valve: {str(e)}")
            messagebox.showerror("Connection Error", f"Failed to connect to Rotary Valve: {str(e)}")
    
    def disconnect_rotary_valve(self):
        if self.rotary_valve:
            self.rotary_valve.close()
            self.rotary_valve = None
            self.status_var.set("Disconnected from Rotary Valve")
            self.valve_connect_btn.configure(text="Connect", command=self.connect_rotary_valve)
    
    def set_flow_rate(self):
        if not self.flow_controller:
            messagebox.showerror("Error", "Flow Controller not connected")
            return
        
        try:
            flow_rate = self.flow_rate_var.get()
            node = int(self.flow_node.get())
            
            # Set setpoint (parameter 33) to the desired flow rate
            self.flow_controller.write(node, 33, flow_rate)
            
            self.status_var.set(f"Flow rate set to {flow_rate} mL/min")
        except Exception as e:
            self.status_var.set(f"Error setting flow rate: {str(e)}")
            messagebox.showerror("Error", f"Failed to set flow rate: {str(e)}")
    
    def set_temperature(self):
        if not self.thermal_bath:
            messagebox.showerror("Error", "Thermal Bath not connected")
            return
        
        try:
            temperature = self.temp_var.get()
            
            # Send command to set temperature
            self.thermal_bath.write(f"SETTEMP {temperature}\r\n".encode())
            
            self.status_var.set(f"Temperature set to {temperature} °C")
        except Exception as e:
            self.status_var.set(f"Error setting temperature: {str(e)}")
            messagebox.showerror("Error", f"Failed to set temperature: {str(e)}")
    
    def set_valve_position(self):
        if not self.rotary_valve:
            messagebox.showerror("Error", "Rotary Valve not connected")
            return
        
        try:
            position = self.valve_pos_var.get()
            
            # Send command to set valve position
            self.rotary_valve.write(f"POS {position}\r\n".encode())
            
            self.status_var.set(f"Valve position set to {position}")
        except Exception as e:
            self.status_var.set(f"Error setting valve position: {str(e)}")
            messagebox.showerror("Error", f"Failed to set valve position: {str(e)}")
    
    def toggle_run(self):
        if self.is_running:
            self.stop_run()
        else:
            self.start_run()
    
    def start_run(self):
        if not (self.flow_controller and self.thermal_bath and self.rotary_valve):
            messagebox.showerror("Error", "All devices must be connected before starting")
            return
        
        self.is_running = True
        self.start_time = time.time()
        self.run_btn.configure(text="Stop")
        
        # Clear previous data
        self.flow_data = []
        self.temp_data = []
        self.valve_data = []
        self.time_data = []
        
        # Start periodic update
        self.update_data()
        
        self.status_var.set("Run started")
    
    def stop_run(self):
        self.is_running = False
        self.run_btn.configure(text="Start")
        
        # Stop periodic update
        if self.update_id:
            self.root.after_cancel(self.update_id)
            self.update_id = None
        
        self.status_var.set("Run stopped")
    
    def update_data(self):
        if not self.is_running:
            return
        
        try:
            # Calculate elapsed time
            current_time = time.time()
            elapsed = current_time - self.start_time
            self.time_data.append(elapsed)
            
            # Format elapsed time as HH:MM:SS
            hours, remainder = divmod(elapsed, 3600)
            minutes, seconds = divmod(remainder, 60)
            self.elapsed_time_var.set(f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}")
            
            # Read flow rate
            node = int(self.flow_node.get())
            flow_rate = self.flow_controller.read(node, 33)
            self.flow_data.append(flow_rate)
            self.current_flow_var.set(f"{flow_rate:.2f} mL/min")
            
            # Read temperature
            self.thermal_bath.write(b"TEMP?\r\n")
            temp_response = self.thermal_bath.readline().decode().strip()
            temperature = float(temp_response)
            self.temp_data.append(temperature)
            self.current_temp_var.set(f"{temperature:.1f} °C")
            
            # Read valve position
            self.rotary_valve.write(b"POS?\r\n")
            valve_response = self.rotary_valve.readline().decode().strip()
            valve_position = int(valve_response)
            self.valve_data.append(valve_position)
            self.current_valve_var.set(str(valve_position))
            
            # Update plots
            self.update_plots()
            
            # Schedule next update
            self.update_id = self.root.after(self.update_interval, self.update_data)
        except Exception as e:
            self.status_var.set(f"Error updating data: {str(e)}")
            messagebox.showerror("Error", f"Failed to update data: {str(e)}")
            self.stop_run()
    
    def update_plots(self):
        # Update flow rate plot
        self.flow_line.set_data(self.time_data, self.flow_data)
        self.ax1.relim()
        self.ax1.autoscale_view()
        
        # Update temperature plot
        self.temp_line.set_data(self.time_data, self.temp_data)
        self.ax2.relim()
        self.ax2.autoscale_view()
        
        # Redraw canvas
        self.canvas.draw()
    
    def save_data(self):
        if not self.time_data:
            messagebox.showinfo("Info", "No data to save")
            return
        
        try:
            # Ask for file location
            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                title="Save Data As"
            )
            
            if not filename:
                return
            
            # Save data to CSV
            with open(filename, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Time (s)', 'Flow Rate (mL/min)', 'Temperature (°C)', 'Valve Position'])
                
                for i in range(len(self.time_data)):
                    writer.writerow([
                        self.time_data[i],
                        self.flow_data[i],
                        self.temp_data[i],
                        self.valve_data[i]
                    ])
            
            self.status_var.set(f"Data saved to {filename}")
            messagebox.showinfo("Success", f"Data saved to {filename}")
        except Exception as e:
            self.status_var.set(f"Error saving data: {str(e)}")
            messagebox.showerror("Error", f"Failed to save data: {str(e)}")
    
    def load_predefined_profiles(self):
        # Create profiles directory if it doesn't exist
        if not os.path.exists("profiles"):
            os.makedirs("profiles")
            
            # Create some default profiles
            default_profiles = {
                "Standard Flow": {
                    "flow_rate": 10.0,
                    "temperature": 25.0,
                    "valve_position": 1
                },
                "High Flow": {
                    "flow_rate": 50.0,
                    "temperature": 30.0,
                    "valve_position": 2
                },
                "Low Temperature": {
                    "flow_rate": 5.0,
                    "temperature": 10.0,
                    "valve_position": 3
                }
            }
            
            for name, settings in default_profiles.items():
                with open(f"profiles/{name}.json", 'w') as f:
                    json.dump(settings, f)
        
        # Load profile names
        self.update_profile_list()
    
    def update_profile_list(self):
        profiles = []
        for file in os.listdir("profiles"):
            if file.endswith(".json"):
                profiles.append(os.path.splitext(file)[0])
        
        self.profile_combo['values'] = profiles
        
        if profiles:
            self.profile_combo.current(0)
    
    def load_profile(self, event=None):
        profile_name = self.profile_var.get()
        
        if not profile_name:
            return
        
        try:
            with open(f"profiles/{profile_name}.json", 'r') as f:
                profile = json.load(f)
            
            # Update UI with profile settings
            self.flow_rate_var.set(profile["flow_rate"])
            self.temp_var.set(profile["temperature"])
            self.valve_pos_var.set(profile["valve_position"])
            
            self.current_profile = profile_name
            self.status_var.set(f"Loaded profile: {profile_name}")
        except Exception as e:
            self.status_var.set(f"Error loading profile: {str(e)}")
            messagebox.showerror("Error", f"Failed to load profile: {str(e)}")
    
    def save_profile(self):
        if not self.current_profile:
            self.new_profile()
            return
        
        try:
            profile = {
                "flow_rate": self.flow_rate_var.get(),
                "temperature": self.temp_var.get(),
                "valve_position": self.valve_pos_var.get()
            }
            
            with open(f"profiles/{self.current_profile}.json", 'w') as f:
                json.dump(profile, f)
            
            self.status_var.set(f"Saved profile: {self.current_profile}")
        except Exception as e:
            self.status_var.set(f"Error saving profile: {str(e)}")
            messagebox.showerror("Error", f"Failed to save profile: {str(e)}")
    
    def new_profile(self):
        profile_name = simpledialog.askstring("New Profile", "Enter profile name:")
        
        if not profile_name:
            return
        
        try:
            profile = {
                "flow_rate": self.flow_rate_var.get(),
                "temperature": self.temp_var.get(),
                "valve_position": self.valve_pos_var.get()
            }
            
            with open(f"profiles/{profile_name}.json", 'w') as f:
                json.dump(profile, f)
            
            self.current_profile = profile_name
            self.update_profile_list()
            self.profile_var.set(profile_name)
            
            self.status_var.set(f"Created new profile: {profile_name}")
        except Exception as e:
            self.status_var.set(f"Error creating profile: {str(e)}")
            messagebox.showerror("Error", f"Failed to create profile: {str(e)}")
    
    def delete_profile(self):
        profile_name = self.profile_var.get()
        
        if not profile_name:
            return
        
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete profile '{profile_name}'?")
        
        if not confirm:
            return
        
        try:
            os.remove(f"profiles/{profile_name}.json")
            
            self.current_profile = None
            self.update_profile_list()
            self.status_var.set(f"Deleted profile: {profile_name}")
        except Exception as e:
            self.status_var.set(f"Error deleting profile: {str(e)}")
            messagebox.showerror("Error", f"Failed to delete profile: {str(e)}")

# For testing without actual hardware
class MockDevices:
    @staticmethod
    def mock_flow_controller():
        class MockFlow:
            def read(self, node, parameter):
                return 10.0 + 2.0 * np.sin(time.time() / 10)
                
            def write(self, node, parameter, value):
                pass
        
        return MockFlow()
    
    @staticmethod
    def mock_thermal_bath():
        class MockBath:
            def __init__(self):
                self.temp = 25.0
                self._last_command = b""
                
            def write(self, command):
                self._last_command = command
                if b"SETTEMP" in command:
                    try:
                        self.temp = float(command.decode().split()[1])
                    except:
                        pass
                
            def readline(self):
                if b"TEMP?" in self._last_command:
                    return f"{self.temp + 0.5 * np.sin(time.time() / 20)}".encode()
                return b"OK"
                
            def close(self):
                pass
        
        return MockBath()
    
    @staticmethod
    def mock_rotary_valve():
        class MockValve:
            def __init__(self):
                self.position = 1
                self._last_command = b""
                
            def write(self, command):
                self._last_command = command
                if b"POS " in command:
                    try:
                        self.position = int(command.decode().split()[1])
                    except:
                        pass
                
            def readline(self):
                if b"POS?" in self._last_command:
                    return f"{self.position}".encode()
                return b"OK"
                
            def close(self):
                pass
        
        return MockValve()

# Main application
def main():
    root = tk.Tk()
    app = MicrofluidicGasSupplySystem(root)
    
    # For testing without hardware, uncomment these lines
    app.flow_controller = MockDevices.mock_flow_controller()
    app.thermal_bath = MockDevices.mock_thermal_bath()
    app.rotary_valve = MockDevices.mock_rotary_valve()
    
    root.mainloop()

if __name__ == "__main__":
    main()