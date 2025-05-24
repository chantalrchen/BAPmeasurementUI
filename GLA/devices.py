import tkinter as tk
from tkinter import messagebox, ttk
import propar   # Bronkhorst MFC
import serial   # Cooling and Valve
import time 


class BronkhorstMFC:
    def __init__(self, port = "COM3"):
        self.port = port
        self.connected = False
        self.instrument = None
        # self.channel = channel
        self.massflow = 0
        self.targetmassflow = 0
        # self.maxmassflow = 4.0
        
    def connect(self):
        try:
            self.instrument = propar.instrument(self.port) # channel = self.channel)
            # print("I am in the MFC connecting function. My port is ", self.port)
            
            ##toegevoegd om te checken whether it is really connected, nog niet getest tho
            if self.get_massflow() is not False:
                self.connected = True
                self.initialize()
                return self.connected
        except Exception as err:
            messagebox.showerror("Error",
                f"An error occurred while connecting the Bronkhorst MFC with port {self.port}: {err}"
            )
        return False  


        ##FOR SIMULATION
        # self.connected = True
        # return self.connected
    

    def disconnect(self):
    # reset the value, fsetpoint = 0 
        try:
            param = [{'proc_nr':33 , 'parm_nr': 3, 'parm_type': propar.PP_TYPE_FLOAT, 'data': 0}]
            self.instrument.write_parameters(param) #Fsetpoint
            
        except Exception as err:
            messagebox.showerror("Error",
             f"An error occurred while disconnecting the Bronkhorst MFC: {err}")
     
        # self.connected = False
        # self.instrument = None
        
    
    def initialize(self):
        try:
            # controlfunction, the instrument works as a flow controller or a pressure controller; manual flexi-flow
            param = [{'proc_nr':115 , 'parm_nr': 10, 'parm_type': propar.PP_TYPE_INT8, 'data': 0}]
            # print("HI I AM IN MFC INITIALIZE FUNCTION MY CONNECTION IS", self.connected )
            self.instrument.write_parameters(param)
            return True


        except Exception as err:
            messagebox.showerror("Error",
                f"An error occurred while initializing the Bronkhorst MFC with channel"# {self.channel}: {err}"
            )
        return False  
    
        # #FOR SIMULATION
        # return True
  
    def get_massflow(self):
        ##the following should be connected when connected with Bronkhorst MFC
        if self.connected and self.instrument is not None:  # device is connected and assigned
            try:
                param = [{'proc_nr':  33, 'parm_nr': 0, 'parm_type': propar.PP_TYPE_FLOAT}] #Fmeasure
                self.massflow = self.instrument.read_parameters(param)
                return self.massflow  
            except Exception as err:
                messagebox.showerror("Error",
                    f"An error occurred while reading the mass flow rate: {err}"
                )
                return False  
        else:
            messagebox.showerror("Error", "The Bronkhorst MFC is not connected.")
            return False  

        # ##FOR SIMULATION
        # if self.connected:
        #     try:
        #         self.massflow += (self.targetmassflow - self.massflow) * 0.1
        #         if abs(self.massflow - self.targetmassflow) < 0.001:
        #             self.massflow = self.targetmassflow
        #         return self.massflow
        #     except Exception as err:
        #         messagebox.showerror("Error",
        #             f"An error occurred while reading the mass flow rate: {err}"
        #         )
        #         return False
        # else:
        #     messagebox.showerror("Error","The Bronkhorst MFC is not connected.")
        #     return False 

    def set_massflow(self, value: float):
        # ##the following should be connected when connected with Bronkhorst MFC
        if self.connected and self.instrument is not None:  # device is connected and assigned
        # if self.connected:
            try:
                # print("HI I AM IN THE SET_MASSFLOW LOOP AND SELF.CONNECTED IS", self.connected)
                # print(value, self.targetmassflow, self.maxmassflow)
                if value < 0:
                    messagebox.showwarning("Mass flow rate can't be negative", f"The mass flow rate can't be negative.")
                    return False             
                else:
                    self.targetmassflow = value
                    
                    #####
                    ###the following should be connected when connected with Bronkhorst MFC
                    param1 = [{'proc_nr':33 , 'parm_nr': 3, 'parm_type': propar.PP_TYPE_FLOAT, 'data': value}]
                    self.instrument.write_parameters(param1) #Fsetpoint
                    # print("HI IM NOW SETTING A MASSFLOW TO ", value)
                    ###
                    
                    return True  
            except Exception as err:
                messagebox.showerror("Error",
                    f"An error occurred while setting the mass flow rate: {err}"
                )
                return False  
        else:
            messagebox.showerror("Error", "The Bronkhorst MFCs is not connected.")
            return False  
        ##

class Koelingsblok:
    #### ALL COMMANDS
    MODEL_VERSION = 'v'
    SERIAL_NUMBER = 'V'
    SET_POINT_TEMPERATURE = 's'
    SET_STORE_NEW_SET_POINT_TEMPERATURE = 'n'
    SET_IDLE_MODE = 'i'
    CLEAR_IDLE_MODE = 'I'
    CURRENT_PLATE_TEMPERATURE = 'p'
    CURRENT_LOG_FILE = 'l'
    CLEAR_LOG_FILE = 'lc'
    START_LOGGING = 'ls'
    STOP_PAUSE_LOGGING = 'lp'
    SET_LOGGING_PERIOD_TO_1S ='le'
    SET_LOGGING_PERIOD_TO_1MIN = 'lm'
    SET_LOGGING_PERIOD_TO_5MIN= 'l5'
    RESET_UNIT_TO_DEFAULT_CONFIGURATION = '#Z'
    CF ='\r'
    LF ='\n'

    def __init__(self, port='COM7', baudrate=9600, timeout=1):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.connected = False
        self.instrument = None

    def connect(self):
        try:
            self.instrument = serial.Serial(self.port, baudrate=self.baudrate, timeout=self.timeout)
            self.connected = True
            return True
        except serial.SerialException as err:
            messagebox.showerror("Error",
                    f"An error occurred while connecting the cooling system: {err}") 
            self.connected = False
            return False

    def disconnect(self):
        try:
            if self.connected:
                self.instrument.close()
                self.connected = False
                print("Cooling system is disconnected")
                return True
        except serial.SerialException as err:
            messagebox.showerror("Error",
                    f"An error occurred while disconnecting the cooling system: {err}") 
            self.connected = False      
            return False

    def send_command(self, command):
        if not self.connected:
            print("Cooling system is not connected")
            return False
        
        try:
            self.instrument.write(f"{command}{self.CF}".encode('ascii'))  #-> self.CF = \r'
            # 100ms delay after each command sent (after \r)
            time.sleep(0.1)
            response = self.instrument.readline().decode('ascii').strip() #-> readline will read till <LF> = \n and then stops
            return response
        except Exception as e:
            print(f"Error sending command '{command}': {e}")
            return False
    
    def get_temperature(self):
        if not self.connected:
            print("Cooling system is not connected")
            return False
        
        try:
            response = self.send_command(self.CURRENT_PLATE_TEMPERATURE)
            
            print(self.send_command(self.CLEAR_IDLE_MODE))
            raw = self.instrument.readline()
            print(f"Raw response bytes: {raw}")
            
            if response:
                print(f"Current plate temperature is {response}")
                return response
            else:
                print("No respond received to get the temperature")
                return False
        except Exception as e:
            print(f"Error getting temperature: {e}")
            return False

    def set_temperature(self, temperature, ambient_temp):
        if self.connected:
            try:
                min_temp = ambient_temp - 30
                if temperature < min_temp:
                    messagebox.showwarning("Value exceeds the minimum temperature", f"The ambient temperature is {temperature:.2f}. The temperature may not exceed {min_temp:.2f} °C. Please enter another temperature.")
                    return False
                else:
                    response = self.send_command(f"{self.SET_STORE_NEW_SET_POINT_TEMPERATURE}{temperature}")
                    raw = self.instrument.readline()
                    print(f"Raw response bytes: {raw}")

                    if response.lower() == "ok":
                        print(f"Temperature successfully set to {temperature}°C")
                        return True
                    else:
                        print(f"Failed to set temperature: {response}")
                        return False
            
            except Exception as err:
                messagebox.showerror("Error",
                    f"An error occurred while setting the temperature: {err}"
                )
                return False  # Operation failed
        else:
            messagebox.showerror("Error", "The Torrey Pines IC20XR Digital Chilling/Heating Dry Baths is not connected.")
            return False #Operation failed
        
        #To simulate
        # self.targettemperature = temperature
  
class RVM:
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
        self.port = port
        self.valve_port = valve_ports
        self.mode = mode #the answer mode for mode = 0 the valve will response immediately 
        self.address = address # unit 1 -> command = f"/1Z\r" (check manual))
        self.connected = False
        self.instrument = None
        self.current_position = None

    def connect(self):
        try:
            self.instrument = serial.Serial(self.port, baudrate=9600, timeout=1)
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
                
        # ##For simulation
        # self.currentposition = 1

    def switch_position(self, position: int):
        if position not in [1, 2]:
            raise ValueError("The position of the valve can only be 1 or 2")

        print(f"Switching RVM Industrial Microfluidic Rotary Valve to position {position}")
        self.send_command(self.SWITCH_SHORTEST, position)
        time.sleep(self.ROTATION_DELAY)
        self.check_status()
        self.current_position = position
        print(f"RVM Industrial Microfluidic Rotary Valve is in positie {position}.")
        
        # ##For simulation
        # self.current_position = position
        # return True

    def get_position(self):
        pos = self.send_command(self.GET_VALVE_POSITION)
        self.current_position = int(pos)
        print(f"The current position of RVM Industrial Microfluidic Rotary Valve is {self.current_position}")
        return self.current_position
        
        # ##For simulation
        # return self.current_position    
    
    def check_status(self):
        while True:
            status = self.send_command(self.GET_STATUS_DETAILS)
            if status == '0':
                break
            elif status == '255':
                time.sleep(self.POLLING_PERIOD)
            else:
                raise ValveError(f"invalid status: {status}")

    def build_command(self, command, parameter=None):
        cmd = f"{self.START_COMMAND}{self.ADDRESS}{command}"
        if parameter is not None:
            cmd += str(parameter)
        if command[0] not in self.NO_R_REQUIRED:
            cmd += self.EXECUTE
        cmd += self.END_COMMAND
        return cmd

    def send_command(self, command, parameter=None):
        if not self.connected:
            raise ValveError("RVM Industrial Microfluidic Rotary Valve is not connected")

        full_cmd = self.build_command(command, parameter)
        self.instrument.reset_input_buffer()
        self.instrument.write(full_cmd.encode())
        error, data = self.read_response()
        self.check_error(error)
        return data

    def read_response(self):
        response = self.instrument.read_until(self.END_ANSWER.encode()).decode('utf-8').strip()
        if not response.startswith('/'):
            raise ValveError(f"invalid response: {response}")

        response = response[2:]  # Verwijder '/' en adres
        error_code = response[0]
        data = response[1:].replace(self.END_ANSWER.strip(), '')
        error = {'@': [0, 'No error'], '`': [0, 'No error']}.get(error_code, [999, 'Invalid error'])
        return error, data

    def check_error(self, error):
        if error[0] != 0:
            raise ValveError(f"error {error[0]}: {error[1]}")
        
#for rvm
class ValveError(Exception):
    '''Error class for AMF modules.

        Attributes:
          message -- explanation of the error
    '''
