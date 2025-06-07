import tkinter as tk
from tkinter import messagebox, ttk
import propar   # Bronkhorst MFC
import serial   # Valve
import time 

##To control and monitor the real devices

class BronkhorstMFC:
    """To control and monitor the Bronkhorst Mass Flow Controller - Flexi Flow
    """
    def __init__(self, port = "COM3"):
        """Initialize the BronkhorstMFC

        Args:
            port (str, optional): COM-port of the MFC. Defaults to "COM3".
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
        try:
            # Connect the MFC with the corresponding COM-port
            self.instrument = propar.instrument(self.port) 
            self.connected = True
            
            #Initalize the parameters
            self.initialize()
            
            return True
        except Exception as err:
            # Show messagebox when connnection failed
            messagebox.showerror("Error",
                f"An error occurred while connecting the Bronkhorst MFC with port {self.port}: {err}"
            )
        return False  
    
    def initialize(self):
        """Initializing the MFC as a flow controller

        Returns: None
        """
        try:
            # Write the value of the Control Function to '0', such that the MFC is initalized as flow controller
            # Manual Flexi-Flow p29
            param = [{'proc_nr':115 , 'parm_nr': 10, 'parm_type': propar.PP_TYPE_INT8, 'data': 0}]
            self.instrument.write_parameters(param)

        except Exception as err:
            # Showing messagebox when initializing MFC failed
            messagebox.showerror("Error",
                f"An error occurred while initializing the Bronkhorst MFC with port {self.port}"
            )
        
    def get_massflow(self):
        """ Reading the mass flow rates (in mL/min) from the MFC 

        Returns:
            float: The actual measured mass flow rate (self.massflow) if reading the parameter was successfull
            boolean False: if the device is not connected or reading mass flow rate went wrong
        """
        # Check whether the device is connected
        if self.connected and self.instrument is not None:  # device is connected and assigned
            try:
                # Read the mass flow rate from the MFC
                # Manual Flexi-Flow p29, Fmeasure
                param = [{'proc_nr':  33, 'parm_nr': 0, 'parm_type': propar.PP_TYPE_FLOAT}] 
                self.massflow = self.instrument.read_parameters(param)
                return self.massflow  
            except Exception as err:
                # Show Messagebox when reading mass flow rate failed
                messagebox.showerror("Error",
                    f"An error occurred while reading the mass flow rate: {err}"
                )
                return False  
        else:
            # Show Messagebox when the MFC is not connected.
            messagebox.showerror("Error", f"The Bronkhorst MFC ({self.port}) is not connected.")
            return False  

    def set_massflow(self, value: float):
        """ Setting the target mass flow rate and write it to the MFC

        Args:
            value (float): the target mass flow rate that the user want to set

        Returns:
            boolean: True if the massflowrate is successfully written, False otherwise
        """
        # Check if the MFC is connected
        if self.connected and self.instrument is not None: 
            try:
                # Block negative values
                if value < 0:
                    # Show Messagebox when user input a negative value
                    messagebox.showwarning("Mass flow rate can't be negative", f"The mass flow rate can't be negative.")
                    return False                            
                else:
                    self.targetmassflow = value
                    # Write the target massflow rate to the parameter Fsetpoint
                    # Manual Flexiflow p29 Fsetpoint
                    param1 = [{'proc_nr':33 , 'parm_nr': 3, 'parm_type': propar.PP_TYPE_FLOAT, 'data': value}]
                    self.instrument.write_parameters(param1)
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
    """To control and monitor the AMF Rotary Valve
    The example code from AMF have been used: https://amf.ch/?post_type=document "Software Examples Python V1"
    This code has somewhat been adjusted for our use
    """
    
    #### ALL COMMANDS
    START_COMMAND = '/'
    END_COMMAND = '\r'
    POLLING_PERIOD = 0.05 ## time for repeated status check
    ADDRESS = '1' #unit 1 -> command = f"/1Z\r" (check manual)
    ROTATION_DELAY = 0.4  # 400 ms rotatietijd for Fast Mode

    START_ANSWER = '/'
    MASTER_ADDRESS = '0'
    END_ANSWER = '\x03\r\n'

    NO_R_REQUIRED = ['?', '!', 'H', 'T', 'Q','X','$','%','#','&','*']

    ERROR_CODES = {'@': [0, 'No Error'],
                   "`": [0, 'No Error'],
                   'A': [1, 'Initialization'],
                   'B': [2, 'Invalid command'],
                   'C': [3, 'Invalid operand'],
                   'D': [4, 'Missing trailing [R]'],
                   'G': [7, 'Device not initialized'],
                   'H': [8, 'Internal failure (valve)'],
                   'I': [9, 'Plunger overload'],
                   'J': [10, 'Valve overload'],
                   'N': [14, 'A/D converter failure'],
                   'O': [15, 'Command overflow'], }

    STATUS_CODES = {'255': [255, 'Busy', 'Valve currently executing an instruction.'],
                    '000': [0, 'Done', 'Valve available for next instruction.'],
                    '128': [128, 'Unknown command', 'Check that the command is written properly'],
                    '144': [144, 'Not homed', 'You forgot the homing! Otherwise, check that you have the right port configuration and try again.'],
                    '145': [145, 'Move out of range', 'You’re probably trying to do a relative positioning and are too close to the limits.'],
                    '146': [146, 'Speed out of range', 'Check the speed that you’re trying to go at.'],
                    '224': [224, 'Blocked', 'Something prevented the valve to move.'],
                    '225': [225, 'Sensor error', 'Unable to read position sensor. This probably means that the cable is disconnected.'],
                    '226': [226, 'Missing main reference', ('Unable to find the valve’s main reference magnet '
                                                            'during homing. This can mean that a reference magnet '
                                                            'of the valve is bad/missing or that the motor is '
                                                            'blocked during homing. Please also check motor '
                                                            'cables and crimp.')],
                    '227': [227, 'Missing reference', ('Unable to find a valve’s reference magnet during '
                                                       'homing. Please check that you have the correct valve '
                                                       'number configuration with command "/1?801". If '
                                                       'not, change it according to the valve you are working '
                                                       'with. This can also mean that a reference magnet of '
                                                       'the valve is bad/missing or that the motor is blocked '
                                                       'during homing.')],
                    '228': [228, 'Bad reference polarity', ('One of the magnets of the reference valve has a bad '
                                                            'polarity. Please check that you have the correct valve '
                                                            'number configuration with command "/1?801". If '
                                                            'not, change it according to the valve you are working '
                                                            'with. This can also mean that a reference magnet has '
                                                            'been assembled in the wrong orientation in the valve.')],
                    }

    # %%% COMMANDS
    # %%%% Configuration Commands
    SET_ADDRESS = '@ADDR='              # 1-9 or A-E, 1 by default
    SET_ANSWER_MODE = '!50'             # Synchronous = 0, Asynchronous = 1, Asynchronous + counter = 2, 0 by default
    SET_VALVE_CONFIGURATION = '!80'     # 4, 6, 8, 10 or 12 valve positions, 6 by default
    RESET_VALVE_COUNTER = '!17'
    SLOW_MODE = '-'                     # RVMFS only
    FAST_MODE = '+'                     # RVMFS only
    ACTIVATE_RS232 = '@RS232'           # Activated by default
    ACTIVATE_RS485 = '@RS485F'
    
    # Plunger command
    SET_PLUNGER_FORCE = '!30'           # 0,1,2 or 3 (0 = high and 3 = low force), 3 by default
    SET_PEAK_SPEED = 'V'                # 0-1600 pulses/s, 150 by default
    SET_ACCELERATION_RATE = 'L'         # 100-59'590 pulses/s², 1557 by default
    SET_DECELERATION_RATE = 'l'         # 100-59'590 pulses/s², 59'590 by default
    SET_SCALLING = 'N'                      # 0 or 1 (0 = 0.01 mm resolution, 1 = 0.00125mm resolution), 0 by default
    
    # %%%% Control Commands
    EXECUTE = 'R'
    REEXECUTE = 'X'
    REPEAT = 'G'                        # 0-60'000, 0 by default = loop forever
    REPEAT_SEQUENCE_START = 'g'
    DELAY = 'M'                         # 0-86'400'000 milliseconds
    HALT = 'H'                          # Pause the sequence AFTER finishng the current move
    HARD_STOP = 'T'                     # Interrupt the current move and supress it from the sequence
    POWER_OFF = '@POWEROFF'             # Shut down the pump

    # %%%% Initialization Commands
    HOME = 'Z'
    HOME2 = 'Y'

    # %%%% Valve Commands
    SWITCH_SHORTEST_FORCE = 'B'
    SWITCH_SHORTEST = 'b'

    SWITCH_CLOCKWISE_FORCE = 'I'
    SWITCH_CLOCKWISE = 'i'

    SWITCH_COUNTERCLOCKWISE_FORCE = 'O'
    SWITCH_COUNTERCLOCKWISE = 'o'
    
    # %%%% Plunger Commands
    ABSOLUTE_POSITION = 'A'             # 0-3000 with N=0, 0-24'000 with N=1
    ABSOLUTE_POSITION2 = 'a'            
    
    RELATIVE_PICKUP = 'P'               # 0-3000 with N=0, 0-24'000 with N=1
    RELATIVE_PICKUP2 = 'p'
    
    RELATIVE_DISPENSE = 'D'             # 0-3000 with N=0, 0-24'000 with N=1
    RELATIVE_DISPENSE2 = 'd'

    # %%%% Report Commands
    GET_STATUS = 'Q'
    GET_PLUNGER_POSITION = '?'
    GET_MAX_SPEED = '?2'
    GET_PLUNGER_ACTUAL_POSITION = '?4'
    GET_VALVE_POSITION = '?6'
    GET_VALVE_NUMBER_MOVES = '?17'
    GET_VALVE_NUMBER_MOVES_SINCE_LAST = '?18'
    GET_SPEED_MODE = '?19' 
    GET_FIRMWARE_CHECKSUM = '?20'
    GET_FIRMWARE_VERSIOM = '?23'
    GET_ACCELERATION = '?25'
    GET_ADDRESS = '?26'
    GET_DECELERATION = '?27'
    GET_SCALLING = '?28'
    GET_CONFIGURATION = '?76'
    GET_PLUNGER_CURRENT = '?300'        # x10 mA
    GET_ANSWER_MODE = '?500'
    GET_NUMBER_VALVE_POSITION = '?801'
    RESET = '$'
    GET_SUPPLY_VOLTAGE = '*'            # x0.1 V
    GET_UID = '?9000'
    IS_PUMP_INITIALIZED = '?9010'       # 1 = True
    GET_PUMP_STATUS_DETAILS = '?9100'
    GET_STATUS_DETAILS = '?9200'
    #####

    def __init__(self, port='COM8', valve_ports=4, mode=0, address=1):
        """Initialize the AMF Rotary Valve

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
        try:
            # Serial communicate with the RVM
            self.instrument = serial.Serial(self.port, baudrate=9600, timeout=1)
            self.connected = True
            print(f"RVM Industrial Microfluidic Rotary Valve is in position {self.port}")

            # Basisconfiguratie
            self.send_command(self.SET_ADDRESS, self.address)
            self.send_command(self.SET_ANSWER_MODE, self.mode)
            self.send_command(self.SET_VALVE_CONFIGURATION, self.valve_port)

            # Valve initialiseren and set the valve position to 1
            self.home()
            self.switch_position(1)
            return True

        except serial.SerialException as err:
            # Show error message if serial connection fails
            messagebox.showerror("Error",
                    f"An error occurred while connecting RVM Industrial Microfluidic Rotary Valve: {err}") 
            self.connected = False
            return False

    def disconnect(self):
        """ Disconnect to the RVM

        Returns:
            Boolean: True if disconnection was successful, False if already disconnected.
        """
        # Check if the device is connected  
        if self.connected:
            # Close the serial communication with the device
            self.instrument.close()
            self.connected = False
            print("RVM Industrial Microfluidic Rotary Valve is disconnected")
            return True
        else:
            return False

    def home(self):
        """ Send homing command to the RVM to reset its position reference.
        """
        print("Homing RVM Industrial Microfluidic Rotary Valve...")
        # Send home command to initialize valve's position
        self.send_command(self.HOME)
        # Wait for the valve to finish rotating
        time.sleep(self.ROTATION_DELAY)
        # Check the valve's status to ensure homing is complete
        self.check_status()
        print("RVM Industrial Microfluidic Rotary Valve homed")        

    def switch_position(self, position: int):
        """Switch the rotary valves position

        Args:
            position (int): Target position (1 or 2)

        Raises:
            ValueError: if the input position is not 1 or 2
        """
        
        # Check whether the input position is 1 or 2
        if position not in [1, 2]:
            raise ValueError("The position of the valve can only be 1 or 2")

        print(f"Switching RVM Industrial Microfluidic Rotary Valve to position {position}")
        # Send the command to move with the shortest path toward the target position
        self.send_command(self.SWITCH_SHORTEST, position)
        # Wait for the valve to complete rotation
        time.sleep(self.ROTATION_DELAY)
        # Confirm the valve completed its movement
        self.check_status()
        # Update the current position
        self.current_position = position
        print(f"RVM Industrial Microfluidic Rotary Valve is in positie {position}.")
    
    def get_position(self):
        """ Get/Read the position from the RVM

        Returns:
            int: Current position of the RVM
        """
        # Read the current position of the RVM
        pos = self.send_command(self.GET_VALVE_POSITION)
        self.current_position = int(pos)
        print(f"The current position of RVM Industrial Microfluidic Rotary Valve is {self.current_position}")
        return self.current_position

    def check_status(self):
        """ Check the RVM status

        Raises:
            ValveError: If an unexpected status is returned
        """
        while True:
            # Send command to obtain the status details
            status = self.send_command(self.GET_STATUS_DETAILS)
            # RVM is ready
            if status == '0':
                break
            
            # RVM is busy
            elif status == '255':
                time.sleep(self.POLLING_PERIOD)
            else:
                raise ValveError(f"invalid status: {status}")

    def build_command(self, command, parameter=None):
        """Build the command to construct a properly formatted command string to send to the valve.

        Args:
            command (str): the base command code
            parameter (float, optional): Optional parameter to include with the command. Defaults to None.

        Returns:
            cmd (str): Formatted command string  
        """
        cmd = f"{self.START_COMMAND}{self.ADDRESS}{command}"
        if parameter is not None:
            cmd += str(parameter)
        if command[0] not in self.NO_R_REQUIRED:
            cmd += self.EXECUTE
        cmd += self.END_COMMAND
        return cmd

    def send_command(self, command, parameter=None):
        """Send command to RVM

        Args:
            command (str): Command code to send.
            parameter (float, optional): Optional parameter. Defaults to None.

        Raises:
            ValveError: If valve is not connected or if an error is detected.

        Returns:
            str: Data obtained from the valve
        """
        if not self.connected:
            raise ValveError("RVM Industrial Microfluidic Rotary Valve is not connected")

        # Build and send full command
        full_cmd = self.build_command(command, parameter)
        self.instrument.reset_input_buffer()
        self.instrument.write(full_cmd.encode())
        
        # Read the response
        error, data = self.read_response()
        self.check_error(error)
        return data

    def read_response(self):
        """Read the response from the valve

        Raises:
            ValveError: if response format is invalid

        Returns:
            tuple:  (error list [code, message], response data string)
        """
        response = self.instrument.read_until(self.END_ANSWER.encode()).decode('utf-8').strip()
        if not response.startswith('/'):
            raise ValveError(f"invalid response: {response}")

        response = response[2:]  # Verwijder '/' en adres
        error_code = response[0]
        data = response[1:].replace(self.END_ANSWER.strip(), '')
        error = {'@': [0, 'No error'], '`': [0, 'No error']}.get(error_code, [999, 'Invalid error'])
        return error, data

    def check_error(self, error):
        """
        Raise an exception if an error code was returned.

        Args:
            error (list): Error code and message.

        Raises:
            ValveError: If error code is not zero.
        """
        if error[0] != 0:
            raise ValveError(f"error {error[0]}: {error[1]}")
        
#for rvm
class ValveError(Exception):
    '''Error class for AMF modules.

        Attributes:
          message -- explanation of the error
    '''