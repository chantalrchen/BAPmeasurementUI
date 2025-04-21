import tkinter as tk
from tkinter import ttk, messagebox
import serial
import minimalmodbus
import time
from threading import Thread

class LabEquipmentControl:
    def __init__(self, root):
        self.root = root
        self.root.title("Microfluidics Control System")
        self.root.geometry("900x700")
        
        # Device connection status
        self.mfc_connected = False
        self.cooling_connected = False
        self.valve_connected = False
        
        # Initialize device variables
        self.mfc_flow_rate = 0.0
        self.cooling_temp = 20.0
        self.valve_position = 1
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True)
        
        # Create tabs
        self.create_connection_tab()
        self.create_mfc_tab()
        self.create_cooling_tab()
        self.create_valve_tab()
        self.create_sequence_tab()
        
        # Status bar
        self.status_bar = tk.Label(root, text="System Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
    def create_connection_tab(self):
        """Tab for connecting to all devices"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Connections")
        
        # Connection frame
        conn_frame = ttk.LabelFrame(tab, text="Device Connections", padding=10)
        conn_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # MFC Connection
        ttk.Label(conn_frame, text="MFC (Bronkhorst):").grid(row=0, column=0, sticky=tk.W)
        self.mfc_port_entry = ttk.Entry(conn_frame, width=10)
        self.mfc_port_entry.grid(row=0, column=1, padx=5)
        self.mfc_port_entry.insert(0, "COM3")
        self.mfc_connect_btn = ttk.Button(conn_frame, text="Connect", command=self.connect_mfc)
        self.mfc_connect_btn.grid(row=0, column=2, padx=5)
        self.mfc_status = ttk.Label(conn_frame, text="Disconnected", foreground="red")
        self.mfc_status.grid(row=0, column=3, padx=5)
        
        # Cooling System Connection
        ttk.Label(conn_frame, text="Cooling (Torrey Pines):").grid(row=1, column=0, sticky=tk.W)
        self.cooling_port_entry = ttk.Entry(conn_frame, width=10)
        self.cooling_port_entry.grid(row=1, column=1, padx=5)
        self.cooling_port_entry.insert(0, "COM4")
        self.cooling_connect_btn = ttk.Button(conn_frame, text="Connect", command=self.connect_cooling)
        self.cooling_connect_btn.grid(row=1, column=2, padx=5)
        self.cooling_status = ttk.Label(conn_frame, text="Disconnected", foreground="red")
        self.cooling_status.grid(row=1, column=3, padx=5)
        
        # Valve Connection
        ttk.Label(conn_frame, text="Valve (RVM Rotary):").grid(row=2, column=0, sticky=tk.W)
        self.valve_port_entry = ttk.Entry(conn_frame, width=10)
        self.valve_port_entry.grid(row=2, column=1, padx=5)
        self.valve_port_entry.insert(0, "COM5")
        self.valve_connect_btn = ttk.Button(conn_frame, text="Connect", command=self.connect_valve)
        self.valve_connect_btn.grid(row=2, column=2, padx=5)
        self.valve_status = ttk.Label(conn_frame, text="Disconnected", foreground="red")
        self.valve_status.grid(row=2, column=3, padx=5)
        
        # Test all connections button
        ttk.Button(conn_frame, text="Test All Connections", command=self.test_all_connections).grid(row=3, column=0, columnspan=4, pady=10)
        
    def create_mfc_tab(self):
        """Tab for MFC control"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="MFC Control")
        
        mfc_frame = ttk.LabelFrame(tab, text="Mass Flow Controller", padding=10)
        mfc_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Flow rate control
        ttk.Label(mfc_frame, text="Flow Rate (ml/min):").grid(row=0, column=0, sticky=tk.W)
        self.flow_rate_entry = ttk.Entry(mfc_frame, width=10)
        self.flow_rate_entry.grid(row=0, column=1, padx=5)
        self.flow_rate_entry.insert(0, "0.0")
        ttk.Button(mfc_frame, text="Set", command=self.set_mfc_flow).grid(row=0, column=2, padx=5)
        
        # Current flow rate display
        ttk.Label(mfc_frame, text="Current Flow:").grid(row=1, column=0, sticky=tk.W)
        self.current_flow_label = ttk.Label(mfc_frame, text="0.0 ml/min")
        self.current_flow_label.grid(row=1, column=1, sticky=tk.W)
        
        # Flow rate slider
        self.flow_slider = ttk.Scale(mfc_frame, from_=0, to=100, orient=tk.HORIZONTAL, command=self.update_flow_slider)
        self.flow_slider.grid(row=2, column=0, columnspan=3, sticky=tk.EW, pady=10)
        
        # Gas selection
        ttk.Label(mfc_frame, text="Gas Type:").grid(row=3, column=0, sticky=tk.W)
        self.gas_type = tk.StringVar()
        gas_options = ["N2", "O2", "Ar", "CO2", "Air", "Custom"]
        ttk.OptionMenu(mfc_frame, self.gas_type, gas_options[0], *gas_options).grid(row=3, column=1, sticky=tk.W)
        
        # MFC info
        ttk.Label(mfc_frame, text="MFC Range:").grid(row=4, column=0, sticky=tk.W)
        ttk.Label(mfc_frame, text="0-100 ml/min").grid(row=4, column=1, sticky=tk.W)
        
    def create_cooling_tab(self):
        """Tab for cooling system control"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Temperature Control")
        
        cooling_frame = ttk.LabelFrame(tab, text="Torrey Pines IC20XR", padding=10)
        cooling_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Temperature setpoint
        ttk.Label(cooling_frame, text="Temperature (°C):").grid(row=0, column=0, sticky=tk.W)
        self.temp_setpoint_entry = ttk.Entry(cooling_frame, width=10)
        self.temp_setpoint_entry.grid(row=0, column=1, padx=5)
        self.temp_setpoint_entry.insert(0, "20.0")
        ttk.Button(cooling_frame, text="Set", command=self.set_cooling_temp).grid(row=0, column=2, padx=5)
        
        # Current temperature display
        ttk.Label(cooling_frame, text="Current Temp:").grid(row=1, column=0, sticky=tk.W)
        self.current_temp_label = ttk.Label(cooling_frame, text="-- °C")
        self.current_temp_label.grid(row=1, column=1, sticky=tk.W)
        
        # Temperature slider
        self.temp_slider = ttk.Scale(cooling_frame, from_=-20, to=100, orient=tk.HORIZONTAL, command=self.update_temp_slider)
        self.temp_slider.grid(row=2, column=0, columnspan=3, sticky=tk.EW, pady=10)
        
        # Cooling/heating mode
        ttk.Label(cooling_frame, text="Mode:").grid(row=3, column=0, sticky=tk.W)
        self.cooling_mode = tk.StringVar()
        ttk.Radiobutton(cooling_frame, text="Cooling", variable=self.cooling_mode, value="cool").grid(row=3, column=1, sticky=tk.W)
        ttk.Radiobutton(cooling_frame, text="Heating", variable=self.cooling_mode, value="heat").grid(row=3, column=2, sticky=tk.W)
        self.cooling_mode.set("cool")
        
        # Start/stop button
        ttk.Button(cooling_frame, text="Start", command=self.start_cooling).grid(row=4, column=0, pady=10)
        ttk.Button(cooling_frame, text="Stop", command=self.stop_cooling).grid(row=4, column=1, pady=10)
        
    def create_valve_tab(self):
        """Tab for valve control"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Valve Control")
        
        valve_frame = ttk.LabelFrame(tab, text="RVM Rotary Valve", padding=10)
        valve_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Valve position selection
        ttk.Label(valve_frame, text="Valve Position:").grid(row=0, column=0, sticky=tk.W)
        self.valve_position_var = tk.IntVar()
        self.valve_position_var.set(1)
        
        # Create position buttons in a grid
        positions = [1, 2, 3, 4, 5, 6, 7, 8]
        for i, pos in enumerate(positions):
            ttk.Radiobutton(valve_frame, text=f"Port {pos}", variable=self.valve_position_var, 
                           value=pos, command=self.set_valve_position).grid(
                           row=1 + i//4, column=i%4, sticky=tk.W, padx=5, pady=2)
        
        # Current position display
        ttk.Label(valve_frame, text="Current Position:").grid(row=3, column=0, sticky=tk.W)
        self.current_valve_position = ttk.Label(valve_frame, text="--")
        self.current_valve_position.grid(row=3, column=1, sticky=tk.W)
        
        # Valve control buttons
        ttk.Button(valve_frame, text="Next Position", command=self.next_valve_position).grid(row=4, column=0, pady=10)
        ttk.Button(valve_frame, text="Previous Position", command=self.prev_valve_position).grid(row=4, column=1, pady=10)
        
    def create_sequence_tab(self):
        """Tab for creating automated sequences"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Sequences")
        
        seq_frame = ttk.LabelFrame(tab, text="Automated Sequences", padding=10)
        seq_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Sequence list
        ttk.Label(seq_frame, text="Sequence Steps:").grid(row=0, column=0, sticky=tk.W)
        self.sequence_listbox = tk.Listbox(seq_frame, height=10, width=50)
        self.sequence_listbox.grid(row=1, column=0, columnspan=3, pady=5)
        
        # Add step buttons
        ttk.Button(seq_frame, text="Add MFC Step", command=self.add_mfc_step).grid(row=2, column=0, pady=5)
        ttk.Button(seq_frame, text="Add Temp Step", command=self.add_temp_step).grid(row=2, column=1, pady=5)
        ttk.Button(seq_frame, text="Add Valve Step", command=self.add_valve_step).grid(row=2, column=2, pady=5)
        
        # Step parameters
        ttk.Label(seq_frame, text="Duration (s):").grid(row=3, column=0, sticky=tk.W)
        self.step_duration = ttk.Entry(seq_frame, width=8)
        self.step_duration.grid(row=3, column=1, sticky=tk.W)
        self.step_duration.insert(0, "10")
        
        # Sequence control
        ttk.Button(seq_frame, text="Remove Step", command=self.remove_step).grid(row=4, column=0, pady=10)
        ttk.Button(seq_frame, text="Clear All", command=self.clear_sequence).grid(row=4, column=1, pady=10)
        ttk.Button(seq_frame, text="Run Sequence", command=self.run_sequence).grid(row=4, column=2, pady=10)
        
        # Sequence status
        self.sequence_status = ttk.Label(seq_frame, text="Sequence ready")
        self.sequence_status.grid(row=5, column=0, columnspan=3)
        
    # Device connection methods
    def connect_mfc(self):
        try:
            port = self.mfc_port_entry.get()
            # Initialize MFC connection using minimalmodbus or Bronkhorst's FlowDDE
            # Example: self.mfc = minimalmodbus.Instrument(port, 1)
            self.mfc_connected = True
            self.mfc_status.config(text="Connected", foreground="green")
            self.update_status("MFC connected successfully")
        except Exception as e:
            self.mfc_connected = False
            self.mfc_status.config(text="Connection Failed", foreground="red")
            self.update_status(f"MFC connection error: {str(e)}")
            messagebox.showerror("Connection Error", f"Failed to connect to MFC:\n{str(e)}")
    
    def connect_cooling(self):
        try:
            port = self.cooling_port_entry.get()
            # Initialize connection to Torrey Pines cooling system
            # Example: self.cooling = serial.Serial(port, baudrate=19200, timeout=1)
            self.cooling_connected = True
            self.cooling_status.config(text="Connected", foreground="green")
            self.update_status("Cooling system connected successfully")
        except Exception as e:
            self.cooling_connected = False
            self.cooling_status.config(text="Connection Failed", foreground="red")
            self.update_status(f"Cooling connection error: {str(e)}")
            messagebox.showerror("Connection Error", f"Failed to connect to cooling system:\n{str(e)}")
    
    def connect_valve(self):
        try:
            port = self.valve_port_entry.get()
            # Initialize connection to RVM rotary valve
            # Example: self.valve = serial.Serial(port, baudrate=9600, timeout=1)
            self.valve_connected = True
            self.valve_status.config(text="Connected", foreground="green")
            self.update_status("Valve connected successfully")
        except Exception as e:
            self.valve_connected = False
            self.valve_status.config(text="Connection Failed", foreground="red")
            self.update_status(f"Valve connection error: {str(e)}")
            messagebox.showerror("Connection Error", f"Failed to connect to valve:\n{str(e)}")
    
    def test_all_connections(self):
        self.connect_mfc()
        self.connect_cooling()
        self.connect_valve()
        
        if all([self.mfc_connected, self.cooling_connected, self.valve_connected]):
            messagebox.showinfo("Connection Test", "All devices connected successfully!")
        else:
            messagebox.showwarning("Connection Test", "Some devices failed to connect")
    
    # Device control methods
    def set_mfc_flow(self):
        if not self.mfc_connected:
            messagebox.showwarning("Connection Error", "MFC is not connected")
            return
        
        try:
            flow_rate = float(self.flow_rate_entry.get())
            # Example: self.mfc.write_register(registeraddress, flow_rate, number_of_decimals=1)
            self.mfc_flow_rate = flow_rate
            self.current_flow_label.config(text=f"{flow_rate} ml/min")
            self.update_status(f"MFC flow rate set to {flow_rate} ml/min")
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid number for flow rate")
    
    def update_flow_slider(self, value):
        flow_rate = float(value)
        self.flow_rate_entry.delete(0, tk.END)
        self.flow_rate_entry.insert(0, f"{flow_rate:.1f}")
        if self.mfc_connected:
            self.set_mfc_flow()
    
    def set_cooling_temp(self):
        if not self.cooling_connected:
            messagebox.showwarning("Connection Error", "Cooling system is not connected")
            return
        
        try:
            temp = float(self.temp_setpoint_entry.get())
            # Example command for Torrey Pines: self.cooling.write(f"T {temp}\r".encode())
            self.cooling_temp = temp
            self.current_temp_label.config(text=f"{temp} °C")
            self.update_status(f"Temperature setpoint set to {temp} °C")
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid number for temperature")
    
    def update_temp_slider(self, value):
        temp = float(value)
        self.temp_setpoint_entry.delete(0, tk.END)
        self.temp_setpoint_entry.insert(0, f"{temp:.1f}")
        if self.cooling_connected:
            self.set_cooling_temp()
    
    def start_cooling(self):
        if not self.cooling_connected:
            messagebox.showwarning("Connection Error", "Cooling system is not connected")
            return
        
        # Example: self.cooling.write("START\r".encode())
        self.update_status("Cooling system started")
    
    def stop_cooling(self):
        if not self.cooling_connected:
            messagebox.showwarning("Connection Error", "Cooling system is not connected")
            return
        
        # Example: self.cooling.write("STOP\r".encode())
        self.update_status("Cooling system stopped")
    
    def set_valve_position(self):
        if not self.valve_connected:
            messagebox.showwarning("Connection Error", "Valve is not connected")
            return
        
        position = self.valve_position_var.get()
        # Example command for RVM valve: self.valve.write(f"GO {position}\r".encode())
        self.valve_position = position
        self.current_valve_position.config(text=f"Port {position}")
        self.update_status(f"Valve set to position {position}")
    
    def next_valve_position(self):
        current = self.valve_position_var.get()
        new_pos = current + 1 if current < 8 else 1
        self.valve_position_var.set(new_pos)
        self.set_valve_position()
    
    def prev_valve_position(self):
        current = self.valve_position_var.get()
        new_pos = current - 1 if current > 1 else 8
        self.valve_position_var.set(new_pos)
        self.set_valve_position()
    
    # Sequence methods
    def add_mfc_step(self):
        try:
            duration = float(self.step_duration.get())
            flow = float(self.flow_rate_entry.get())
            step = f"MFC: {flow} ml/min for {duration} s"
            self.sequence_listbox.insert(tk.END, step)
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers for flow rate and duration")
    
    def add_temp_step(self):
        try:
            duration = float(self.step_duration.get())
            temp = float(self.temp_setpoint_entry.get())
            step = f"Temp: {temp} °C for {duration} s"
            self.sequence_listbox.insert(tk.END, step)
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers for temperature and duration")
    
    def add_valve_step(self):
        try:
            duration = float(self.step_duration.get())
            pos = self.valve_position_var.get()
            step = f"Valve: Port {pos} for {duration} s"
            self.sequence_listbox.insert(tk.END, step)
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid number for duration")
    
    def remove_step(self):
        try:
            selection = self.sequence_listbox.curselection()
            self.sequence_listbox.delete(selection)
        except:
            messagebox.showwarning("Selection Error", "Please select a step to remove")
    
    def clear_sequence(self):
        self.sequence_listbox.delete(0, tk.END)
    
    def run_sequence(self):
        if not all([self.mfc_connected, self.cooling_connected, self.valve_connected]):
            messagebox.showwarning("Connection Error", "Not all devices are connected")
            return
        
        sequence = self.sequence_listbox.get(0, tk.END)
        if not sequence:
            messagebox.showwarning("Sequence Error", "No steps in sequence")
            return
        
        # Run sequence in a separate thread to avoid freezing the UI
        Thread(target=self._execute_sequence, args=(sequence,), daemon=True).start()
    
    def _execute_sequence(self, sequence):
        self.sequence_status.config(text="Sequence running...")
        self.update_status("Starting sequence execution")
        
        for step in sequence:
            try:
                if step.startswith("MFC:"):
                    # Parse MFC step
                    parts = step.split()
                    flow = float(parts[1])
                    duration = float(parts[4])
                    
                    # Execute step
                    self.flow_rate_entry.delete(0, tk.END)
                    self.flow_rate_entry.insert(0, str(flow))
                    self.set_mfc_flow()
                    time.sleep(duration)
                    
                elif step.startswith("Temp:"):
                    # Parse temperature step
                    parts = step.split()
                    temp = float(parts[1])
                    duration = float(parts[4])
                    
                    # Execute step
                    self.temp_setpoint_entry.delete(0, tk.END)
                    self.temp_setpoint_entry.insert(0, str(temp))
                    self.set_cooling_temp()
                    time.sleep(duration)
                    
                elif step.startswith("Valve:"):
                    # Parse valve step
                    parts = step.split()
                    pos = int(parts[2])
                    duration = float(parts[5])
                    
                    # Execute step
                    self.valve_position_var.set(pos)
                    self.set_valve_position()
                    time.sleep(duration)
                    
            except Exception as e:
                self.update_status(f"Sequence error: {str(e)}")
                messagebox.showerror("Sequence Error", f"Error executing step:\n{step}\n\n{str(e)}")
                break
        
        self.sequence_status.config(text="Sequence completed")
        self.update_status("Sequence execution finished")
    
    # Utility methods
    def update_status(self, message):
        """Update the status bar with a message"""
        self.status_bar.config(text=message)
        self.root.update_idletasks()
    
    def on_closing(self):
        """Clean up when closing the application"""
        # Add any cleanup code needed for devices here
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = LabEquipmentControl(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
