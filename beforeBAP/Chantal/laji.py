import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import scrolledtext
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time
import threading
import csv
import datetime


# Placeholder functions to interact with the hardware (replace with actual API calls)
def get_temperature():
    # Placeholder: Get temperature from Torrey Pines IC20XR
    return 25.0  # Replace with real API call

def set_temperature(temp):
    # Placeholder: Set temperature on the Torrey Pines IC20XR
    pass  # Replace with real API call

def set_valve_position(position):
    # Placeholder: Set valve position on the RVM
    pass  # Replace with real API call

def get_flow_rate():
    # Placeholder: Get flow rate from the MFC (Bronkhorst)
    return 10.0  # Replace with real API call

def set_flow_rate(rate):
    # Placeholder: Set flow rate on the MFC (Bronkhorst)
    pass  # Replace with real API call

class MFCControlSystem:
    def __init__(self, window):
        self.window = window
        self.running = False
        self.time_data = []
        self.flow_data = []
        self.pressure_data = []
        self.logs = []  # Store logs in a list

        self.create_ui()

    def create_ui(self):
        # Main Frame
        frame = tk.Frame(self.window)
        frame.pack(padx=20, pady=20)

        # Left frame for input controls
        left_frame = tk.Frame(frame)
        left_frame.grid(row=0, column=0, padx=20)

        # Temperature Control (IC20XR)
        temp_label = tk.Label(left_frame, text="Target Temperature: ")
        temp_label.grid(row=0, column=0, pady=10)
        self.temp_entry = tk.Entry(left_frame, width=50)
        self.temp_entry.grid(row=1, column=0, pady=10)

        # Valve Control (RVM)
        valve_label = tk.Label(left_frame, text="Valve Position (%): ")
        valve_label.grid(row=2, column=0, pady=10)
        self.valve_entry = tk.Entry(left_frame, width=50)
        self.valve_entry.grid(row=3, column=0, pady=10)

        # Flow rate control (MFC)
        flow_label = tk.Label(left_frame, text="Flow Rate: ")
        flow_label.grid(row=4, column=0, pady=10)
        self.flow_entry = tk.Entry(left_frame, width=50)
        self.flow_entry.grid(row=5, column=0, pady=10)

        # Update button
        update_button = tk.Button(left_frame, text="Update Parameters", command=self.update_parameters)
        update_button.grid(row=6, column=0, pady=20)

        # Start/Stop Button
        self.start_stop_button = tk.Button(left_frame, text="Start", command=self.toggle_system)
        self.start_stop_button.grid(row=7, column=0, pady=20)

        # Export Logs Button
        export_button = tk.Button(left_frame, text="Export Logs", command=self.export_logs)
        export_button.grid(row=8, column=0, pady=20)

        # Right frame for display of updated parameters
        right_frame = tk.Frame(frame)
        right_frame.grid(row=0, column=1, padx=20)

        # Display updated values
        self.temp_display = tk.Label(right_frame, text="Current Temperature: ")
        self.temp_display.grid(row=0, column=1, pady=10)

        self.valve_display = tk.Label(right_frame, text="Valve Position: ")
        self.valve_display.grid(row=1, column=1, pady=10)

        self.flow_display = tk.Label(right_frame, text="Flow Rate: ")
        self.flow_display.grid(row=2, column=1, pady=10)

        # Logging Data Display
        self.log_display = scrolledtext.ScrolledText(right_frame, width=50, height=10)
        self.log_display.grid(row=3, column=1, pady=10)

        # Create the figure for plotting
        self.figure, self.ax = plt.subplots()
        self.ax.set_title("Flow Rate & Pressure Over Time")
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Parameter Value")

        # Embed matplotlib figure into tkinter window
        self.canvas = FigureCanvasTkAgg(self.figure, master=right_frame)
        self.canvas.get_tk_widget().grid(row=4, column=1, pady=10)

    def update_parameters(self):
        """Update parameters and display them"""
        try:
            # Get the temperature, flow rate, and valve position values
            temp = float(self.temp_entry.get())
            flow_rate = float(self.flow_entry.get())
            valve_position = float(self.valve_entry.get())

            # Update devices (placeholders)
            set_temperature(temp)
            set_flow_rate(flow_rate)
            set_valve_position(valve_position)

            # Update displays
            self.temp_display.config(text=f"Current Temperature: {temp}°C")
            self.flow_display.config(text=f"Flow Rate: {flow_rate} ml/min")
            self.valve_display.config(text=f"Valve Position: {valve_position}%")

            # Log the changes
            log_entry = f"Temperature: {temp}°C, Flow Rate: {flow_rate} ml/min, Valve Position: {valve_position}%"
            self.logs.append(log_entry)
            self.log_display.insert(tk.END, log_entry + "\n")
            self.log_display.yview(tk.END)

            # Update data for plotting (only if system is running)
            if self.running:
                self.time_data.append(time.time())
                self.flow_data.append(flow_rate)
                self.pressure_data.append(get_flow_rate())  # Simulated for now

                # Redraw the graph
                self.ax.clear()
                self.ax.plot(self.time_data, self.flow_data, label="Flow Rate", color='blue')
                self.ax.plot(self.time_data, self.pressure_data, label="Pressure", color='red')
                self.ax.legend()
                self.ax.set_title("Flow Rate & Pressure Over Time")
                self.ax.set_xlabel("Time (s)")
                self.ax.set_ylabel("Parameter Value")
                self.canvas.draw()
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numerical values.")

    def toggle_system(self):
        """Start/Stop the system and manage the start/stop button"""
        if self.running:
            self.running = False
            self.start_stop_button.config(text="Start")
        else:
            self.running = True
            self.start_stop_button.config(text="Stop")

            # Simulate data updates every second
            threading.Thread(target=self.simulate_data_updates).start()

    def simulate_data_updates(self):
        """Simulate parameter changes over time"""
        while self.running:
            self.update_parameters()
            time.sleep(1)

    def export_logs(self):
        """Automatically export logs to a CSV file with datetime-based filename"""
        # Get the current date and time for the filename
        current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        log_filename = f"logs_{current_time}.csv"

        try:
            with open(log_filename, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Timestamp", "Temperature (°C)", "Flow Rate (ml/min)", "Valve Position (%)"])
                for log in self.logs:
                    writer.writerow([time.strftime("%Y-%m-%d %H:%M:%S"), *log.split(", ")])
            messagebox.showinfo("Export Successful", f"Logs successfully exported to {log_filename}")
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export logs: {e}")

# Create the main window
window = tk.Tk()
window.title("MFC Control System")

# Initialize the control system
control_system = MFCControlSystem(window)

# Start the tkinter event loop
window.mainloop()
