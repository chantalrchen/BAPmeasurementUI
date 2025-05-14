import tkinter as tk
from tkinter import messagebox, ttk
import propar   # Bronkhorst MFC
import serial   # Cooling and Valve
import time 
import threading
# import amfTools

###
#MFC
class BronkhorstMFC:
    def __init__(self, port = "COM3"):
        self.port = port
        self.connected = False
        self.instrument = None
        # self.channel = channel
        self.massflow = 0
        self.targetmassflow = 0
        self.maxmassflow = 4.0
        
    def connect(self):
        try:
            self.instrument = propar.instrument(self.port) # channel = self.channel)
            print("I am in the MFC connecting function. My port is ", self.port)
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
    
    #reset the value, fsetpoint = 0 
    def disconnect(self):
        try:
            param = [{'proc_nr':33 , 'parm_nr': 3, 'parm_type': propar.PP_TYPE_FLOAT, 'data': 0}]
            self.instrument.write_parameters(param) #Fsetpoint
            
        except Exception as err:
            messagebox.showerror("Error",
             f"An error occurred while disconnecting the Bronkhorst MFC: {err}")
     


    #     self.connected = False
    #     self.instrument = None
        
    
    def initialize(self):
        try:
            # controlfunction, the instrument works as a flow controller or a pressure controller; manual flexi-flow
            param = [{'proc_nr':115 , 'parm_nr': 10, 'parm_type': propar.PP_TYPE_INT8, 'data': 0}]
            print("HI I AM IN MFC INITIALIZE FUNCTION MY CONNECTION IS", self.connected )
            self.instrument.write_parameters(param)


        except Exception as err:
            messagebox.showerror("Error",
                f"An error occurred while initializing the Bronkhorst MFC with channel"# {self.channel}: {err}"
            )
        return False  
    
        #FOR SIMULATION
        #  return True
  
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

        ##FOR SIMULATION
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
        ##the following should be connected when connected with Bronkhorst MFC
        if self.connected and self.instrument is not None:  # device is connected and assigned
        # if self.connected:
            try:
                print("HI I AM IN THE SET_MASSFLOW LOOP AND SELF.CONNECTED IS", self.connected)
                print(value, self.targetmassflow, self.maxmassflow)
                if value < 0:
                    messagebox.showwarning("Mass flow rate can't be negative", f"The mass flow rate can't be negative.")
                    return False             
                elif value > self.maxmassflow:
                    messagebox.showwarning("Value exceeds the maximum mass flow rate", f"The mass flow rate may not exceed {self.maxmassflow:.2f} mL/min. The mass flow rate will be set to {self.maxmassflow:.2f} mL/min.")
                    self.targetmassflow = self.maxmassflow
                    
                    # ####
                    # ##the following should be connected when connected with Bronkhorst MFC
                    param = [{'proc_nr':33 , 'parm_nr': 3, 'parm_type': propar.PP_TYPE_FLOAT, 'data': self.maxmassflow}]
                    self.instrument.write_parameters(param)
                    print("HI IM NOW SETTING A MASSFLOW TO ", self.maxmassflow)
                    # ###
                    
                    return True
                else:
                    self.targetmassflow = value
                    
                    #####
                    ###the following should be connected when connected with Bronkhorst MFC
                    param1 = [{'proc_nr':33 , 'parm_nr': 3, 'parm_type': propar.PP_TYPE_FLOAT, 'data': value}]
                    self.instrument.write_parameters(param1) #Fsetpoint
                    print("HI IM NOW SETTING A MASSFLOW TO ", value)
                    ####
                    
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
    def __init__(self, port = 'COM7'):
        self.port = port
        self.connected = False
        self.instrument = None
        self.temperature = 0
        self.targettemperature = 0
        self.dummy = 0
    
    def connect(self):
        
        # ##the following should be connected when connected with the Torrey Pines IC20XR Digital Chilling/Heating Dry Baths
        # # p24: 9600 baud, 1 stop bit, no parity, no hardware handshake, 100ms delay after each command sent (after \r)
        # # 100 ms delay, so a timeout of 1s should be enough
        try:
            self.instrument = serial.Serial(
                self.port,
                baudrate=9600,
                timeout=3,
                write_timeout=2,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                rtscts=False,
                dsrdtr=False,
                xonxoff=False
            )
            print("I am in the cooling connecting function. My port is ", self.port)
            self.connected = True
            return self.connected
        except Exception as err:
            messagebox.showerror("Error",
                f"An error occurred while connecting the Torrey Pines IC20XR Digital Chilling/Heating Dry Baths: {err}"
            )
        return False  # Operation failed
        # ##
        
        ##the following is used only for simulation
        # self.connected = True
        # return self.connected
        # ##
        
    def get_temperature(self):
    
        # ##the following should be connected when connected with the Torrey Pines IC20XR Digital Chilling/Heating Dry Baths
        if self.connected and self.instrument is not None: 
            try:
                # sending a request to read the temperature; The current plate temperature will be returned in a text string terminated by <CR><LF>, e.g. 14.3\r
                self.instrument.write(b"p\r")  
                # 100ms delay after each command sent (after \r)
                time.sleep(0.1)  
                self.response = self.instrument.read_until(b"\r").decode().strip()  # reads until \r
                return self.response
            except Exception as err:
                messagebox.showerror("Error",
                    f"An error occurred while getting the temperature: {err}"
                )
                return False  # Operation failed
        else:
            return False #Operation failed
        # ##
        
            ##the following is used only for simulation
            # if dummy == 0:
            #     return self.temperature
            # elif dummy == 1:                
            #     if self.connected:
            #         try:
            #             self.temperature += (self.targettemperature - self.temperature) * 0.1
            #             if abs(self.temperature - self.targettemperature) < 0.001:
            #                 self.temperature = self.targettemperature
            #             return self.temperature
            #         except Exception as err:
            #             messagebox.showerror("Error",
            #                 f"An error occurred while reading the temperature: {err}"
            #             )
            #             return False
            #     else:
            #         messagebox.showerror("Error","The Torrey Pines IC20XR Digital Chilling/Heating Dry Baths is not connected.")
            #         return False  # Operation failed
        ##

    # def set_temperature(self, value: float, temp_ambient):

    #     ##the following should be connected when connected with the Torrey Pines IC20XR Digital Chilling/Heating Dry Baths
    #     if self.connected and self.instrument is not None: 
    #     # if self.connected:
    #         try:
    #             #the cooling system can only lower the temperature by 30 degrees below ambient
    #             min_temp = temp_ambient - 30
    #             if value < min_temp:
    #                 messagebox.showwarning("Value exceeds the minimum temperature", f"The ambient temperature is {temp_ambient:.2f}. The temperature may not exceed {min_temp:.2f} °C")
    #                 self.targettemperature = min_temp
                    
    #                 ###OFFICIAL
    #                 ##the following should be connected when connected with the Torrey Pines IC20XR Digital Chilling/Heating Dry Baths
    #                 # self.instrument.write(b"n" + str(min_temp).encode() + "\r") 
                    
    #                 #if the above does not work, try: 
    #                 self.instrument.write(f"n{value}\r".encode()) 
    #                 # 100ms delay after each command sent (after \r)
    #                 time.sleep(0.1) 
    #                 return True
    #             else:
    #                 self.targettemperature = value
                    
    #                 ##OFFICIAL
    #                 ##the following should be connected when connected with the Torrey Pines IC20XR Digital Chilling/Heating Dry Baths
    #                 # self.instrument.write(b"n" + str(value).encode() + "\r") 
                    
    #                 #if the above does not work, try: 
    #                 self.instrument.write(f"n{value}\r".encode()) 
    #                 # 100ms delay after each command sent (after \r)
                    
    #                 time.sleep(0.1) 
    #                 return True
    #         except Exception as err:
    #             messagebox.showerror("Error",
    #                 f"An error occurred while setting the temperature: {err}"
    #             )
    #             return False  # Operation failed
    #     else:
    #         messagebox.showerror("Error", "The Torrey Pines IC20XR Digital Chilling/Heating Dry Baths is not connected.")
    #         return False #Operation failed
        
    def set_temperature(self, value: float, temp_ambient):
        if not self.connected:
            messagebox.showwarning("Device not connected", "Cooling device is not connected.")
            return

        if not isinstance(temp_ambient, (int, float)):
            messagebox.showwarning("Ambient Temp Missing", "Set the ambient temperature first.")
            return

        # Launch background thread
        threading.Thread(target=self.threaded_set_temperature, args=(value, temp_ambient), daemon=True).start()
    
    def threaded_set_temperature(self, target_temp, temp_ambient):
        min_temp = temp_ambient - 30

        if target_temp < min_temp:
            messagebox.showwarning(
                "Temperature Too Low",
                f"Temperature can't be lower than {min_temp:.2f} °C based on ambient {temp_ambient:.2f} °C. It will be set to {min_temp:.2f} °C."
            )
            target_temp = min_temp

        try:
            if self.instrument.out_waiting > 0:
                self.instrument.reset_output_buffer()
            self.instrument.reset_input_buffer()

            command = f"n{target_temp:.1f}\r"
            print(f"[Cooling] Sending: {repr(command)}")
            written = self.instrument.write(command.encode('ascii'))
            print(f"[Cooling] Bytes written: {written}")
            
            time.sleep(12)  # Give time to process
            response = self.instrument.read_until(b"\r").decode().strip()
            print(f"[Cooling] Response: {response}")

            self.targettemperature = target_temp

        except serial.SerialTimeoutException:
            messagebox.showerror("Serial Timeout", f"Timeout writing to {self.port}.")
        except serial.SerialException as err:
            messagebox.showerror("Serial Error", f"Serial communication error: {err}")
        except Exception as err:
            messagebox.showerror("Unknown Error", f"Unexpected error: {err}")

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

    def __init__(self, port='COM4', valve_ports=4, mode=0, address=1):
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

        except serial.SerialException as err:
            messagebox.showerror("Error",
                    f"An error occurred while connecting RVM Industrial Microfluidic Rotary Valve: {err}") 
            self.connected = False

    def disconnect(self):
        if self.connected:
            self.instrument.close()
            self.connected = False
            print("RVM Industrial Microfluidic Rotary Valve is disconnected")

    def home(self):
        print("Homing RVM Industrial Microfluidic Rotary Valve...")
        self.send_command(self.HOME)
        time.sleep(self.ROTATION_DELAY)
        self.check_status()
        print("RVM Industrial Microfluidic Rotary Valve homed")

    def switch_position(self, position: int):
        if position not in [1, 2]:
            raise ValueError("The position of the valve can only be 1 or 2")

        print(f"Switching RVM Industrial Microfluidic Rotary Valve to position {position}")
        self.send_command(self.SWITCH_SHORTEST, position)
        time.sleep(self.ROTATION_DELAY)
        self.check_status()
        self.current_position = position
        print(f"RVM Industrial Microfluidic Rotary Valve is in positie {position}.")

    def get_position(self):
        pos = self.send_command(self.GET_VALVE_POSITION)
        self.current_position = int(pos)
        print(f"The current position of RVM Industrial Microfluidic Rotary Valve is {self.current_position}")
        return self.current_position

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


class AutomatedSystemUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Automated System")
        self.root.geometry("1400x800")
        
        self.mfcs = [BronkhorstMFC(port = 'COM6'), BronkhorstMFC(port = 'COM5'), BronkhorstMFC(port = 'COM3')] #,  BronkhorstMFC(port = 'COM3', channel = 2), BronkhorstMFC(port = 'COM3', channel = 3)]
        self.cooling = Koelingsblok()
        self.valve = RVM()
        
        # Header frame for connection and status
        header_frame = ttk.Frame(self.root)
        header_frame.pack(side='top', fill='x', padx=5, pady=5)
        
        # Connection status frame
        connection_frame = ttk.Frame(header_frame)
        connection_frame.pack(side='right', padx=10)
        
        ttk.Label(connection_frame, text="Device Connections", font=("Arial", 11, "bold")).pack(fill = 'both', expand = True)
        # Connection status labels
        self.connection_mfc1_port_label = ttk.Label(connection_frame, 
                                                 text=f"MFC Port: {self.mfcs[0].port}, Connected: {self.mfcs[0].connected}")
        self.connection_mfc1_port_label.pack(fill='both', expand=True)
        
        self.connection_mfc2_port_label = ttk.Label(connection_frame, 
                                                 text=f"MFC Port: {self.mfcs[1].port}, Connected: {self.mfcs[1].connected}")
        self.connection_mfc2_port_label.pack(fill='both', expand=True)
        
        self.connection_mfc3_port_label = ttk.Label(connection_frame, 
                                                 text=f"MFC Port: {self.mfcs[2].port}, Connected: {self.mfcs[2].connected}")
        self.connection_mfc3_port_label.pack(fill='both', expand=True)
        
        # Cooling        
        self.connection_cooling_port_label = ttk.Label(connection_frame, 
                                                     text=f"Cooling Port: {self.cooling.port}, Connected: {self.cooling.connected}")
        self.connection_cooling_port_label.pack(fill='both', expand=True)
        
        self.connection_valve_port_label = ttk.Label(connection_frame, 
                                                  text=f"RVM Port: {self.valve.port}, Connected: {self.valve.connected}")
        self.connection_valve_port_label.pack(fill='both', expand=True)
        
        connect_all_button = ttk.Button(connection_frame, text = "Connect all devices", command = self.connect_all_devices)
        connect_all_button.pack(side='right', fill = 'both', expand = 'true')
        
        othervar_frame  = ttk.Frame(header_frame)
        othervar_frame.pack(side='right', padx=10)
        
        # Ambient temperature section
        ttk.Label(othervar_frame, text="Set Ambient Temperature", font=("Arial", 11, "bold")).pack(fill='both', expand=True)
        # Label and Entry for ambient temperature
        self.ambient_temp_label = tk.Label(othervar_frame, text=f"Ambient Temperature (°C): not set")
        self.ambient_temp_label.pack(fill='both', expand=True)
        self.ambient_temp = tk.DoubleVar()  # Use DoubleVar for floating-point values
        self.ambient_temp_entry = tk.Entry(othervar_frame, textvariable = self.ambient_temp)
        self.ambient_temp_entry.pack(fill='both', expand=True)
        ambient_temp_button = ttk.Button(othervar_frame, text = "Set ambient temperature", command = self.set_ambient_temp)
        ambient_temp_button.pack(fill='both', expand=True)
        
        # Status bar, to show what has been adjusted
        # Status label
        self.status_var = tk.StringVar() 
        self.status_var.set("Status:")
        status_bar = ttk.Label(header_frame, text='Status', textvariable=self.status_var)
        status_bar.pack(fill='both', padx=5, pady=5)
        
        self.running_var_bar = tk.Label(header_frame, text="")
        self.running_var_bar.pack(side= 'bottom', fill='x')
        
        # Notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True)

        self.create_menu()
        self.create_device_tab()
        
    def set_ambient_temp(self):
        """
        Retrieve the ambient temperature from the entry box and set it.
        """
        try:
            # Get the value from the entry box
            self.ambient_temp = float(self.ambient_temp_entry.get())
            # Update the status bar to show the ambient temperature has been set
            self.ambient_temperature_label.config(text=f"Ambient temperature: {self.ambient_temp} °C")
            self.ambient_temp_label.config(text=f"Ambient temperature: {self.ambient_temp} °C")
            self.status_var.set(f"Ambient temperature set to {self.ambient_temp} °C")
        except ValueError:
            self.status_var.set("Invalid input! Enter a floating number for the ambient temperature.")
            messagebox.showerror("Invalid Input", "Please enter a floating number for ambient temperature.")
            
    def update_run_var(self):
 
        # Get mass flow rates from MFCs
        mass_flow_1 = f"{self.mfcs[0].get_massflow()[0]['data']:} mL/min" if self.mfcs[0].connected else "N/A"
        mass_flow_2 = f"{self.mfcs[1].get_massflow()[0]['data']:.2f} mL/min" if self.mfcs[1].connected else "N/A"
        mass_flow_3 = f"{self.mfcs[2].get_massflow()[0]['data']:.2f} mL/min" if self.mfcs[2].connected else "N/A"
        
        # print("what we get back from get_massflow()", self.mfcs[0].get_massflow()[0]['data'])
        
        # Get temperature from cooling system
        temperature = f"{self.cooling.get_temperature()} °C" if self.cooling.connected else "N/A"

        # Get valve position from valve
        valve_position = self.valve.currentposition if self.valve.connected else "N/A"
        self.running_var_bar.config(text=f"MFC 1 Mass Flow Rate: {mass_flow_1} | MFC 2 Mass Flow Rate: {mass_flow_2} | MFC 3 Mass Flow Rate: {mass_flow_3} | Temperature: {temperature} | Valve Position: {valve_position}")

        # Schedule the next update
        self.notebook.after(10, self.update_run_var)
        
    def create_menu(self):
        menu = tk.Menu(self.root)
        
        # Settings menu
        settings_menu = tk.Menu(menu, tearoff=0)
        settings_menu.add_command(label="Communication Settings", command=self.com_settings)
        menu.add_cascade(label="Settings", menu=settings_menu)
        
        self.root.config(menu=menu)
    
    def create_device_tab(self):
        device_tab = ttk.Frame(self.notebook)
        device_tab.pack(fill='both', expand=True)
        self.notebook.add(device_tab, text="Device Control")
        self.notebook.pack(expand=True, fill='both')
        
        ############	MFC		###########################
        self.mfc_frames = []
        self.massflow_vars = []
        self.current_massflow_labels = []
        self.target_massflow_labels = []
        
        all_mfc_frame = ttk.LabelFrame(device_tab)
        all_mfc_frame.pack(fill='x', padx=10, pady=5)
        
        for index in range(3):
            # Create a frame for the MFC
            mfc_frame = ttk.LabelFrame(all_mfc_frame, text=f'MFC {index+1}')
            mfc_frame.grid(row = 0, column = index, padx=10, pady=5)
            self.mfc_frames.append(mfc_frame)  # Store the frame reference

            # Label for mass flow rate
            massflow_label = tk.Label(mfc_frame, text="Mass flow rate (mL/min):")
            massflow_label.grid(row=0, column=0, padx=10, pady=10)

            # Entry field for mass flow rate
            massflow_var = tk.DoubleVar()
            massflow_entry = tk.Entry(mfc_frame, textvariable=massflow_var)
            massflow_entry.grid(row=0, column=1, padx=10, pady=10)
            self.massflow_vars.append(massflow_var)  # Store the variable reference

            # Button to set the mass flow rate
            # lambda: anonymous function means that the function is without a name. 
            # using lambda, such that it doesn't run the function when initiating the program, and passes the value index to the function
            # https://www.geeksforgeeks.org/using-lambda-in-gui-programs-in-python/
            set_massflow_button = tk.Button(mfc_frame, text="Set mass flow rate", command=lambda i = index : self.set_MFCmassflow(i))
            set_massflow_button.grid(row=1, column=0, columnspan=2, pady=10)

            # Label to display the current flow rate
            current_massflow_label = tk.Label(mfc_frame, text="Current mass flow rate: Not available")
            current_massflow_label.grid(row=2, column=0, padx=10, pady=10)
            self.current_massflow_labels.append(current_massflow_label)  # Store the label reference

            # Label to display the target flow rate
            target_massflow_label = tk.Label(mfc_frame, text=f"Target mass flow rate: {self.mfcs[index].targetmassflow:.2f} mL/min")
            target_massflow_label.grid(row=2, column=1, padx=10, pady=10)
            self.target_massflow_labels.append(target_massflow_label)  # Store the label reference
            
            # Connect button
            MFC_connect_button = tk.Button(mfc_frame, text="Connect", command=lambda i = index :self.connect_MFC(i))
            MFC_connect_button.grid(row=3, column=0, padx=10, pady=10)

        # # Disconnect button
        # MFC_disconnect_button = tk.Button(mfc_frame, text="Disconnect", command= lambda i = index : self.disconnect_MFC(i))
        # MFC_disconnect_button.grid(row=3, column=1, padx=10, pady=10)

        ############	COOLING		###########################
        cooling_frame = ttk.LabelFrame(device_tab, text='Cooling')
        cooling_frame.pack(fill='x', padx=10, pady=5)
        
        # label for the temp
        temperature_label = tk.Label(cooling_frame, text="Temperature (°C):")
        temperature_label.grid(row=0, column=0, padx=10, pady=10)
        
        # entry field for temp
        self.temperature_var = tk.DoubleVar()
        temperature_entry = tk.Entry(cooling_frame, textvariable=self.temperature_var)
        temperature_entry.grid(row=0, column=1, padx=10, pady=10)
        
        # button to set the temp
        set_temperature_button = tk.Button(cooling_frame, text="Set temperature", command=self.set_temperature)
        set_temperature_button.grid(row=1, column=0, columnspan=2, pady=10)

        # Connect button
        cooling_connect_button = tk.Button(cooling_frame, text="Connect", command=self.connect_cooling)
        cooling_connect_button.grid(row=1, column=1, padx=10, pady=10)
        
        # Label to display the ambient temp
        self.ambient_temperature_label = tk.Label(cooling_frame, text=f"Ambient temperature: Not set")
        self.ambient_temperature_label.grid(row=2, column=0, padx=10, pady=10)
        
        # Label to display the current temp
        self.current_temperature_label = tk.Label(cooling_frame, text="Current temperature: Not available")
        self.current_temperature_label.grid(row=2, column=1, padx=10, pady=10)
        
        # Label to display the target temp
        self.target_temperature_label = tk.Label(cooling_frame, text=f"Target temperature: {self.cooling.targettemperature:.2f} °C")
        self.target_temperature_label.grid(row=2, column=2, padx=10, pady=10)


        # # Disconnect button
        # cooling_disconnect_button = tk.Button(cooling_frame, text="Disconnect", command=self.disconnect_cooling)
        # cooling_disconnect_button.grid(row=3, column=1, padx=10, pady=10)

        ############	VALVE		###########################
        valve_frame = ttk.LabelFrame(device_tab, text='Valve')
        valve_frame.pack(fill='x', padx=10, pady=5)
        
        # Valve position control
        ttk.Label(valve_frame, text="Valve Position:").grid(row=0, column=0, padx=10, pady=10)
        self.valve_pos_var = tk.IntVar(value=1)
        ttk.Combobox(valve_frame, textvariable=self.valve_pos_var, values=[1, 2], width=5).grid(row=0, column=1, padx=10, pady=10)

        # # button to switch the position
        # set_valve_button = tk.Button(valve_frame, text="Switch position", command=self.set_valve)
        # set_valve_button.grid(row=1, column=0, columnspan=2, pady=10)
        # button to set the position of the valve
        set_valve_button = tk.Button(valve_frame, text="Set valve", command=self.set_valve)
        set_valve_button.grid(row=1, column=0, columnspan=2, pady=10)

        # Connect button
        valve_connect_button = tk.Button(valve_frame, text="Connect", command=self.connect_valve)
        valve_connect_button.grid(row=1, column=1, padx=10, pady=10)
    
        # Disconnect button
        valve_disconnect_button = tk.Button(valve_frame, text="Disconnect", command=self.disconnect_valve)
        valve_disconnect_button.grid(row=1, column=2, padx=10, pady=10)

        # Label to display the current position of the valve
        self.current_valve_label = tk.Label(valve_frame, text="Current position of the valve: Not available") ## 2 positions available: ON and OFF
        self.current_valve_label.grid(row=2, column=0, padx=10, pady=10)
        
    def connect_MFC(self, index):
        if self.mfcs[index].connect():
            #messagebox.showinfo("Connection", "MFC successfully connected.")
            #updating the connection info
            self.update_connection_devices()
            self.status_var.set(f"MFC {index + 1} connected")
        else:
            messagebox.showinfo("Connection Failed", f"MFC {index + 1} is not connected")
            
    # def disconnect_MFC(self, index):
    #     self.mfcs[index].disconnect()
    #     #messagebox.showinfo("Disconnected", "MFC disconnected successfully.")
    #     #updating the connection info
    #     self.update_connection_devices()
    #     self.status_var.set(f"MFC {index + 1} disconnected")
    
    def connect_cooling(self):  
        if self.cooling.connect():
            #messagebox.showinfo("Connection", "Torrey Pines IC20XR Digital Chilling/Heating Dry Baths successfully connected.")
            #updating the connection info
            self.update_connection_devices()
            self.status_var.set(f"Torrey Pines IC20XR Digital Chilling/Heating Dry Baths connected")
        else:
            messagebox.showinfo("Connection Failed", "Cooling is not connected")
         
    # def disconnect_cooling(self):
    #     self.cooling.disconnect()
    #     #messagebox.showinfo("Disconnected", "Torrey Pines IC20XR Digital Chilling/Heating Dry Baths disconnected successfully.")
    #     #updating the connection info
    #     self.update_connection_devices()
    #     self.status_var.set(f"Torrey Pines IC20XR Digital Chilling/Heating Dry Baths disconnected")

    def connect_valve(self):  
        if self.valve.connect():
            #messagebox.showinfo("Connection", "RVM Industrial Microfluidic Rotary valve is successfully connected.")
            #updating the connection info
            self.update_connection_devices()
            
            #initializing the home position of the valve
            self.currentposition = 1
            
            self.status_var.set(f"RVM Industrial Microfluidic Rotary valve connected and set to home position 1")
        else:
            messagebox.showinfo("Connection Failed", "RVM is not connected")
         
    def disconnect_valve(self):
        self.valve.disconnect()
        #messagebox.showinfo("Disconnected", "RVM Industrial Microfluidic Rotary valve is disconnected successfully.")
        #updating the connection info
        self.update_connection_devices()
        self.status_var.set(f"RVM Industrial Microfluidic Rotary valve disconnected")

    def connect_all_devices(self):
        self.connect_MFC(index = 0)
        self.connect_MFC(index = 1)
        self.connect_MFC(index = 2)
        self.connect_cooling()
        self.connect_valve()
        self.status_var.set(f"MFC, Torrey Pines IC20XR Digital Chilling/Heating Dry Baths and RVM Industrial Microfluidic Rotary valve connected")
   
    def update_connection_devices(self):
        
        #Labels at the Header
        self.connection_mfc1_port_label.config (text=f"MFC 1 Port: {self.mfcs[0].port}, Connected: {self.mfcs[0].connected}")
        self.connection_mfc2_port_label.config (text=f"MFC 2 Port: {self.mfcs[1].port}, Connected: {self.mfcs[1].connected}")
        self.connection_mfc3_port_label.config (text=f"MFC 3 Port: {self.mfcs[2].port}, Connected: {self.mfcs[2].connected}")
        self.connection_cooling_port_label.config(text=f"Cooling Port: {self.cooling.port}, Connected: {self.cooling.connected}")
        self.connection_valve_port_label.config(text=f"RVM Port: {self.valve.port}, Connected: {self.valve.connected}")

    def com_settings(self):
        #Opens een top level window
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Connection Settings")
        settings_window.geometry("400x400")
        
        #this forces all focus on the top level until the toplevel is closed
        settings_window.grab_set()
        
        # Bronkhorst MFC settings
        MFC_frame = ttk.LabelFrame(settings_window, text="Bronkhorst MFC")
        MFC_frame.pack(fill="both", padx=10, pady=10)
        
        ttk.Label(MFC_frame, text="Port:").grid(row=0, column=0, padx=5, pady=5)
        self.MFC1_port_var = tk.StringVar(value=self.mfcs[0].port)
        MFC1_port_entry = ttk.Entry(MFC_frame, textvariable=self.MFC1_port_var)
        MFC1_port_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(MFC_frame, text="Port:").grid(row=1, column=0, padx=5, pady=5)
        self.MFC2_port_var = tk.StringVar(value=self.mfcs[1].port)
        MFC2_port_entry = ttk.Entry(MFC_frame, textvariable=self.MFC2_port_var)
        MFC2_port_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(MFC_frame, text="Port:").grid(row=2, column=0, padx=5, pady=5)
        self.MFC3_port_var = tk.StringVar(value=self.mfcs[2].port)
        MFC3_port_entry = ttk.Entry(MFC_frame, textvariable=self.MFC3_port_var)
        MFC3_port_entry.grid(row=2, column=1, padx=5, pady=5)
        
        # Cooling settings
        cooling_frame = ttk.LabelFrame(settings_window, text="Torrey Pines IC20XR Digital Chilling/Heating Dry Baths")
        cooling_frame.pack(fill="both", padx=10, pady=10)
        
        ttk.Label(cooling_frame, text="Port:").grid(row=3, column=0, padx=5, pady=5)
        self.cooling_port_var = tk.StringVar(value=self.cooling.port)
        cooling_port_entry = ttk.Entry(cooling_frame, textvariable=self.cooling_port_var)
        cooling_port_entry.grid(row=3, column=1, padx=5, pady=5)
        
        # valve settings
        valve_frame = ttk.LabelFrame(settings_window, text="RVM Industrial Microfluidic Rotary valve ")
        valve_frame.pack(fill="both", padx=10, pady=10)
        
        ttk.Label(valve_frame, text="Port:").grid(row=4, column=0, padx=5, pady=5)
        self.valve_port_var = tk.StringVar(value=self.valve.port)
        valve_port_entry = ttk.Entry(valve_frame, textvariable=self.valve_port_var)
        valve_port_entry.grid(row=4, column=1, padx=5, pady=5)
            
        save_button = ttk.Button(settings_window, text="Save", command=self.save_settings)
        save_button.pack(pady=10)
        
    def save_settings(self):
        self.mfcs[0].port = self.MFC1_port_var.get()
        self.mfcs[1].port = self.MFC2_port_var.get()
        self.mfcs[2].port = self.MFC3_port_var.get()
        self.cooling.port = self.cooling_port_var.get()
        self.valve.port = self.valve_port_var.get()
        
        self.update_connection_devices()
        self.status_var.set("Port connections are updated.")

    def set_MFCmassflow(self, index):
        massflowrate = self.massflow_vars[index].get()
        if self.mfcs[index].set_massflow(massflowrate):
            self.target_massflow_labels[index].config(text=f"Target mass flow rate: {self.mfcs[index].targetmassflow} mL/min")
            self.update_massflow(index)
        else:
            self.status_var.set("MFC: Failed to set mass flow rate.")
            
    def update_massflow(self, index):
        current_flow = self.mfcs[index].get_massflow()[0]['data']
        self.update_run_var()
        if current_flow is not None:
            self.current_massflow_labels[index].config(text=f"Current mass flow rate: {current_flow:.2f} mL/min")
        else:
            self.status_var.set("Failed to read mass flow rate.")
        
        # Passing the index to the function by using lambda
        # Lambda are anonymous function means that the function is without a name
        # https://www.geeksforgeeks.org/using-lambda-in-gui-programs-in-python/
        self.root.after(1000, lambda: self.update_massflow(index)) #updating the MFC flow rate reading each 1s
        
    def set_temperature(self):
        if self.cooling.connected == False:
            messagebox.showwarning("Device not connected", "The Torrey Pines IC20XR Digital Chilling/Heating Dry Baths is not connected")
            return False
        elif not isinstance(self.ambient_temp, (int, float)):
            messagebox.showwarning("Invalid Input", "Ambient Temperature has not been set yet or is an non-numeric value.")
            return False
        else:    
            try:
                temperature = float(self.temperature_var.get())
                self.cooling.set_temperature(temperature, self.ambient_temp)
                self.target_temperature_label.config(text=f"Target temperature: {self.cooling.targettemperature:.2f} °C")
                self.update_temperature()
                
                ##if non-floating number, tk.tclerror occurs
            except tk.TclError as e:
                messagebox.showerror("Invalid Input", f"Please enter a floating number for target temperature. {e}")
                
    def update_temperature(self):
        current_temp = self.cooling.get_temperature()
        self.update_run_var()
        if current_temp is not None:
            self.current_temperature_label.config(text=f"Current temperature: {current_temp} °C")
        else:
            self.status_var.set("Failed to read the temperature.")
        
        #Updating temperature every 1s; otherwise the simulation/reading the data won't work. It would only happen one time.
        #https://www.geeksforgeeks.org/python-after-method-in-tkinter/
        self.notebook.after(1000, self.update_temperature) 
        
    def set_valve(self):
        position = self.valve_pos_var.get()
        if self.valve.switch_position(position):
            self.update_valve()

    def update_valve(self):
        target_position = self.valve.get_position()
        self.update_run_var()
        if target_position is not None:
            if self.currentposition != target_position:                
                self.current_valve_label.config(text=f"Current position of the valve: {target_position}")
                self.status_var.set(f"The position is set to {target_position}.")
            else:
                self.status_var.set(f"The target position is the current position, position {target_position}.")
        else:
            self.status_var.set("Failed to read the position of the valve.")
    
        
def main():
    root = tk.Tk()
    app = AutomatedSystemUI(root)
    root.mainloop()
    
if __name__ == "__main__":
    main()
