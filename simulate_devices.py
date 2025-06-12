import tkinter as tk
from tkinter import messagebox

# This code has been written by C.R. Chen and F.Lin for the BAP project E-nose.

# This file is purely used to simulate the devices

class BronkhorstMFC:
    """To simulate the control and monitor the Bronkhorst Mass Flow Controller - Flexi Flow
    """
    def __init__(self, port = "COM3"):
        """Initialize the simualted BronkhorstMFC

        Args:
            port (str, optional): COM port to which MFC is connected. Defaults to "COM3".
        """
        # Initalization of the COM-port at which the device is connected
        self.port = port
        
        # Initializiation of the flag whether the device is connected or not
        self.connected = False
        self.instrument = None
        
        # Initialization of the last measured massflow
        self.massflow = 0
        
        # Initialization of the target massflow
        self.targetmassflow = 0
        
    def connect(self):
        """Connect to the MFC and initialize the parameters

        Returns:
            boolean: True if connected successfully, False if not connected successfully
        """
        # Assumuning connecting always goed correctly
        self.connected = True
        return self.connected
    
    def initialize(self):
        """Initializing the MFC as a flow controller

        Returns: None
        """
        # Assuming initalizing always goes correctly
        return True
  
    def get_massflow(self):
        """ Reading the mass flow rates (in mL/min) from the MFC 

        Returns:
            float: The actual measured mass flow rate (self.massflow) if reading the parameter was successfull
            boolean False: if the device is not connected or reading mass flow rate went wrong
        """
        if self.connected:
            try:
                # Simulate as if the massflow is gradually updating to target massflow rate
                self.massflow += (self.targetmassflow - self.massflow) * 0.1

                # For simulation: if the difference is very small, assign it to the target massflow rate
                if abs(self.massflow - self.targetmassflow) < 0.001:
                    self.massflow = self.targetmassflow
                return self.massflow
            
            except Exception as err:
            # Show error if something goes wrong during the update
                messagebox.showerror("Error",
                    f"An error occurred while reading the mass flow rate: {err}"
                )
                return False
        else:
            messagebox.showerror("Error","The Bronkhorst MFC is not connected.")
            return False 

    def set_massflow(self, value: float):
        """ Setting the target mass flow rate and write it to the MFC

        Args:
            value (float): the target mass flow rate that the user want to set

        Returns:
            boolean: True if the massflowrate is successfully written, False otherwise
        """
        # Check if the MFC is connected
        if self.connected:
            try:
                # Block negative values
                if value < 0:
                    # Show Messagebox when user input a negative value
                    messagebox.showwarning("Mass flow rate can't be negative", f"The mass flow rate can't be negative.")
                    return False             
                else:
                    # For simulation set the value directly to targetmassflow
                    self.targetmassflow = value
                    return True  
            except Exception as err:
                # Show error if writing to the instrument fails
                messagebox.showerror("Error",
                    f"An error occurred while setting the mass flow rate: {err}"
                )
                return False  
        else:
        # Show error if the device is not connected
            messagebox.showerror("Error", "The Bronkhorst MFCs is not connected.")
            return False  

class RVM:
    """To simulate the control and monitor the AMF Rotary Valve
    """

    def __init__(self, port='COM8', valve_ports=4, mode=0, address=1):
        """Initialize the simulated AMF Rotary Valve

        Args:
            port (str, optional): COM port of the RVM. Defaults to 'COM8'.
            valve_ports (int, optional): Number of ports on the RVM. Defaults to 4.
            mode (int, optional): Communication mode. Defaults to 0.
            address (int, optional): _descripDevice adress for serial communication. Defaults to 1.
        """
        self.port = port
        self.valve_port = valve_ports
        self.mode = mode #the answer mode for mode = 0 the valve will response immediately 
        self.address = address # unit 1 -> command = f"/1Z\r" (check manual))
        self.connected = False
        self.instrument = None
        self.current_position = None

    def connect(self):
        """ Connect to the RVM through serial communication and initialize the valve

        Returns:
            Boolean: True if successfull serial communication and initialization, otherwise false.
        """
        self.connected = True
        return True

    def disconnect(self):
        """ Disconnect to the RVM

        Returns:
            Boolean: True if disconnection was successful, False if already disconnected.
        """
        self.connected = False
        return False

    def home(self):
        """ Send homing command to the RVM to reset its position reference.
        """
        self.currentposition = 1

    def switch_position(self, position: int):
        """Switch the rotary valves position

        Args:
            position (int): Target position (1 or 2)

        Raises:
            ValueError: if the input position is not 1 or 2
        """
        self.current_position = position
        return True

    def get_position(self):
        """ Get/Read the position from the RVM

        Returns:
            int: Current position of the RVM
        """
        return self.current_position
