import tkinter as tk
from tkinter import messagebox, ttk
import propar   # Bronkhorst MFC
import serial   # Valve
import time 

# This code has been written by C.R. Chen and F.Lin for the BAP project E-nose.

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
        """ Reading the flow rates (in mL/min) from the MFC 

        Returns:
            float: The actual measured flow rate (self.massflow) if reading the parameter was successfull
            boolean False: if the device is not connected or reading flow rate went wrong
        """
        # Check whether the device is connected
        if self.connected and self.instrument is not None:  # device is connected and assigned
            try:
                # Read the flow rate from the MFC
                # Manual Flexi-Flow p29, Fmeasure
                param = [{'proc_nr':  33, 'parm_nr': 0, 'parm_type': propar.PP_TYPE_FLOAT}] 
                self.massflow = self.instrument.read_parameters(param)
                return self.massflow  
            except Exception as err:
                # Show Messagebox when reading flow rate failed
                messagebox.showerror("Error",
                    f"An error occurred while reading the flow rate: {err}"
                )
                return False  
        else:
            # Show Messagebox when the MFC is not connected.
            messagebox.showerror("Error", f"The Bronkhorst MFC ({self.port}) is not connected.")
            return False  

    def set_massflow(self, value: float):
        """ Setting the target flow rate and write it to the MFC

        Args:
            value (float): the target flow rate that the user want to set

        Returns:
            boolean: True if the massflowrate is successfully written, False otherwise
        """
        # Check if the MFC is connected
        if self.connected and self.instrument is not None: 
            try:
                # Block negative values
                if value < 0:
                    # Show Messagebox when user input a negative value
                    messagebox.showwarning("Flow rate can't be negative", f"The flow rate can't be negative.")
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
                    f"An error occurred while setting the flow rate: {err}"
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
    POLLING_PERIOD = 0.1 ## time for repeated status check
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
        self.port = port
        self.valve_port = valve_ports
        self.mode = mode #the answer mode for mode = 0 the valve will response immediately 
        self.address = address # unit 1 -> command = f"/1Z\r" (check manual))
        self.connected = False
        self.instrument = None
        self.current_position = None

    def connect(self):
        try:
            self.instrument = serial.Serial(self.port, baudrate=9600, timeout=10)
            self.connected = True
            print(f"RVM Industrial Microfluidic Rotary Valve is in position {self.port}")

            # Basisconfiguratie
            self.send_command(self.SET_ADDRESS, self.address)
            self.send_command(self.SET_ANSWER_MODE, self.mode)
            self.send_command(self.SET_VALVE_CONFIGURATION, self.valve_port)

            # Valve initialiseren
            self.home()
            self.switch_position(1)
            return True

        except serial.SerialException as err:
            messagebox.showerror("Error",
                    f"An error occurred while connecting RVM Industrial Microfluidic Rotary Valve: {err}") 
            self.connected = False
            return False
        
        # ##TO simulate
        # self.connected = True
        # return True

    def disconnect(self):
        if self.connected:
            self.instrument.close()
            self.connected = False
            print("RVM Industrial Microfluidic Rotary Valve is disconnected")
            return True
        else:
            return False
        
        ##To simulate
        # self.connected = False
        # return False

    def home(self):
        print("Homing RVM Industrial Microfluidic Rotary Valve...")
        self.send_command(self.HOME)
        time.sleep(self.ROTATION_DELAY)
        self.check_status()
        print("RVM Industrial Microfluidic Rotary Valve homed")        
        
    def switch_position(self, position: str, direction='ANY', force=False):
        if direction not in ['ANY', 'CW', 'CCW']:
            raise ValueError('Direction parameter must be one of: "ANY","CW","CCW"]')

        if position not in [1, 2]:
            raise ValueError("The position of the valve can only be 1 or 2")
        print(position)
        command_switch = {'ANY': 'SWITCH_SHORTEST',
                          'CW': 'SWITCH_CLOCKWISE',
                          'CCW': 'SWITCH_COUNTERCLOCKWISE'}
        cmd = command_switch.get(direction)

        if force:
            cmd += '_FORCE'

        self.send_command(eval(f'self.{cmd}'), position)
        time.sleep(self.ROTATION_DELAY)
        self.check_status()
        self.current_position = position
        print(f"RVM Industrial Microfluidic Rotary Valve is in positie {position}.")
        print(f'Valve in position {position}')

    def get_position(self):
        self.current_position = int(self.send_command(self.GET_VALVE_POSITION))
        print(f"The current position of RVM Industrial Microfluidic Rotary Valve is {self.current_position}")
        return self.current_position
        

    def send_command(self, command: str, parameter: str = None) -> str:
        """Send a command, get a response back and return the response. (No Status check)"""
        if not self.connected:
            raise ValveError('No AMF valve is connected.')

        original_command = command
          
        command = self.START_COMMAND + str(self.address) + original_command

        # format the command if it has some parameter
        if parameter is not None:
            command = command + str(parameter)

        if original_command[0] not in self.NO_R_REQUIRED:
            command = command + self.EXECUTE

        command = command + self.END_COMMAND

        self.instrument.write(data=command.encode())
        time.sleep(0.2)
        error, data = self.read_response()
        self.check_error(error)

        return data

    def check_status(self):
        busy = True
        status = '255'
        while busy:
            if status == '0':
                busy = False
            else:
                time.sleep(self.POLLING_PERIOD)
            
            self.instrument.reset_input_buffer()
            status = self.send_command(self.GET_STATUS_DETAILS)
            print (f'status = {status}')
            if status not in ['0', '1', '255', '', None]:
                raise ValveError(f'Bad Status: {self.STATUS_CODES.get(status)}')
                
    def read_response(self):
        response = self.instrument.read_until(self.END_ANSWER.encode()).decode('utf-8')
        print(" This is the response", response, "end response")
        if self.mode == 2 and response[2] == '`' and len(response) > 2:
            if response[3] != 0:
                if response[-len(self.END_ANSWER):] == self.END_ANSWER:
                    response = response[:-len(self.END_ANSWER)]
                        
                error = self.ERROR_CODES[response[2].upper()]
                self.counter = response[3:]
                data = '0'
                return error, data
            else:
                response = response[2:]
        else: 
            response = response[2:]

        if response[-len(self.END_ANSWER):] == self.END_ANSWER:
            response = response[:-len(self.END_ANSWER)]

        error = self.ERROR_CODES[response[0].upper()]
        data = response[1:]

        return error, data

    def check_error(self, error):
        code = error[0]

        if code == 0:
            return True
        raise ValveError(f'{error[0]}: {error[1]}')
        
#for rvm
class ValveError(Exception):
    '''Error class for AMF modules.

        Attributes:
          message -- explanation of the error
    '''